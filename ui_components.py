# ui_components.py
from PySide6.QtCore import QSize
from PySide6.QtGui import QIcon, QPixmap, Qt
from PySide6.QtWidgets import QWidget, QHBoxLayout, QPushButton

from resource import ICON_PATH_DEFAULT, ICON_PATH_CHECKED


def create_bottom_bar(parent):
    """
    创建底部工具栏
    """
    bottom_bar = QWidget()
    bottom_bar.setFixedHeight(45)
    bottom_bar.setStyleSheet("background-color: #ece4d7; border-top: 1px solid #d4cbb8;")

    bottom_layout = QHBoxLayout(bottom_bar)
    bottom_layout.setContentsMargins(10, 5, 10, 5)

    # 置顶按钮
    parent.pin_button = QPushButton()
    parent.pin_button.setCheckable(True)
    parent.pin_button.clicked.connect(parent.toggle_pin)
    parent.pin_button.setFixedSize(35, 35)
    parent.pin_button.setToolTip("置顶/取消置顶便签(Ctrl+T)")

    # 创建图标对象，使用 resource_path 获取正确路径
    pin_icon_default = QIcon(QPixmap(ICON_PATH_DEFAULT))
    parent.pin_button.setIcon(pin_icon_default)
    parent.pin_button.setIconSize(QSize(20, 20))

    # 使用样式表来控制图标和背景颜色
    parent.pin_button.setStyleSheet(f"""
    QPushButton {{
        border: none;
        border-radius: 17px;
        background-color: transparent;

    }}
    QPushButton:hover {{
        background-color: #dcd4c7;
    }}
    QPushButton:checked {{
        background-color: #transparent;

    }}
    QPushButton:checked:hover {{
        background-color: #dcd4c7;
    }}
    """)

    # 字体缩小按钮
    parent.font_down_button = QPushButton("-")
    parent.font_down_button.setFixedSize(28, 28)
    parent.font_down_button.clicked.connect(parent.decrease_font_size)
    parent.font_down_button.setToolTip("缩小字体 (Ctrl+'-')/(鼠标滚轮+Ctrl)")
    parent.font_down_button.setStyleSheet("""
        QPushButton {
            border: none;
            border-radius: 14px;
            font-size: 18px;
            padding: -2px 0px 0px 0px;
            text-align: center;
        }
        QPushButton:hover {
            background-color: #dcd4c7;
        }
        QPushButton:pressed {
            background-color: #c4c1af;
        }
    """)

    # 字体放大按钮
    parent.font_up_button = QPushButton("+")
    parent.font_up_button.setFixedSize(28, 28)
    parent.font_up_button.clicked.connect(parent.increase_font_size)
    parent.font_up_button.setToolTip("放大字体 (Ctrl+'+')/(鼠标滚轮+Ctrl)")
    parent.font_up_button.setStyleSheet("""
        QPushButton {
            border: none;
            border-radius: 14px;
            font-size: 18px;
            padding: -2px 0px 0px 0px;
            text-align: center;
        }
        QPushButton:hover {
            background-color: #dcd4c7;
        }
        QPushButton:pressed {
            background-color: #c4c1af;
        }
    """)

    # 将按钮添加到布局中，并让它们靠左
    bottom_layout.addWidget(parent.pin_button)
    bottom_layout.addWidget(parent.font_down_button)
    bottom_layout.addWidget(parent.font_up_button)
    bottom_layout.addStretch()

    return bottom_bar
def toggle_pin(parent):
    parent.is_pinned = not parent.is_pinned
    parent.pin_button.setChecked(parent.is_pinned)  # 确保按钮状态与逻辑同步

    # 动态切换图标
    if parent.is_pinned:
        parent.pin_button.setIcon(QIcon(QPixmap(ICON_PATH_CHECKED)))
    else:
        parent.pin_button.setIcon(QIcon(QPixmap(ICON_PATH_DEFAULT)))

    # 尝试使用 win32 模块进行置顶，效果更稳定
    try:
        import win32gui
        import win32con
        hwnd = int(parent.winId())

        if parent.is_pinned:
            win32gui.SetWindowPos(hwnd, win32con.HWND_TOPMOST, 0, 0, 0, 0,
                                  win32con.SWP_NOMOVE | win32con.SWP_NOSIZE | win32con.SWP_NOACTIVATE)
        else:
            win32gui.SetWindowPos(hwnd, win32con.HWND_NOTOPMOST, 0, 0, 0, 0,
                                  win32con.SWP_NOMOVE | win32con.SWP_NOSIZE | win32con.SWP_NOACTIVATE)
    except ImportError:
        # 如果无法导入 win32 模块（例如在非 Windows 系统上），则使用 Qt 原生方法
        flags = parent.windowFlags()
        if parent.is_pinned:
            parent.setWindowFlags(flags | Qt.WindowType.WindowStaysOnTopHint)
        else:
            parent.setWindowFlags(flags & ~Qt.WindowType.WindowStaysOnTopHint)

        # 重新显示窗口以应用标志
        parent.show()