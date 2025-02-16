import util
import random

from .anchor import *
from .mark   import *
from .style  import Position, ContentType, Style

from app import output
from app import workspace
from app import resources
from app import appconfig

from PIL import Image

targets = []

CONFIG  = appconfig.get('watermark', [
    util.Field('style', Style.DEFAULT)
])

#region 主函数

def main_menu():
    m = util.Menu('Lekco Visurus - 添加水印', 'Q')
    m.add(util.Display(display))
    m.add(util.Option('C', '选择目标图像…', choose_targets))
    m.add(util.Option('S', '水印样式…',     CONFIG.style.set))
    m.add(util.Option('Y', '保存当前设置',  lambda: appconfig.save(CONFIG)))
    m.add(util.Option('O', '执行导出…',     execute))
    m.add(util.Option('Q', '返回'))
    m.run()

def display():
    util.print_left(f'已选择 {len(targets)} 张目标图像:')
    for i in range(len(targets)):
        util.print_left(f'{i + 1}. ' + targets[i].info())
    util.print_splitter()

#endregion

# 选择图片对象

def choose_targets():
    global targets
    targets = workspace.c_main()

#region 图像处理

def get_position(style: Style, size: tuple[int, int], offset: ScalableVector2D) -> util.Vector2D:
    key = style.position
    pos = None
    if   key == Position.RANDOM:
        pos = util.Vector2D(random.randint(0, size[0]), random.randint(0, size[1]))
    elif key == Position.TOP_LEFT:
        pos = util.Vector2D(0, 0)
    elif key == Position.TOP_CENTER:
        pos = util.Vector2D(int(size[0] / 2), 0)
    elif key == Position.TOP_RIGHT:
        pos = util.Vector2D(size[0], 0)
    elif key == Position.CENTER_LEFT:
        pos = util.Vector2D(0, int(size[1] / 2))
    elif key == Position.CENTER_CENTER:
        pos = util.Vector2D(int(size[0] / 2), int(size[1] / 2))
    elif key == Position.CENTER_RIGHT:
        pos = util.Vector2D(size[0], int(size[1] / 2))
    elif key == Position.BOTTOM_LEFT:
        pos = util.Vector2D(0, size[1])
    elif key == Position.BOTTOM_CENTER:
        pos = util.Vector2D(int(size[0] / 2), size[1])
    elif key == Position.BOTTOM_RIGHT:
        pos = util.Vector2D(size[0], size[1])
    pos += offset.scale(size)
    return pos

def get_anchor(style: Style, position: util.Vector2D) -> Anchor:
    return Anchor(position, style.offset, style.aligns[0], style.aligns[1])

def get_mark(style: Style, anchor: Anchor, scaler: util.AutoScalableVector2D) -> MarkBase:
    if style.content == ContentType.TEXT:
        return LabelMark(anchor, scaler, resources.get(style.font), style.color, style.text)
    else:
        return ImageMark(anchor, scaler, style.psource, style.opacity)

def process(style: Style, img: Image.Image) -> Image.Image:
    position = get_position(style, img.size, style.offset)
    anchor   = get_anchor(style, position)
    mark     = get_mark(style, anchor, style.scale)
    return mark.mark(img)

@util.errhandler
def execute():
    if len(targets) <= 0:
        raise ValueError('目标图像为空.')
    
    out = []
    for srcimg in targets:
        util.print_output(f'正在处理 {srcimg.name}...')
        processed = process(CONFIG.style, srcimg.image)
        out.append(util.OutImage(processed, srcimg))
    
    if len(out) > 0:
        output.main(out)

#endregion
