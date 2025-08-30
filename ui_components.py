# ui_components.py
from PySide6.QtCore import QSize
from PySide6.QtGui import QIcon, QPixmap, Qt
from PySide6.QtWidgets import QWidget, QHBoxLayout, QPushButton

from resource import ICON_PATH_DEFAULT, ICON_PATH_CHECKED

# 全局变量定义
BOTTOM_BAR_HEIGHT = 45
PIN_BUTTON_SIZE = 36
PIN_BUTTON_RADIUS = PIN_BUTTON_SIZE // 2  # 整数除法避免小数, 用于计算圆角半径
PIN_ICON_SIZE = 20
FONT_BUTTON_SIZE = 28  # 字体按钮大小
FONT_BUTTON_RADIUS = FONT_BUTTON_SIZE // 2  # 字体按钮圆角半径


def create_bottom_bar(parent):
    """
    创建底部工具栏
    """
    bottom_bar = QWidget()
    bottom_bar.setFixedHeight(BOTTOM_BAR_HEIGHT)
    bottom_bar.setStyleSheet(StyleSheetManager.get_bottom_bar_style())

    bottom_layout = QHBoxLayout(bottom_bar)
    bottom_layout.setContentsMargins(10, 5, 10, 5)

    # 置顶按钮
    parent.pin_button = QPushButton()
    parent.pin_button.setCheckable(True)
    parent.pin_button.clicked.connect(parent.toggle_pin)
    parent.pin_button.setFixedSize(PIN_BUTTON_SIZE, PIN_BUTTON_SIZE)
    parent.pin_button.setToolTip("置顶/取消置顶便签(Ctrl+T)")

    # 创建图标对象，使用 resource_path 获取正确路径
    pin_icon_default = QIcon(QPixmap(ICON_PATH_DEFAULT))
    parent.pin_button.setIcon(pin_icon_default)
    parent.pin_button.setIconSize(QSize(PIN_ICON_SIZE, PIN_ICON_SIZE))

    # 使用样式表来控制图标和背景颜色
    parent.pin_button.setStyleSheet(StyleSheetManager.get_pin_button_style())

    # 字体缩小按钮
    parent.font_down_button = QPushButton("-")
    parent.font_down_button.setFixedSize(FONT_BUTTON_SIZE, FONT_BUTTON_SIZE)
    parent.font_down_button.clicked.connect(parent.decrease_font_size)
    parent.font_down_button.setToolTip("缩小字体 (Ctrl+'-')/(鼠标滚轮+Ctrl)")
    parent.font_down_button.setStyleSheet(StyleSheetManager.get_font_button_style())

    # 字体放大按钮
    parent.font_up_button = QPushButton("+")
    parent.font_up_button.setFixedSize(FONT_BUTTON_SIZE, FONT_BUTTON_SIZE)
    parent.font_up_button.clicked.connect(parent.increase_font_size)
    parent.font_up_button.setToolTip("放大字体 (Ctrl+'+')/(鼠标滚轮+Ctrl)")
    parent.font_up_button.setStyleSheet(StyleSheetManager.get_font_button_style())

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


class StyleSheetManager:
    # 底栏颜色常量
    BOTTOM_BAR_BACKGROUND_COLOR = "#ece4d7"
    BOTTOM_BAR_BORDER_COLOR = "#d4cbb8"
    # 按钮颜色常量
    BUTTON_HOVER_COLOR = "rgba(255, 255, 255, 0.4)"
    BUTTON_CHECKED_HOVER_COLOR = BUTTON_HOVER_COLOR
    BUTTON_PRESSED_COLOR = BUTTON_HOVER_COLOR
    BUTTON_BACKGROUND_COLOR = "transparent"

    @staticmethod
    def get_bottom_bar_style():
        return f"""
        background-color: {StyleSheetManager.BOTTOM_BAR_BACKGROUND_COLOR}; 
        border-top: 1px solid {StyleSheetManager.BOTTOM_BAR_BORDER_COLOR};
        """

    @staticmethod
    def get_pin_button_style():
        return f"""
        QPushButton {{
            border: none;
            border-radius: {PIN_BUTTON_RADIUS};
            background-color: {StyleSheetManager.BUTTON_BACKGROUND_COLOR};
        }}
        QPushButton:hover {{
            background-color: {StyleSheetManager.BUTTON_HOVER_COLOR};
        }}
        QPushButton:checked {{
            background-color: {StyleSheetManager.BUTTON_BACKGROUND_COLOR};
        }}
        QPushButton:checked:hover {{
            background-color: {StyleSheetManager.BUTTON_CHECKED_HOVER_COLOR};
        }}
        """

    @staticmethod
    def get_font_button_style():
        return f"""
        QPushButton {{
            border: none;
            border-radius: {FONT_BUTTON_RADIUS};
            font-size: 18px;
            padding: -2px 0px 0px 0px;
            text-align: center;
        }}
        QPushButton:hover {{
            background-color: {StyleSheetManager.BUTTON_HOVER_COLOR};
        }}
        QPushButton:pressed {{
            background-color: {StyleSheetManager.BUTTON_PRESSED_COLOR};
        }}
        """
