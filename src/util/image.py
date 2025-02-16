import os

from .ansi    import *
from .printer import *

from PIL          import Image
from PIL.ExifTags import Base
from datetime     import datetime

IMAGE_EXTENSIONS = ['.jpg', '.jpeg', '.png', '.bmp', '.gif', '.ico', '.psd', '.webp', '.tif', '.tiff']
IMAGE_FILETYPES  = [('图像文件', ';'.join('*' + ext for ext in IMAGE_EXTENSIONS))]

class InImage:
    def __init__(self, path: str) -> None:
        self._path   = path
        self._dir    = os.path.dirname(path)
        self._name   = os.path.basename(path)
        self._size   = os.path.getsize(path)
        raw          = self.raw
        self._width  = raw.width
        self._height = raw.height
    
    @property
    def path(self):
        return self._path
    
    @property
    def dir(self):
        return self._dir
    
    @property
    def name(self):
        return self._name
    
    @property
    def size(self):
        return self._size
    
    @property
    def image(self) -> Image.Image:
        return self.raw.convert('RGBA')
    
    @property
    def raw(self) -> Image.Image:
        if not os.path.isfile(self._path):
            raise FileExistsError(f'文件\'{self.name}\'不存在.')
        try:
            return Image.open(self._path)
        except Image.UnidentifiedImageError:
            raise TypeError(f'文件\'{self.name}\'格式不支持.')
    
    @property
    def exif(self):
        data = None
        with Image.open(self._path) as raw:
            data = raw._getexif()
        return {
            Base.Make             : InImage._exif_format(data, Base.Make, lambda val: val, 'Unknown'),
            Base.Model            : InImage._exif_format(data, Base.Model, lambda val: val, 'Unknown'),
            Base.LensModel        : InImage._exif_format(data, Base.LensModel, lambda val: val, 'Unknown'),
            Base.FocalLength      : InImage._exif_format(data, Base.FocalLength, lambda val: f'{InImage._to_int(val)}mm', '-mm'),
            Base.ExposureTime     : InImage._exif_format(data, Base.ExposureTime, lambda val: f'{val if val >= 1 else val.real.__str__()}s', '1/-s'),
            Base.FNumber          : InImage._exif_format(data, Base.FNumber, lambda val: f'f/{InImage._to_int(val)}', 'f/-'),
            Base.ISOSpeedRatings  : InImage._exif_format(data, Base.ISOSpeedRatings, lambda val: f'ISO{val}', 'ISO-'),
            Base.DateTimeOriginal : InImage._exif_format(data, Base.DateTimeOriginal, lambda val: datetime.strptime(val, "%Y:%m:%d %H:%M:%S").__str__(), '-/-/- -:-:-'),
        }
    
    @staticmethod
    def _to_int(value):
        if value.denominator == 1:
            return value.numerator
        return value
    
    @staticmethod
    def _exif_format(data, key, formatfunc, default):
        if data == None:
            return default
        value = data.get(key, None)
        return formatfunc(value) if value != None else default
    
    def info(self, fstr: str = "* xx. {} @0000×0000 *") -> AnsiStream:
        return fomit_path(fstr, self._path) + \
               AnsiStr(f' @{self._width}×{self._height}', FORMAT_ANNO)

class OutImage:
    def __init__(self, image: Image.Image, src: InImage = None):
        self._image  = image
        self._width  = image.width
        self._height = image.height
        self._dir    = None
        self._name   = None
        if isinstance(src, InImage):
            self._dir  = src._dir
            self._name = src._name
    
    @property
    def image(self):
        return self._image
    
    @property
    def dir(self):
        return self._dir
    
    @property
    def name(self):
        return self._name
    
    def convert(self, mode: str) -> None:
        self._image = self._image.convert(mode)
    
    def formated_name(self) -> AnsiStream:
        return fomit_str('* xx. {} @0000×0000 *', self._name) + \
               AnsiStr(f' @{self._width}×{self._height}', FORMAT_ANNO)

__all__ = ["InImage", "OutImage", "IMAGE_EXTENSIONS", "IMAGE_FILETYPES"]
