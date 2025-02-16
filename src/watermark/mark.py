from abc  import ABC
from abc  import abstractmethod
from PIL  import Image
from PIL  import ImageDraw
from PIL  import ImageFont
from util import Color, Vector2D, AutoScale, AutoScalableVector2D

from .anchor import Anchor

class MarkBase(ABC):
    def __init__(self, anchor: Anchor, scaler: AutoScalableVector2D) -> None:
        super().__init__()
        
        self._anchor = anchor
        self._scaler = scaler
    
    @property
    def anchor(self):
        return self._anchor
    
    @property
    def scaler(self):
        return self._scaler
    
    @abstractmethod
    def mark(self, image: Image.Image) -> Image.Image:
        pass

class ImageMark(MarkBase):
    def __init__(self, anchor: Anchor, scaler: AutoScalableVector2D, image: str, opacity: float) -> None:
        super().__init__(anchor, scaler)
        
        self._image   = image
        self._opacity = opacity
        
    @property
    def image(self):
        return self._image
    
    @property
    def opacity(self):
        return self._opacity
    
    def _scale(self, refsize: tuple[int, int]) -> Vector2D:
        with Image.open(self._image) as image:
            return self._scaler.scale(refsize, image.size)
    
    def mark(self, image: Image.Image) -> Image.Image:
        size     = self._scale(image.size)
        position = self._anchor.real_position(size)
        with Image.open(self._image).convert('RGBA') as img:
            nimg = img.resize(size)
            pale = Image.new('RGBA', nimg.size, (0, 0, 0, 0))
            aimg = Image.blend(pale, nimg, self._opacity / 100.0)
            image.paste(aimg, position, aimg)
            return image

class LabelMark(MarkBase):
    def __init__(self, anchor: Anchor, scaler: AutoScalableVector2D, font: str, color: Color, text: str) -> None:
        super().__init__(anchor, scaler)
        
        if not (
            (scaler.x_number() or scaler.x_scalable()) and scaler.y_auto() or
            (scaler.x_number() or scaler.y_scalable()) and scaler.x_auto()
        ):
            raise ValueError('文字水印的尺寸必须以值或比例指定长或宽.')
        
        self._font      = font
        self._scaler    = scaler
        self._color     = color
        self._text      = text
    
    @property
    def font(self):
        return self._font
    
    @property
    def text(self):
        return self._text
    
    @property
    def color(self):
        return self._color

    def _scale(self, refsize: tuple[int, int]) -> tuple[tuple[int, int], int]:
        scaled = super(AutoScalableVector2D, self._scaler).scale(refsize)
        width, height = scaled.x, scaled.y
        if isinstance(width, AutoScale):
            _font_size = height
            font  = ImageFont.truetype(self._font, height)
            width = font.getlength(self._text)
            _size = (width, height)
            return (_size, _font_size)
        else:
            size   = 0
            length = 0
            while length < width:
                size  += 1
                font   = ImageFont.truetype(self._font, size)
                length = font.getlength(self._text)
            return ((length, size), size)
    
    def mark(self, image: Image.Image) -> Image.Image:
        size, font_size = self._scale(image.size)
        position = self._anchor.real_position(size)
        font = ImageFont.truetype(self._font, font_size)
        text = Image.new('RGBA', image.size, (0, 0, 0, 0))
        draw = ImageDraw.Draw(text)
        draw.text(position, self._text, self._color.tuple, font)
        return Image.alpha_composite(image, text)
