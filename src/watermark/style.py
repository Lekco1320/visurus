import util

from .anchor import HorizontalAlignment, VerticalAlignment

from enum import Enum
from app  import input
from app  import resources

#region 常量

_POSITION_ANNOTATIONS = {
    'RANDOM'       : '随机位置',
    'BOTTOM_LEFT'  : '图像左下角',
    'BOTTOM_CENTER': '图像下中央',
    'BOTTOM_RIGHT' : '图像右下角',
    'CENTER_LEFT'  : '图像正左侧',
    'CENTER_CENTER': '图像正中央',
    'CENTER_RIGHT' : '图像正右侧',
    'TOP_LEFT'     : '图像左上角',
    'TOP_CENTER'   : '图像上中央',
    'TOP_RIGHT'    : '图像右上角',
}

class Position(Enum):
    RANDOM        = 0
    BOTTOM_LEFT   = 1
    BOTTOM_CENTER = 2
    BOTTOM_RIGHT  = 3
    CENTER_LEFT   = 4
    CENTER_CENTER = 5
    CENTER_RIGHT  = 6
    TOP_LEFT      = 7
    TOP_CENTER    = 8
    TOP_RIGHT     = 9
    
    def __str__(self):
        return _POSITION_ANNOTATIONS[self.name]

_CONTENT_TYPE_ANNOTATIONS = {
    'TEXT' : '文字',
    'IMAGE': '图像',
}

class ContentType(Enum):
    TEXT  = 0
    IMAGE = 1
    
    def __str__(self):
        return _CONTENT_TYPE_ANNOTATIONS[self.name]

#endregion

#region 变量

class Style(util.Config):
    FIELDS = [
        util.Field('content',  ContentType.TEXT),
        util.Field('font',     resources.Font.TIMES_REGULAR),
        util.Field('color',    util.Color('#0000007F')),
        util.Field('text',     'Lekco'),
        util.Field('psource',  '无'),
        util.Field('opacity',  80),
        util.Field('aligns',   [HorizontalAlignment.LEFT, VerticalAlignment.TOP]),
        util.Field('scale',    util.AutoScalableVector2D(util.Scale(0.05), util.AutoScale())),
        util.Field('position', Position.TOP_LEFT),
        util.Field('offset',   util.ScalableVector2D(util.Scale(0.01), util.Scale(0.01)))
    ]
    
    DEFAULT = None
    
    @staticmethod
    def default() -> 'Style':
        ret = Style()
        ret.validate(Style.FIELDS)
        return ret
    
    def __init__(self) -> None:
        super().__init__('')
        self.validate(Style.FIELDS)
    
    def self_validate(self) -> bool:
        return super().validate(Style.FIELDS)
    
    def set(self):
        main(self)

Style.DEFAULT = Style.default()

#endregion

# 主函数

def main(style: Style):
    m = util.Menu('Lekco Visurus - 水印样式', 'Q')
    m.add(util.Option('W', '水印内容', lambda: w_main(style),      lambda: w_get_value(style)))
    m.add(util.Option('F', '水印字体', lambda: f_main(style),      lambda: f_value(style),     lambda: style.content == ContentType.TEXT))
    m.add(util.Option('C', '文字颜色', lambda: set_color(style),   lambda: get_color(style),   lambda: style.content == ContentType.TEXT))
    m.add(util.Option('T', '文字内容', lambda: set_text(style),    lambda: get_text(style),    lambda: style.content == ContentType.TEXT))
    m.add(util.Option('R', '图片源',   lambda: set_psource(style), lambda: get_psource(style), lambda: style.content == ContentType.IMAGE))
    m.add(util.Option('O', '不透明度', lambda: set_opacity(style), lambda: get_opacity(style), lambda: style.content == ContentType.IMAGE))
    m.add(util.Option('A', '对齐方式', lambda: a_main(style),      lambda: a_value(style)))
    m.add(util.Option('S', '水印尺寸', lambda: set_size(style),    lambda: get_size(style)))
    m.add(util.Option('P', '水印位置', lambda: p_main(style),      lambda: p_get_value(style)))
    m.add(util.Option('E', '位置偏移', lambda: set_offset(style),  lambda: get_offset(style)))
    m.add(util.Option('Q', '返回'))
    m.run()

#region 水印内容

def w_main(style: Style):
    m = util.Menu('Lekco Visurus - 水印内容')
    m.add(util.Option('T', '文字', lambda: w_set_value(style, ContentType.TEXT)))
    m.add(util.Option('P', '图片', lambda: w_set_value(style, ContentType.IMAGE)))
    m.add(util.Option('Q', '返回'))
    m.run()

def w_set_value(style: Style, type: ContentType):
    style.content = type

def w_get_value(style: Style) -> str:
    return style.content.__str__()

#endregion

#region 水印字体

@util.errhandler
def f_main(style: Style):
    style.font = resources.font_main(style.font)

def f_value(style: Style) -> str:
    return util.fomit_path('* F | 水印字体: {} *', resources.font_name(style.font))

#endregion

#region 文字颜色

@util.errhandler
def set_color(style: Style):
    style.color = input.input_color()

def get_color(style: Style) -> str:
    return style.color.hex

#endregion

#region 文字内容

def set_text(style: Style):
    util.print_output('请输入水印内容:')
    style.text = util.get_input()

def get_text(style: Style) -> str:
    return util.fomit_str('* T | 水印内容: {} *', style.text)

#endregion

#region 图片源

@util.errhandler
def set_psource(style: Style):
    util.print_output('请输入图片源路径:')
    ans = input.select_files(util.IMAGE_EXTENSIONS, util.IMAGE_FILETYPES)
    if len(ans) > 0:
        style.psource = ans[0]

def get_psource(style: Style) -> str:
    return util.fomit_path('* S | 图片源: {} *', style.psource)

#endregion

#region 不透明度

@util.errhandler
def set_opacity(style: Style):
    util.print_output('请输入不透明度(%):')
    style.opacity = input.input_number(validation=lambda x: 0 <= x <= 100)

def get_opacity(style: Style) -> str:
    return f'{style.opacity}%'

#endregion

#region 对齐方式

def a_main(style: Style):
    m = util.Menu('Lekco Visurus - 对齐方式', 'Q')
    m.add(util.Option('H', '水平对齐', lambda: a_set_hailgn(style), lambda: a_get_halign(style)))
    m.add(util.Option('V', '垂直对齐', lambda: a_set_vailgn(style), lambda: a_get_valign(style)))
    m.add(util.Option('Q', '返回'))
    m.run()

def a_set_hailgn(style: Style):
    m = util.Menu('Lekco Visurus - 水平对齐')
    m.add(util.Option('L', '左对齐',   lambda: a_set_halign(style, HorizontalAlignment.LEFT)))
    m.add(util.Option('C', '居中对齐', lambda: a_set_halign(style, HorizontalAlignment.CENTER)))
    m.add(util.Option('R', '右对齐',   lambda: a_set_halign(style, HorizontalAlignment.RIGHT)))
    m.add(util.Option('Q', '返回'))
    m.run()

def a_set_halign(style: Style, halign: HorizontalAlignment):
    style.aligns[0] = halign

def a_get_halign(style: Style) -> str:
    return style.aligns[0]

def a_set_vailgn(style: Style):
    m = util.Menu('Lekco Visurus - 垂直对齐')
    m.add(util.Option('T', '顶部对齐', lambda: a_set_valign(style, VerticalAlignment.TOP)))
    m.add(util.Option('C', '居中对齐', lambda: a_set_valign(style, VerticalAlignment.CENTER)))
    m.add(util.Option('B', '底部对齐', lambda: a_set_valign(style, VerticalAlignment.BOTTOM)))
    m.add(util.Option('Q', '返回'))
    m.run()

def a_set_valign(style: Style, valign: VerticalAlignment):
    style.aligns[0] = valign

def a_get_valign(style: Style) -> str:
    return style.aligns[1]

def a_value(style: Style) -> str:
    return f'{style.aligns[0]}, {style.aligns[1]}'

#endregion

#region 缩放方式

@util.errhandler
def set_size(style: Style):
    util.print_output('请输入尺寸大小(w, h):')
    util.print_ps('使用\'*\'标记图像尺寸分量')
    vector = input.input_auto_scalable_vector2d()
    if style.content == ContentType.TEXT and not (
           (vector.x_number() or vector.x_scalable()) and vector.y_auto() or
           (vector.y_number() or vector.y_scalable()) and vector.x_auto()
        ):
        raise ValueError('文字水印的尺寸必须以值或比例指定长或宽.')
    style.scale = vector

def get_size(style: Style) -> str:
    size = style.scale
    return f'{size.x}×{size.y}'

#endregion

#region 水印位置

def p_main(style: Style):
    m = util.Menu('Lekco Visurus - 水印位置')
    m.add(util.Option('1', '图像左下角', lambda: p_set_value(style, Position.BOTTOM_LEFT)))
    m.add(util.Option('2', '图像下中央', lambda: p_set_value(style, Position.BOTTOM_CENTER)))
    m.add(util.Option('3', '图像右下角', lambda: p_set_value(style, Position.BOTTOM_RIGHT)))
    m.add(util.Option('4', '图像正左侧', lambda: p_set_value(style, Position.CENTER_LEFT)))
    m.add(util.Option('5', '图像正中央', lambda: p_set_value(style, Position.CENTER_CENTER)))
    m.add(util.Option('6', '图像正右侧', lambda: p_set_value(style, Position.CENTER_RIGHT)))
    m.add(util.Option('7', '图像左上角', lambda: p_set_value(style, Position.TOP_LEFT)))
    m.add(util.Option('8', '图像上中央', lambda: p_set_value(style, Position.TOP_CENTER)))
    m.add(util.Option('9', '图像右上角', lambda: p_set_value(style, Position.TOP_RIGHT)))
    m.add(util.Option('R', '随机位置',   lambda: p_set_value(style, Position.RANDOM)))
    m.add(util.Option('Q', '返回'))
    m.run()

def p_set_value(style: Style, value: Position):
    style.position = value

def p_get_value(style: Style) -> str:
    return style.position.__str__()

#endregion

#region 位置偏移

@util.errhandler
def set_offset(style: Style):
    util.print_output('请输入位置偏移(x, y):')
    style.offset = input.input_scalable_vector2d(validation=None)

def get_offset(style: Style) -> str:
    return style.offset.__str__()

#endregion
