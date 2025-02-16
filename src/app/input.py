import os
import util

from typing import Callable

def input_color() -> util.Color:
    util.print_output('请任选一种格式输入颜色值:')
    util.print_ps('分量格式: 255,255,255')
    util.print_ps('十六进制格式: #FFFFFF')
    ans = util.get_input().strip()
    c   = ans if ans.startswith('#') else tuple(map(int, ans.split(',')))
    c   = util.Color(c)
    util.print_output('请任选一种格式输入不透明度:')
    util.print_ps('百分比格式: 100%')
    util.print_ps('十进制格式: 255')
    util.print_ps('十六进制格式: #FF')
    ans = util.get_input().strip()
    if   ans.endswith('%'):
        opc = int(ans[:-1]) / 100 * 255
    elif ans.startswith('#'):
        opc = int(ans[1:], 16)
    else:
        opc = int(ans)
    if opc < 0 or opc > 255:
        raise ValueError(f'非法不透明度值: \'{ans}\'.')
    c._a = int(opc)
    return c

def input_number(type: type = int, validation: Callable[[util.Number], bool] = None) -> util.Number:
    value = type(util.get_input())
    if isinstance(validation, Callable) and not validation(value):
        raise ValueError(f'非法的整数值: {value}.')
    return value

def input_vector2d(type: type = int, validation: Callable[[util.Number, util.Number], bool] = None) -> util.Vector2D:
    ans = list(map(type, util.get_input().strip(' ()').split(',')))
    if len(ans) != 2 or isinstance(validation, Callable) and not validation(ans[0], ans[1]):
        raise ValueError(f'非法的值: \'{ans}\'.')
    return util.Vector2D(ans[0], ans[1])

def scalable_vector2d_validation(x: util.NumberOrScale, y: util.NumberOrScale) -> bool:
    return isinstance(x, (int, float)) and x > 0 or \
           isinstance(y, (int, float)) and y > 0 or \
           isinstance(x, (util.Scale, util.AutoScale)) and isinstance(y, (util.Scale, util.AutoScale))

def input_scalable_vector2d(
    type: type = int,
    validation: Callable[[util.NumberOrScale, util.NumberOrScale], bool] = scalable_vector2d_validation
) -> util.ScalableVector2D:
    ans = list(map(str, util.get_input().strip(' ()').split(',')))
    for i in range(len(ans)):
        ans[i] = ans[i].strip()
        if ans[i].endswith('*'):
            ans[i] = util.Scale(float(ans[i][:-1]))
        else:
            ans[i] = type(ans[i])
    if len(ans) != 2 or isinstance(validation, Callable) and not validation(ans[0], ans[1]):
        raise ValueError(f'非法的值: \'{ans}\'.')
    return util.ScalableVector2D(ans[0], ans[1])

def input_auto_scalable_vector2d(
    type: type = int,
    validation: Callable[[util.NumberOrAutoScale, util.NumberOrAutoScale], bool] = scalable_vector2d_validation
) -> util.AutoScalableVector2D:
    ans = list(map(str, util.get_input().strip(' ()').split(',')))
    for i in range(len(ans)):
        ans[i] = ans[i].strip()
        if   ans[i].lower() == 'auto':
            ans[i] = util.AutoScale()
        elif ans[i].endswith('*'):
            ans[i] = util.Scale(float(ans[i][:-1]))
        else:
            ans[i] = type(ans[i])
    if len(ans) != 2 or isinstance(validation, Callable) and not validation(ans[0], ans[1]):
        raise ValueError(f'非法的值: \'{ans}\'.')
    return util.AutoScalableVector2D(ans[0], ans[1])

def input_valid_sequence(source: list[str]) -> tuple[str]:
    ans = util.get_input().strip().split()
    add = set()
    for effect in ans:
        if effect not in source:
            raise ValueError(f'非法的输入值: \'{effect}\'.')
        add.add(effect)
    if len(add) != len(source):
        raise ValueError('错误的输入值分量: 缺少值或值重复.')
    return tuple(ans)

@util.errhandler
def select_files(exts: list[str], types: list[tuple[str, str]], multiple: bool = False) -> list[str]:
    ret: list[str] = []
    m = util.Menu('Lekco Visurus - 选择文件')
    m.add(util.Option('F', '输入文件路径',       lambda: input_file(exts, ret)))
    if multiple:
        m.add(util.Option('P', '输入文件夹路径', lambda: input_folder(exts, ret)))
    m.add(util.Option('D', '对话框选择',         lambda: input_dialog(types, multiple, ret)))
    m.add(util.Option('Q', '返回'))
    m.run()
    return ret

def check_extension(path: str, exts: list[str]) -> bool:
    _, extension = os.path.splitext(path)
    return extension.lower() in exts

def check_path(path: str) -> tuple[str, bool]:
    path = path.strip('" \n\t')
    return (path, os.path.exists(path))

def get_folder_files(path: str, recursive: bool) -> list[str]:
    ret = []
    if recursive:
        for root, dirs, files in os.walk(path):
            for file in files:
                file_path = os.path.join(root, file)
                ret.append(file_path)
    else:
        with os.scandir(path) as entries:
            for entry in entries:
                if entry.is_file():
                    ret.append(entry.path)
    return ret

def input_file(exts: list[str], result: list[str]):
    util.print_output('请输入文件路径:')
    path, exist = check_path(util.get_input())
    if not exist:
        raise FileExistsError(f'文件\'{path}\'不存在.')
    if check_extension(path, exts):
        result.append(path)

def input_folder(exts: list[str], result: list[str]):
    util.print_output('请输入文件夹路径:')
    path, exist = check_path(util.get_input())
    if not exist:
        raise FileExistsError(f'文件夹\'{path}\'不存在.')
    input     = util.get_input('是否包含子文件夹？是/[否] ')
    recursive = input.strip().upper() == '是'
    files     = get_folder_files(path, recursive)
    for file in files:
        if check_extension(file, exts):
            result.append(file)

def input_dialog(types: list[tuple[str, str]], multiple: bool, result: list[str]):
    util.print_output('已启动文件选择器.')
    from tkinter import filedialog
    delegate  = filedialog.askopenfilenames if multiple else filedialog.askopenfilename
    filetypes = types
    selected  = delegate(title='选择文件', filetypes=filetypes)
    if isinstance(selected, tuple):
        for name in selected:
            if os.path.isfile(name):
                result.append(name)
    elif isinstance(selected, str) and os.path.isfile(selected):
        result.append(selected)
