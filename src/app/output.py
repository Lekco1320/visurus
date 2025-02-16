import os
import util

from app import appconfig
from app import workspace

from tkinter  import filedialog
from datetime import datetime

images: list[util.OutImage] = []
chosen: list[int]           = []

FORMAT_MAP = {
    '*.JPG': 'JPEG',
    '*.PNG': 'PNG',
    '*.BMP': 'BMP',
    '*.GIF': 'GIF',
}

CONFIG = appconfig.get('output', [
    util.Field('dir',      '桌面'),
    util.Field('format',   '*.JPG'),
    util.Field('filename', 'o_{N}{E}'),
])

def init(imgs: list[util.OutImage]):
    global images, chosen
    images = imgs
    chosen = list(range(1, len(images) + 1))

def main(imgs: list[util.OutImage]):
    init(imgs)
    
    m = util.Menu('Lekco Visurus - 导出设置', 'Q')
    m.add(util.Display(display))
    m.add(util.Splitter('- 参数 -'))
    m.add(util.Option('P', '导出内容',   p_main, p_value))
    m.add(util.Option('D', '导出路径',   d_main, d_value))
    m.add(util.Option('F', '导出格式',   f_main, f_value))
    m.add(util.Option('S', '文件名格式', n_main, n_value))
    m.add(util.Splitter('- 导出 -'))
    m.add(util.Option('V', '预览图像',   preview))
    m.add(util.Option('Y', '保存当前设置', lambda: appconfig.save(CONFIG)))
    m.add(util.Option('O', '确认并导出', output))
    m.add(util.Option('Q', '返回'))
    m.run()

def display():
    util.print_left(f'导出源含有 {len(images)} 张图像:')
    for i in range(len(images)):
        util.print_left(f'{i + 1}. ' + images[i].formated_name())
    util.print_splitter()

def check_space() -> bool:
    ret = len(images) > 0
    if not ret:
        util.print_error('[错误] 导出源为空.')
    return ret

@util.errhandler
def choose() -> list[int]:
    if not check_space():
        return
    
    while True:
        util.print_output('请选择目标图像:')
        util.print_ps('请用空格隔开多个索引')
        util.print_ps('空输入默认全选')
        ans = list(map(int, util.get_input().split()))
        if len(ans) == 0:
            util.up_line()
            util.print_output(' '.join([str(i) for i in range(1, len(images) + 1)]))
            return [i for i in range(1, len(images) + 1)]
        else:
            for i in ans:
                if i < 0 or i > len(images):
                    raise IndexError(f'\'{i}\' 超出索引范围.')
            return ans

def preview():
    if not check_space():
        return
    
    for id in choose():
        workspace.image_window(images[id - 1].image, images[id - 1].name)

def p_main():
    global chosen
    chosen = choose()

def p_value() -> str:
    return chosen.__str__()

def d_main():
    m = util.Menu('Lekco Visurus - 导出内容')
    m.add(util.Option('O', '导出至源路径', d_source))
    m.add(util.Option('D', '导出至桌面',   d_desktop))
    m.add(util.Option('F', '选择指定目录', d_disk))
    m.add(util.Option('Q', '返回'))
    m.run()

def d_source(): 
    CONFIG.dir = '源路径'

def d_desktop(): 
    CONFIG.dir = '桌面'

def d_disk():
    util.print_output('请选择目标路径:')
    CONFIG.dir = filedialog.askdirectory()

def d_value() -> str:
    return util.fomit_path('* D | 导出路径: {} *', CONFIG.dir)

def f_main():
    m = util.Menu('Lekco Visurus - 导出格式')
    m.add(util.Option('J', '*.JPG', f_jpg))
    m.add(util.Option('P', '*.PNG', f_png))
    m.add(util.Option('B', '*.BMP', f_bmp))
    m.add(util.Option('G', '*.GIF', f_gif))
    m.add(util.Option('Q', '返回'))
    m.run()

def f_jpg():
    CONFIG.format = '*.JPG'

def f_png():
    CONFIG.format = '*.PNG'

def f_bmp():
    CONFIG.format = '*.BMP'

def f_gif():
    CONFIG.format = '*.GIF'

def f_value() -> str:
    return CONFIG.format

def n_display(): 
    util.print_left('下列参数以给定占位符表示:')
    colored = lambda c: util.AnsiStr(c, util.FORMAT_VALUE)
    util.print_left(colored('{N}') + ' | 源文件名')
    util.print_left(colored('{E}') + ' | 导出格式拓展名')
    util.print_left(colored('{Y}') + ' | 导出时间:年')
    util.print_left(colored('{M}') + ' | 导出时间:月')
    util.print_left(colored('{D}') + ' | 导出时间:日')
    util.print_left(colored('{H}') + ' | 导出时间:时')
    util.print_left(colored('{m}') + ' | 导出时间:分')
    util.print_left(colored('{S}') + ' | 导出时间:秒')
    util.print_splitter()

@util.errhandler
def n_main():
    util.true_clear_screen()
    util.print_title('Lekco Visurus - 文件名格式')
    n_display()
    util.print_output('请输入参数对应的占位符:')
    util.print_ps('请按顺序连续拼接一个或多个参数.')
    CONFIG.filename = util.get_input()

def n_value(): 
    return CONFIG.filename

def validate_filename(name: str) -> bool: 
    if os.name == 'posix': 
        invalid_chars = ''
    else:
        invalid_chars = '<>:"/\\|?*'    
    return not any(char in name for char in invalid_chars)

def generate_filename(path: str) -> str: 
    name      = os.path.splitext(os.path.basename(path))[0]
    extension = CONFIG.format[1:].lower()
    time      = datetime.now()
    info      = {
        'N': name,
        'E': extension,
        'Y': time.year,
        'M': time.month,
        'D': time.day,
        'H': time.hour,
        'm': time.minute,
        'S': time.second
    }
    return CONFIG.filename.format_map({key : info[key] for key in info.keys()})

def output():
    util.print_output('正在导出图像...')
    format = FORMAT_MAP[CONFIG.format]
    for i in chosen:
        dir = CONFIG.dir
        if dir == '桌面':
            if os.name == 'posix':
                dir = os.path.join(os.path.expanduser('~'), 'Desktop')
            else: 
                dir = os.path.join(os.environ['USERPROFILE'], 'Desktop')
        elif dir == '源路径':
            dir = images[i - 1].dir
        
        name = generate_filename(images[i - 1].name)
        if not validate_filename(name): 
            raise ValueError(f'文件名\"{name}\"中含有非法字符.')
        
        path = os.path.join(dir, name)
        if format in ['JPEG', 'BMP'] and images[i - 1].image.mode == 'RGBA':
            images[i - 1].convert('RGB')
        images[i - 1].image.save(path, format)
        util.print_success(f'{name} 导出成功.')
    util.wait()
