# coding: utf-8

from PIL import Image
from PIL.ExifTags import TAGS


class ExifException(Exception):
    pass


class Exif(object):

    def __init__(self, fn):
        if isinstance(fn, Image.Image):
            self.im = fn
            self.overwrite = False
        elif isinstance(fn, (str, unicode)):
            self.im = Image.open(fn)
            self.overwrite = True
        else:
            raise ExifException()

        self.fn = fn
        self.get_exif()

    def get_exif(self):
        self.data = {}
        info = self.im._getexif()
        for tag, value in info.items():
            decoded = TAGS.get(tag, tag)
            self.data[decoded] = value
        return self.data

    def rotate(self):
        # We rotate regarding to the EXIF orientation information
        if 'Orientation' in self.data.keys():
            orientation = self.data['Orientation']
            if orientation == 1:
                # Nothing
                self.im = self.im.copy()
            elif orientation == 2:
                # Vertical Mirror
                self.im = self.im.transpose(Image.FLIP_LEFT_RIGHT)
            elif orientation == 3:
                # Rotation 180°
                self.im = self.im.transpose(Image.ROTATE_180)
            elif orientation == 4:
                # Horizontal Mirror
                self.im = self.im.transpose(Image.FLIP_TOP_BOTTOM)
            elif orientation == 5:
                # Horizontal Mirror + Rotation 270°
                self.im = self.im.transpose(Image.FLIP_TOP_BOTTOM).transpose(Image.ROTATE_270)
            elif orientation == 6:
                # Rotation 270°
                self.im = self.im.transpose(Image.ROTATE_270)
            elif orientation == 7:
                # Vertical Mirror + Rotation 270°
                self.im = self.im.transpose(Image.FLIP_LEFT_RIGHT).transpose(Image.ROTATE_270)
            elif orientation == 8:
                # Rotation 90°
                self.im = self.im.transpose(Image.ROTATE_90)

            # No more Orientation information
            self.data['Orientation'] = 1

    def delete_exif(self):
        self.im.info.clear()

    def clear(self, quality=100):
        self.rotate()
        self.delete_exif()

        if self.overwrite:
            self.im.save(self.fn, quality=quality)
        else:
            return self.im
