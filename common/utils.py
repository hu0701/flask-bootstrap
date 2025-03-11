# 获取文件名和扩展名，并生成唯一的保存文件路径。

from pathlib import Path


def get_file_name_parts( filename: str):
    pos = filename.rfind('.')
    if pos == -1:
        return filename, ''

    return filename[:pos], filename[pos + 1:]


def get_save_filepaths(file_path: Path, filename: str):
    save_file = file_path.joinpath(filename)
    if not save_file.exists():
        return save_file

    name, ext = get_file_name_parts(filename)
    for index in range(1, 100):
        save_file = file_path.joinpath(f'{name}{index}.{ext}')
        if not save_file.exists():
            return save_file

    return file_path.joinpath(f'{name}_override.{ext}')