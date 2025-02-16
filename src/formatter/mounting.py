import util

from app import input
from app import output
from app import workspace
from app import appconfig

from PIL import Image

from . import effects_option

targets: list[util.InImage] = []

CONFIG = appconfig.get('mounting', [
    util.Field('width',  0.05),
    util.Field('height', 0.03),
    util.Field('color',  util.Color('#FFFFFFFF')),
    util.Field('estyle', effects_option.Style('图像装裱'))
])

@util.errhandler
def main():
    m = util.Menu('Lekco Visurus - 图像装裱', 'Q')
    m.add(util.Display(display))
    m.add(util.Splitter('- 装裱参数 -'))
    m.add(util.Option('W', '边距宽度', lambda: margin_main('width'),  lambda: margin_value('width')))
    m.add(util.Option('H', '边距高度', lambda: margin_main('height'), lambda: margin_value('height')))
    m.add(util.Option('B', '裱褙颜色',    set_color, get_color))
    m.add(util.Option('E', '效果与水印…', CONFIG.estyle.set))
    m.add(util.Option('Y', '保存当前设置', lambda: appconfig.save(CONFIG)))
    m.add(util.Splitter('- 导入与导出 -'))
    m.add(util.Option('C', '选择目标图像…', choose_targets))
    m.add(util.Option('O', '执行导出…', execute))
    m.add(util.Option('Q', '返回'))
    m.run()

def choose_targets():
    global targets
    targets = workspace.c_main()

def display():
    util.print_left(f'已选择 {len(targets)} 张目标图像:')
    for i in range(len(targets)):
        util.print_left(f'{i + 1}. ' + targets[i].info())
    util.print_splitter()

def margin_main(attrname: str):
    m = util.Menu('Lekco Visurus - 边距尺寸')
    m.add(util.Option('F', '固定尺寸', lambda: margin_fixed(attrname)))
    m.add(util.Option('S', '指定比例', lambda: margin_propotion(attrname)))
    m.add(util.Option('Q', '返回'))
    m.run()

@util.errhandler
def margin_fixed(attrname: str):
    util.print_output('请输入尺寸值(>0):')
    value = input.input_number(validation=lambda x: x > 0)
    setattr(CONFIG, attrname, value)

@util.errhandler
def margin_propotion(attrname: str):
    util.print_output('请输入比例(%):')
    value = input.input_number(validation=lambda x: x > 0)
    setattr(CONFIG, attrname, value)

def margin_value(attrname: str):
    attr = getattr(CONFIG, attrname)
    if isinstance(attr, int):
        return attr
    else:
        return f'{attr * 100}%'

def set_color():
    CONFIG.color = input.input_color()

def get_color() -> str:
    return CONFIG.color.hex

@util.errhandler
def execute():
    if len(targets) <= 0:
        raise ValueError('目标图像为空.')
    
    out = []
    for srcimg in targets:
        result = CONFIG.estyle.process(process, srcimg.image)
        out.append(util.OutImage(result, srcimg))
    if len(out) > 0:
        output.main(out)

@util.errhandler
def process(image: Image.Image) -> Image.Image:
    width  = image.width
    height = image.height
    x, y   = 0, 0
    if isinstance(CONFIG.width, int):
        x      = CONFIG.width
        width += x * 2
    else:
        x      = int(CONFIG.width * image.width)
        width += x * 2
    if isinstance(CONFIG.height, int):
        y       = CONFIG.height
        height += y * 2
    else:
        y       = int(CONFIG.height * image.height)
        height += y * 2
    result = Image.new('RGBA', (width, height), CONFIG.color.hex)
    result.paste(image, (x, y), image)
    return result
