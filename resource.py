import os
import sys

def resource_path(relative_path):
    """获取资源文件的绝对路径"""
    try:
        # PyInstaller创建的临时文件夹
        base_path = getattr(sys, '_MEIPASS', os.path.abspath(""))  # noqa
    except AttributeError:
        base_path = os.path.abspath("")

    return os.path.join(base_path, relative_path)


# 使用 resource_path 函数获取图标路径
ICON_PATH_DEFAULT = resource_path("resources/setTop_default.svg")
ICON_PATH_CHECKED = resource_path("resources/setTop_checked.svg")