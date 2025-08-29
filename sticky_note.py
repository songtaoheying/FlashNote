# sticky_note.py
from PySide6.QtGui import QFont, Qt
from PySide6.QtWidgets import QMainWindow, QVBoxLayout, QWidget, QSizeGrip

from event_handlers import WindowEventHandler, TextEditEventHandler
from text_editor import CustomTextEdit, change_background_color, change_font_color, hide_scrollbars, change_font
from ui_components import create_bottom_bar, toggle_pin


class StickyNote(QMainWindow):
    def __init__(self):
        super().__init__()
        self.old_pos = None
        self.is_pinned = False

        self.setWindowFlags(Qt.WindowType.FramelessWindowHint | Qt.WindowType.Tool)
        # self.setWindowTitle("桌面便签")

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
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(1, 1, 1, 1)
        main_layout.setSpacing(0)

        # 创建文本编辑区域
        self.text_edit = CustomTextEdit()
        main_layout.addWidget(self.text_edit)

        # 底部区域，用作拖动句柄和按钮区域
        self.bottom_bar = create_bottom_bar(self)
        main_layout.addWidget(self.bottom_bar)

        # 窗口尺寸调整控制点
        self.grip = QSizeGrip(self)
        self.grip.setFixedSize(30, 30)
        self.grip.move(self.width() - self.grip.width(), self.height() - self.grip.height())

        # 初始化事件处理器
        self.window_event_handler = WindowEventHandler(self)
        self.text_event_handler = TextEditEventHandler(self)

        # 首次设置字体
        font = QFont("Source Han Sans SC", max(8, self.current_font_size))
        self.text_edit.setFont(font)





    # 在 StickyNote 类中添加以下方法
    def toggle_pin(self):
        toggle_pin(self)

    def change_background_color(self):
        change_background_color(self)

    def change_font_color(self):
        change_font_color(self)

    def hide_scrollbars(self, hide):
        hide_scrollbars(self, hide)

    def mousePressEvent(self, event):
        self.window_event_handler.mouse_press_event(event)

    def mouseMoveEvent(self, event):
        self.window_event_handler.mouse_move_event(event)

    def mouseReleaseEvent(self, event):
        self.window_event_handler.mouse_release_event(event)

    def wheelEvent(self, event):
        self.window_event_handler.wheel_event(event)

    def keyPressEvent(self, event):
        self.window_event_handler.key_press_event(event)

    def resizeEvent(self, event):
        self.window_event_handler.resize_event(event)

    def contextMenuEvent(self, event):
        self.window_event_handler.context_menu_event(event)

    def changeEvent(self, event):
        # 只有在 window_event_handler 初始化后才处理事件
        if hasattr(self, 'window_event_handler') and self.window_event_handler:
            self.window_event_handler.change_event(event)
        # 调用父类的 changeEvent 方法确保正常行为
        super().changeEvent(event)

    def increase_font_size(self):
        self.text_edit.increase_font_size()

    def decrease_font_size(self):
        self.text_edit.decrease_font_size()

    def paste_plain_text(self):
        self.text_edit.paste_plain_text()

    def copy_plain_text(self):
        self.text_edit.copy_plain_text()

    def change_font(self):
        change_font(self)