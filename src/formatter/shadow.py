import util

from app import input
from PIL import Image
from PIL import ImageFilter

class Style(util.Config):
    FIELDS = [
        util.Field('color',  util.Color('#0000007F')),
        util.Field('offset', util.Vector2D(10, 10)),
        util.Field('limit',  util.Vector2D(8, 8)),
        util.Field('blur',   5),
    ]
    
    DEFAULT = None
    
    @classmethod
    def default(cls) -> 'Style':
        ret = Style()
        ret.validate(Style.FIELDS)
        return ret
    
    def __init__(self) -> None:
        super().__init__('')
        self.validate(Style.FIELDS)
    
    def self_validate(self) -> bool:
        return super().validate(Style.FIELDS)

    def set(self):
        style_main(self)

Style.DEFAULT = Style.default()

def style_main(style: Style):
    m = util.Menu('Lekco Visurus - 阴影效果', 'Q')
    m.add(util.Option('C', '阴影颜色', lambda: set_color(style),  lambda: get_color(style)))
    m.add(util.Option('O', '阴影偏移', lambda: set_offset(style), lambda: get_offset(style)))
    m.add(util.Option('L', '范围限制', lambda: set_limit(style),  lambda: get_limit(style)))
    m.add(util.Option('B', '模糊程度', lambda: set_blur(style),   lambda: get_blur(style)))
    m.add(util.Option('Q', '返回'))
    m.run()

def set_color(style: Style):
    style.color = input.input_color()

def get_color(style: Style) -> str:
    return style.color.hex

@util.errhandler
def set_offset(style: Style):
    util.print_output('请输入偏移量(x, y):')
    style.offset = input.input_vector2d()

def get_offset(style: Style) -> str:
    return style.offset.__str__()

@util.errhandler
def set_limit(style: Style):
    util.print_output('请输入范围限制(x, y):')
    style.limit = input.input_vector2d()

def get_limit(style: Style) -> str:
    return style.limit.__str__()

@util.errhandler
def set_blur(style: Style):
    util.print_output('请输入模糊程度(>=0):')
    style.blur = input.input_number(validation=lambda x: x >= 0)

def get_blur(style: Style) -> str:
    return style.blur.__str__()

def process(style: Style, image: Image.Image) -> Image.Image:
    return _blur(image, style.offset.tuple(), style.limit.tuple(), style.color, style.blur)

# https://code.activestate.com/recipes/474116-drop-shadows-with-pil/
def _blur(image: Image.Image, offset: tuple, limit: tuple, color: util.Color, depth: int) -> Image.Image:
    """
    Add a gaussian blur drop shadow to an image.
    image       - The image to overlay on top of the shadow.
    """
    # Create the backdrop image -- a box in the background colour with a shadow on it.
    totalWidth = image.width + abs(offset[0]) + 2 * limit[0]
    totalHeight = image.height + abs(offset[1]) + 2 * limit[1]
    back = Image.new("RGBA", (totalWidth, totalHeight), (0, 0, 0, 0))
    # Place the shadow, taking into account the offset from the image
    shadowLeft = limit[0] + max(offset[0], 0)
    shadowTop = limit[1] + max(offset[1], 0)
    back.paste(color.tuple, [shadowLeft, shadowTop, shadowLeft + image.width, shadowTop + image.height])
    # Apply the filter to blur the edges of the shadow.  Since a small kernel
    # is used, the filter must be applied repeatedly to get a decent blur.
    for _ in range(depth):
        back = back.filter(ImageFilter.BLUR)
    # Paste the input image onto the shadow backdrop  
    imageLeft = limit[0] - min(offset[0], 0)
    imageTop = limit[1] - min(offset[1], 0)
    back.paste(image, (imageLeft, imageTop))
    return back
