import util

from app import input
from app import output
from app import workspace
from app import appconfig
from app import resources
from app import console

from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
from PIL import ImageFilter
from PIL import ImageEnhance

from PIL.ExifTags import Base

from . import effects_option

#region 变量

CONFIG = appconfig.get('photo_params', [
    util.Field('size',          '4K'),
    util.Field('estyle',        effects_option.Style('标注参数')),
    util.Field('typeset',       '底部双侧标注'),
    util.Field('bottom_side',   ['{B}', '{D}', '{L} {F} {E} {I}', '{T}']),
    util.Field('bottom_center', ['Shot on ', '{D} ', '{M} ', '{L} {F} {E} {I}']),
    util.Field('back_blur',     ['{D}', '{L} {F} {E} {I}', 50, 0.45]),
])

targets: list[util.InImage] = []
out: list[util.OutImage]    = []

width = { '1080P' : 1920, '2K' : 2560, '4K' : 3840 }
info  = None

#endregion

#region 主函数

@util.errhandler
def main():
    global targets, out
    targets.clear()
    out.clear()
    targets = workspace.c_main()
    if len(targets) == 0:
        raise ValueError('目标图像为空.')
    for image in targets:
        single_main(image)
    if len(out) > 0:
        output.main(out)

def single_main(image: util.InImage):
    global info
    info = image.exif
    
    m = util.Menu('Lekco Visurus - 拍摄参数', 'X')
    m.add(util.Display(lambda: display(image)))
    m.add(util.Splitter('- 拍摄参数 -'))
    m.add(util.Option('M', '相机制造商', set_make,          get_make))
    m.add(util.Option('D', '相机型号',   set_model,         get_model))
    m.add(util.Option('B', '镜头型号',   set_lens_model,    get_lens_model))
    m.add(util.Option('L', '焦距',       set_focal_len,     get_focal_len))
    m.add(util.Option('E', '曝光时间',   set_exposure_time, get_exposure_time))
    m.add(util.Option('F', '光圈值',     set_fnumber,       get_fnumber))
    m.add(util.Option('I', 'ISO值',      set_iso,           get_iso))
    m.add(util.Option('T', '拍摄时间',   set_datetime,      get_datetime))
    m.add(util.Splitter('- 排版设置 -'))
    m.add(util.Option('P', '排版样式',   p_main, p_value))
    m.add(util.Option('C', '排版参数…',  bottom_side_main,   enfunc=lambda: CONFIG.typeset == '底部双侧标注'))
    m.add(util.Option('C', '排版参数…',  bottom_center_main, enfunc=lambda: CONFIG.typeset == '底部中央标注'))
    m.add(util.Option('C', '排版参数…',  blur_main,          enfunc=lambda: CONFIG.typeset == '背景模糊标注'))
    m.add(util.Option('S', '图像尺寸',   s_main,             s_value))
    m.add(util.Option('H', '效果与水印…',  CONFIG.estyle.set))
    m.add(util.Option('Y', '保存当前设置', lambda: appconfig.save(CONFIG)))
    m.add(util.Splitter('- 导出 -'))
    m.add(util.Option('V', '查看原图', lambda: workspace.image_window(image.image, image.name)))
    m.add(util.Option('O', '完成设置', lambda: execute(image, m)))
    m.add(util.Option('X', '放弃'))
    m.run()

def display(image: util.InImage):
    util.print_left('当前图像: ' + image.info('* 当前图像: {} @0000×0000 *'))
    util.print_splitter()

#endregion

#region 拍摄参数

@console.history('photo_params.make')
def set_make():
    util.print_output('请输入相机制造商:')
    info[Base.Make] = util.get_input()

def get_make() -> str:
    return info[Base.Make]

@console.history('photo_params.model')
def set_model():
    util.print_output('请输入相机型号:')
    info[Base.Model] = util.get_input()

def get_model() -> str:
    return info[Base.Model]

@console.history('photo_params.lens_model')
def set_lens_model():
    util.print_output('请输入镜头型号:')
    info[Base.LensModel] = util.get_input()

def get_lens_model() -> str:
    return info[Base.LensModel]

@console.history('photo_params.focal_length')
def set_focal_len():
    util.print_output('请输入焦距:')
    info[Base.FocalLength] = util.get_input()

def get_focal_len() -> str:
    return info[Base.FocalLength]

@console.history('photo_params.exposure_time')
def set_exposure_time():
    util.print_output('请输入曝光时间:')
    info[Base.ExposureTime] = util.get_input()

def get_exposure_time() -> str:
    return info[Base.ExposureTime]

@console.history('photo_params.fnumber')
def set_fnumber():
    util.print_output('请输入光圈值:')
    info[Base.FNumber] = util.get_input()

def get_fnumber() -> str:
    return info[Base.FNumber]

@console.history('photo_params.iso')
def set_iso():
    util.print_output('请输入ISO值:')
    info[Base.ISOSpeedRatings] = util.get_input()

def get_iso() -> str:
    return info[Base.ISOSpeedRatings]

def set_datetime():
    util.print_output('请输入拍摄时间:')
    info[Base.DateTimeOriginal] = util.get_input()

def get_datetime() -> str:
    return info[Base.DateTimeOriginal]

#endregion

#region 图像尺寸

def s_main():
    m = util.Menu('Lekco Visurus - 图像尺寸')
    m.add(util.Option('1', '1080P', s_1080P))
    m.add(util.Option('2', '2K',    s_2K))
    m.add(util.Option('3', '4K',    s_4K))
    m.add(util.Option('4', '自适应', s_fit))
    m.add(util.Option('Q', '退出'))
    m.run()

def s_1080P():
    CONFIG.size = '1080P'

def s_2K():
    CONFIG.size = '2K'

def s_4K():
    CONFIG.size = '4K'

def s_fit():
    CONFIG.size = '自适应'

def s_value() -> str:
    return CONFIG.size

#endregion

#region 排版模式

def p_main():
    m = util.Menu('Lekco Visurus - 排版样式')
    m.add(util.Option('S', '底部两侧标注', p_bottom_side))
    m.add(util.Option('C', '底部中央标注', p_bottom_center))
    m.add(util.Option('B', '背景模糊标注', p_blur))
    m.add(util.Option('Q', '返回'))
    m.run()

def p_bottom_side():
    CONFIG.typeset = '底部双侧标注'

def p_bottom_center():
    CONFIG.typeset = '底部中央标注'

def p_blur():
    CONFIG.typeset = '背景模糊标注'

def p_value() -> str:
    return CONFIG.typeset

#endregion

#region 排版参数

def param_display():
    util.print_left('下列参数以给定占位符表示:')
    colored = lambda c: util.AnsiStr(c, util.FORMAT_VALUE)
    util.print_left(colored('{M}') + ' | 相机制造商')
    util.print_left(colored('{D}') + ' | 相机型号')
    util.print_left(colored('{B}') + ' | 镜头型号')
    util.print_left(colored('{L}') + ' | 焦距')
    util.print_left(colored('{E}') + ' | 曝光时间')
    util.print_left(colored('{F}') + ' | 光圈值')
    util.print_left(colored('{I}') + ' | ISO值')
    util.print_left(colored('{T}') + ' | 拍摄时间')
    util.print_splitter()

@util.errhandler
def set_param(attrname: str, id: int):
    util.print_output('请输入参数对应的占位符:')
    util.print_ps('请按顺序连续拼接一个或多个参数.')
    getattr(CONFIG, attrname)[id] = util.get_input()

@util.errhandler
def get_param(attrname: str, id: int):
    return getattr(CONFIG, attrname)[id]

def bottom_side_main():
    ATTRNAME = 'bottom_side'
    m = util.Menu('Lekco Visurus - 排版参数', 'Q')
    m.add(util.Display(param_display))
    m.add(util.Option('A', '左第一行', lambda: set_param(ATTRNAME, 0), lambda: get_param(ATTRNAME, 0)))
    m.add(util.Option('B', '左第二行', lambda: set_param(ATTRNAME, 1), lambda: get_param(ATTRNAME, 1)))
    m.add(util.Option('C', '右第一行', lambda: set_param(ATTRNAME, 2), lambda: get_param(ATTRNAME, 2)))
    m.add(util.Option('D', '右第二行', lambda: set_param(ATTRNAME, 3), lambda: get_param(ATTRNAME, 3)))
    m.add(util.Option('Q', '返回'))
    m.run()

def bottom_center_main():
    ATTRNAME = 'bottom_center'
    m = util.Menu('Lekco Visurus - 排版参数', 'Q')
    m.add(util.Display(param_display))
    m.add(util.Option('A', '第一行黑字', lambda: set_param(ATTRNAME, 0), lambda: get_param(ATTRNAME, 0)))
    m.add(util.Option('B', '第一行红字', lambda: set_param(ATTRNAME, 1), lambda: get_param(ATTRNAME, 1)))
    m.add(util.Option('C', '第一行粗字', lambda: set_param(ATTRNAME, 2), lambda: get_param(ATTRNAME, 2)))
    m.add(util.Option('D', '第二行',     lambda: set_param(ATTRNAME, 3), lambda: get_param(ATTRNAME, 3)))
    m.add(util.Option('Q', '返回'))
    m.run()

def blur_main():
    ATTRNAME = 'back_blur'
    m = util.Menu('Lekco Visurus - 排版参数', 'Q')
    m.add(util.Display(param_display))
    m.add(util.Option('A', '第一行文本',   lambda: set_param(ATTRNAME, 0), lambda: get_param(ATTRNAME, 0)))
    m.add(util.Option('B', '第二行文本',   lambda: set_param(ATTRNAME, 1), lambda: get_param(ATTRNAME, 1)))
    m.add(util.Option('R', '背景模糊程度', lambda: blur_set_blur,          lambda: CONFIG.back_blur[2].__str__()))
    m.add(util.Option('I', '背景亮度',     lambda: blur_set_brightness,    lambda: f'{CONFIG.back_blur[3] * 100}%'))
    m.add(util.Option('Q', '返回'))
    m.run()

@util.errhandler
def blur_set_blur():
    util.print_output('请输入模糊半径:')
    CONFIG.back_blur[2] = input.input_number(validation=lambda x: x >= 0)

@util.errhandler
def blur_set_brightness():
    util.print_output('请输入亮度(%):')
    ans = input.input_number(validation=lambda x: 0 <= x <= 100)
    CONFIG.back_blur[3] = ans / 100

#endregion

#region 图像处理

params_map = {
    'M' : Base.Make,
    'D' : Base.Model,
    'B' : Base.LensModel,
    'L' : Base.FocalLength,
    'E' : Base.ExposureTime,
    'F' : Base.FNumber,
    'I' : Base.ISOSpeedRatings,
    'T' : Base.DateTimeOriginal
}

def param_to_str(attrname: str, id: int) -> str:
    return getattr(CONFIG, attrname)[id].format_map({key : info[params_map[key]] for key in params_map.keys()})

@util.errhandler
def execute(srcimg: util.InImage, menu: util.Menu):
    img  = resize(srcimg.image)
    func = None
    if   CONFIG.typeset == '底部双侧标注':
        func = process_bottom_side
    elif CONFIG.typeset == '底部中央标注':
        func = process_bottom_center
    elif CONFIG.typeset == '背景模糊标注':
        func = process_blur
    processed = CONFIG.estyle.process(func, img)
    out.append(util.OutImage(processed, srcimg))
    menu.exit()

def resize(image: Image.Image) -> Image.Image:
    if CONFIG.size == '自适应':
        return image
    newheight = round(image.height * width[CONFIG.size] / image.width)
    return image.resize((width[CONFIG.size], newheight))

def process_bottom_side(image: Image.Image) -> Image.Image:
    width, height = image.size
    margin = round(width * 200 / 8250)
    bottom = round(height * 650 / 5500)
    bmar1  = round(bottom * 135 / 660)
    bmar2  = round(bottom * 55  / 660)
    font   = round(bottom * 140 / 660)
    offy   = margin + height + bmar1
    
    final  = Image.new('RGBA', (width + margin * 2, height + margin + bottom), (255, 255, 255))
    final.paste(image, (margin, margin), image)
    
    light = ImageFont.truetype(resources.get(resources.Font.PUHUI_LIGHT), font)
    bold  = ImageFont.truetype(resources.get(resources.Font.PUHUI_BOLD), font)
    draw  = ImageDraw.Draw(final)
    sget  = lambda id: param_to_str('bottom_side', id)
    
    draw.text((margin, offy), sget(0), (0, 0, 0), bold)
    draw.text((margin, offy + font + bmar2), sget(1), (50, 50, 50), light)
    length = draw.textlength(sget(2), bold)
    draw.text((width + margin - length, offy), sget(2), (0, 0, 0), bold)
    length = draw.textlength(sget(3), light)
    draw.text((width + margin - length, offy + font + bmar2), sget(3), (50, 50, 50), light)
    
    return final

def process_bottom_center(image: Image.Image) -> Image.Image:
    width, height = image.size
    margin = round(width * 200 / 8250)
    bottom = round(height * 650 / 5500)
    bmar1  = round(bottom * 125 / 660)
    bmar2  = round(bottom * 55  / 660)
    font1  = round(bottom * 160 / 660)
    font2  = round(bottom * 135 / 660)
    offy   = margin + height + bmar1
    
    final  = Image.new('RGBA', (width + margin * 2, height + margin + bottom), (255, 255, 255))
    final.paste(image, (margin, margin), image)
    sget  = lambda id: param_to_str('bottom_center', id)
    
    light   = ImageFont.truetype(resources.get(resources.Font.PUHUI_LIGHT), font2)
    regular = ImageFont.truetype(resources.get(resources.Font.PUHUI_REGULAR), font1)
    bold    = ImageFont.truetype(resources.get(resources.Font.PUHUI_BOLD), font1)
    draw    = ImageDraw.Draw(final)
    
    len0 = draw.textlength(sget(0), regular)
    len1 = draw.textlength(sget(1), bold)
    len2 = draw.textlength(sget(2), bold)
    left = round((image.width + 2 * margin - len0 - len1 - len2) / 2)
    draw.text((left, offy), sget(0), (0, 0, 0), regular)
    draw.text((left + len0, offy), sget(1), (227, 39, 39), bold)
    draw.text((left + len0 + len1, offy), sget(2), (0, 0, 0), bold)
    
    len3  = draw.textlength(sget(3), light)
    left  = round((image.width + 2 * margin - len3) / 2)
    draw.text((left, offy + font1 + bmar2), sget(3), (50, 50, 50), light)
    
    return final

def process_blur(image: Image.Image) -> Image.Image:
    width, height = image.size
    margin = round(width * 400 / 8250)
    bottom = round(height * 650 / 5500)
    bmar1  = round(bottom * 125 / 660)
    bmar2  = round(bottom * 55  / 660)
    font1  = round(bottom * 160 / 660)
    font2  = round(bottom * 135 / 660)
    offy   = margin + height + bmar1
    
    bwidth  = round(width + 2 * margin)
    bheight = round(height + margin + bottom)
    final   = ImageEnhance.Brightness(image.copy() \
                                           .resize((bwidth, bheight)) \
                                           .filter(ImageFilter.GaussianBlur(CONFIG.back_blur[2]))) \
                                           .enhance(CONFIG.back_blur[3])
    final.paste(image, (margin, margin), image)
    sget = lambda id: param_to_str('back_blur', id)
    
    bold    = ImageFont.truetype(resources.get(resources.Font.PUHUI_BOLD), font1)
    regular = ImageFont.truetype(resources.get(resources.Font.PUHUI_REGULAR), font2)
    draw    = ImageDraw.Draw(final)
    
    len0 = draw.textlength(sget(0), bold)
    left = round((bwidth - len0) / 2)
    draw.text((left, offy), sget(0), (255, 255, 255), bold)
    len1 = draw.textlength(sget(1), regular)
    left = round((bwidth - len1) / 2)
    draw.text((left, offy + font1 + bmar2), sget(1), (255, 255, 255), regular)
    
    return final

#endregion
