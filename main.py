import sys

from PySide6.QtWidgets import QApplication, QMainWindow, QTextEdit, QPushButton, QVBoxLayout, QWidget, QSizeGrip, \
    QHBoxLayout, QMenu
from PySide6.QtCore import Qt, QPoint, QSize
from PySide6.QtGui import  QFont, QIcon

# 图标路径，确保该文件存在
ICON_PATH_DEFAULT = "resources/setTop_default.svg"
ICON_PATH_CHECKED = "resources/setTop_checked.svg"

class StickyNote(QMainWindow):
    def __init__(self):
        super().__init__()
        self.old_pos = None
        self.is_pinned = False
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint | Qt.WindowType.Tool)
        self.setWindowTitle("桌面便签")

        # 调整窗口的整体样式，使用更柔和的颜色
        self.setStyleSheet("""
            QMainWindow {
                border: 1px solid #d4cbb8;   /* 柔和的边框 */
            }
        """)
        # 初始尺寸
        self.resize(500, 400)
        self.base_size = self.size()

        # 初始字体大小
        self.current_font_size = 12

        # 创建中央 Widget 和布局
        central_widget = QWidget()
        # central_widget.setStyleSheet("""
        #         QWidget {
        #             border: 1px solid #d4cbb8;
        #             border-radius: 8px;
        #         }
        #     """)
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(1, 1, 1, 1)
        main_layout.setSpacing(0)

        # 创建文本编辑区域
        self.text_edit = QTextEdit()
        self.set_text_edit()
        main_layout.addWidget(self.text_edit)

        # 底部区域，用作拖动句柄和按钮区域
        self.bottom_bar = QWidget()
        self.bottom_bar.setFixedHeight(45)
        self.bottom_bar.setStyleSheet("background-color: #ece4d7; border-top: 1px solid #d4cbb8;")

        bottom_layout = QHBoxLayout(self.bottom_bar)
        bottom_layout.setContentsMargins(10, 5, 10, 5)

        # 置顶按钮
        self.pin_button = QPushButton()
        self.pin_button.setCheckable(True)
        self.pin_button.clicked.connect(self.toggle_pin)
        self.pin_button.setFixedSize(35, 35)
        self.pin_button.setToolTip("置顶/取消置顶便签(Ctrl+T)")

        # 创建图标对象
        pin_icon = QIcon(ICON_PATH_DEFAULT)
        self.pin_button.setIcon(pin_icon)
        self.pin_button.setIconSize(QSize(20, 20))

        # 使用样式表来控制图标和背景颜色
        self.pin_button.setStyleSheet(f"""
        QPushButton {{
            border: none;
            border-radius: 17px;
            background-color: transparent;
            icon: url({ICON_PATH_DEFAULT});
        }}
        QPushButton:hover {{
            background-color: #dcd4c7;
        }}
        QPushButton:checked {{
            background-color: #transparent;
            icon: url({ICON_PATH_CHECKED});
        }}
        QPushButton:checked:hover {{
            background-color: #dcd4c7;
        }}
        """)

        # 字体缩小按钮
        self.font_down_button = QPushButton("-")
        self.font_down_button.setFixedSize(28, 28)
        self.font_down_button.clicked.connect(self.decrease_font_size)
        self.font_down_button.setToolTip("缩小字体 (Ctrl+'-')/(鼠标滚轮+Ctrl)")
        self.font_down_button.setStyleSheet("""
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
        self.font_up_button = QPushButton("+")
        self.font_up_button.setFixedSize(28, 28)
        self.font_up_button.clicked.connect(self.increase_font_size)
        self.font_up_button.setToolTip("放大字体 (Ctrl+'+')/(鼠标滚轮+Ctrl)")
        self.font_up_button.setStyleSheet("""
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
        bottom_layout.addWidget(self.pin_button)
        bottom_layout.addWidget(self.font_down_button)
        bottom_layout.addWidget(self.font_up_button)
        bottom_layout.addStretch()

        main_layout.addWidget(self.bottom_bar)

        # 窗口尺寸调整控制点
        self.grip = QSizeGrip(self)
        self.grip.setFixedSize(30, 30)
        self.grip.move(self.width() - self.grip.width(), self.height() - self.grip.height())

        # 首次设置字体
        self.set_font_size()

    def set_text_edit(self):
        """创建并配置文本编辑区域"""
        # 文本编辑区域
        self.text_edit.setStyleSheet("""
            QTextEdit {
                border: none;
                padding: 15px;
                background-color: white;  /* 文本区域的背景颜色与主窗口保持一致 */
            }

            /* 垂直滚动条 */
            QScrollBar:vertical {
                border: none;
                background: #f0f0e0; /* 滚动条背景色 */
                width: 10px;
                margin: 0px;
            }

            /* 滚动条把手 */
            QScrollBar::handle:vertical {
                background: #c0c0b0;
                min-height: 20px;
                border-radius: 5px;
            }

            /* 鼠标悬停时把手的颜色 */
            QScrollBar::handle:vertical:hover {
                background: #a0a090;
            }

            /* 滚动条空白区域 */
            QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {
                background: none;
            }

            /* 滚动条按钮（上下箭头） */
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
                height: 0px;
            }
        """)

    def set_font_size(self):
        """设置文本编辑框的字体和大小"""
        # 字体可以保持不变，以支持中文
        font = QFont("Source Han Sans SC", max(8, self.current_font_size))
        self.text_edit.setFont(font)

    def increase_font_size(self):
        """放大字体"""
        self.current_font_size += 2
        self.set_font_size()

    def decrease_font_size(self):
        """缩小字体"""
        if self.current_font_size > 8:
            self.current_font_size -= 2
            self.set_font_size()

    def resizeEvent(self, event):
        # 调整 QSizeGrip 的位置
        self.grip.move(self.width() - self.grip.width(), self.height() - self.grip.height())
        super().resizeEvent(event)

    def contextMenuEvent(self, event):
        """
        处理右键点击事件，显示上下文菜单。
        """
        menu = QMenu(self)
        close_action = menu.addAction("关闭")
        close_action.triggered.connect(QApplication.instance().quit)
        menu.exec(event.globalPos())

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            # 只有在底部拖动栏区域点击时才允许拖动
            if self.bottom_bar.underMouse():
                self.old_pos = event.globalPosition().toPoint()
            else:
                self.old_pos = None  # 在其他区域点击不记录位置
        super().mousePressEvent(event)

    def mouseMoveEvent(self, event):
        if self.old_pos is not None and event.buttons() & Qt.MouseButton.LeftButton:
            delta = QPoint(event.globalPosition().toPoint() - self.old_pos)
            self.move(self.x() + delta.x(), self.y() + delta.y())
            self.old_pos = event.globalPosition().toPoint()

    def mouseReleaseEvent(self, event):
        self.old_pos = None

    # 设置文本编辑器快捷键的自定义行为
    def setup_text_edit(self):
        original_wheel_event = self.text_edit.wheelEvent

        def custom_wheel_event(event):
            if event.modifiers() & Qt.KeyboardModifier.ControlModifier:
                if event.angleDelta().y() > 0:
                    self.increase_font_size()
                else:
                    self.decrease_font_size()
                return
            original_wheel_event(event)

        self.text_edit.wheelEvent = custom_wheel_event

    def keyPressEvent(self, event):
        if event.modifiers() & Qt.KeyboardModifier.ControlModifier:
            if event.key() in [Qt.Key.Key_Plus, Qt.Key.Key_Equal]:
                self.increase_font_size()
                return
            elif event.key() == Qt.Key.Key_Minus:
                self.decrease_font_size()
                return
            elif event.key() == Qt.Key.Key_T:
                self.toggle_pin()
                return
        super().keyPressEvent(event)

    def toggle_pin(self):
        self.is_pinned = not self.is_pinned
        self.pin_button.setChecked(self.is_pinned)  # 确保按钮状态与逻辑同步

        # 尝试使用 win32 模块进行置顶，效果更稳定
        try:
            import win32gui
            import win32con
            hwnd = int(self.winId())

            if self.is_pinned:
                win32gui.SetWindowPos(hwnd, win32con.HWND_TOPMOST, 0, 0, 0, 0,
                                      win32con.SWP_NOMOVE | win32con.SWP_NOSIZE | win32con.SWP_NOACTIVATE)
            else:
                win32gui.SetWindowPos(hwnd, win32con.HWND_NOTOPMOST, 0, 0, 0, 0,
                                      win32con.SWP_NOMOVE | win32con.SWP_NOSIZE | win32con.SWP_NOACTIVATE)
        except ImportError:
            # 如果无法导入 win32 模块（例如在非 Windows 系统上），则使用 Qt 原生方法
            flags = self.windowFlags()
            if self.is_pinned:
                self.setWindowFlags(flags | Qt.WindowType.WindowStaysOnTopHint)
            else:
                self.setWindowFlags(flags & ~Qt.WindowType.WindowStaysOnTopHint)

            # 重新显示窗口以应用标志
            self.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    note = StickyNote()
    note.show()
    sys.exit(app.exec())