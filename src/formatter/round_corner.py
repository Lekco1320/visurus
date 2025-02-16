import util

from app import input
from PIL import Image
from PIL import ImageDraw

class Style(util.Config):
    FIELDS = [
        util.Field('radius', 10),
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
    m = util.Menu('Lekco Visurus - 圆角效果', 'Q')
    m.add(util.Option('R', '圆角半径', lambda: set_radius(style), lambda: get_radius(style)))
    m.add(util.Option('Q', '返回'))

@util.errhandler
def set_radius(style: Style):
    util.print_output('请输入圆角半径:')
    value = input.input_number(validation=lambda x: x >= 0)
    style.radius = value

def get_radius(style: Style) -> str:
    return f'{style.radius}px'

# https://www.pyget.cn/p/185266
def process(style: Style, image: Image.Image) -> Image.Image: 
    radii = style.radius
    circle = Image.new('L', (radii * 2, radii * 2), 0)
    draw = ImageDraw.Draw(circle)
    draw.ellipse((0, 0, radii * 2, radii * 2), fill=255)

    w, h = image.size

    alpha = Image.new('L', image.size, 255)
    alpha.paste(circle.crop((0, 0, radii, radii)), (0, 0))
    alpha.paste(circle.crop((radii, 0, radii * 2, radii)), (w - radii, 0))
    alpha.paste(circle.crop((radii, radii, radii * 2, radii * 2)), (w - radii, h - radii))
    alpha.paste(circle.crop((0, radii, radii, radii * 2)), (0, h - radii))

    image.putalpha(alpha)
    return image
