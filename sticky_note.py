# sticky_note.py
from PySide6.QtGui import QFont, Qt
from PySide6.QtWidgets import QMainWindow, QVBoxLayout, QWidget, QSizeGrip, QApplication

from event_handlers import WindowEventHandler, TextEditEventHandler
from text_editor import CustomTextEdit
from ui_components import create_bottom_bar, toggle_pin



# 定义全局边框颜色变量
BORDER_COLOR = "#d4cbb8"

class StickyNote(QMainWindow):
    def __init__(self):
        super().__init__()
        self.old_pos = None
        self.is_pinned = False

        self.setWindowFlags(Qt.WindowType.FramelessWindowHint | Qt.WindowType.Tool)
        # self.setWindowTitle("桌面便签")

        # 调整窗口的整体样式，使用更柔和的颜色
        self.setStyleSheet(f"""
            QMainWindow {{
                border: 1px solid {BORDER_COLOR};   /* 边框颜色 */
            }}
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
        QApplication.instance().installEventFilter(self)

        # 首次设置字体
        font = QFont("Source Han Sans SC", max(8, self.current_font_size))
        self.text_edit.setFont(font)

    # sticky_note.py


    def toggle_pin(self):
        toggle_pin(self)

    def change_background_color(self):
        self.text_edit.change_background_color()

    def change_font_color(self):
        self.text_edit.change_font_color()

    def change_font(self):
        self.text_edit.change_font_dialog()
    def hide_scrollbars(self,hide):
        self.text_edit.hide_scrollbars(hide)

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


    def eventFilter(self, obj, event):
        # 调用自定义的事件处理方法
        return self.window_event_handler.event_filter(obj, event)

    # 在 sticky_note.py 中
    def create_new_note(self):
        """
        创建新的便签实例
        """

        # 创建新的便签窗口
        new_note = create_window()
        # 设置新便签的位置稍微偏移一些，避免完全重叠
        new_pos = self.pos()
        new_note.move(new_pos.x() + 30, new_pos.y() + 30)
        new_note.show()
    def close_and_update_count(self):
        """关闭窗口并手动触发计数更新"""

        # 先减少计数
        on_window_destroyed()
        # 再关闭窗口
        self.close()

# 全局窗口计数
window_count = 0
def on_window_destroyed():
    """窗口销毁时调用"""
    global window_count
    # print("当前窗口数:", window_count)
    window_count -= 1
    # print("递减后窗口数:", window_count)
    if window_count <= 0:
        QApplication.quit()

def create_window():
    """创建新窗口并增加计数"""
    global window_count
    window = StickyNote()
    # print("当前窗口数", window_count)
    window_count += 1
    # print("递增当前窗口数:", window_count)
    return window
