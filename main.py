import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QTextEdit, QPushButton, QVBoxLayout, QWidget, QSizeGrip, \
    QHBoxLayout, QMenu
from PyQt5.QtCore import Qt, QPoint
from PyQt5.QtGui import QColor, QPalette, QFont


class StickyNote(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.Tool)
        self.setWindowTitle("桌面便签")

        # 窗口加上黑白边框 避免白色背景
        self.setStyleSheet("""
            QMainWindow {
                border: 1px solid #000; /* 设置一个浅灰色边框 */
                background-color: white;    /* 窗口背景色 */
            }
        """)

        # 初始尺寸
        self.resize(500, 400)
        self.base_size = self.size()

        # 初始字体大小
        self.current_font_size = 12

        # 窗口的白色背景
        palette = self.palette()
        palette.setColor(QPalette.Window, QColor(255, 255, 255))
        self.setPalette(palette)

        # 创建中央 Widget 和布局
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(1, 1, 1, 1)
        main_layout.setSpacing(0)

        # 文本编辑区域
        self.text_edit = QTextEdit()
        self.text_edit.setPlaceholderText("请输入文本")
        self.text_edit.setStyleSheet("""
            QTextEdit {
                border: none;
                padding: 15px;
                background-color: #fff;  /* 文本区域的背景颜色 */
            }

            /* 垂直滚动条 */
            QScrollBar:vertical {
                border: none;
                background: #f0f0f0;
                width: 10px;  /* 滚动条宽度 */
                margin: 0px 0px 0px 0px;
            }

            /* 滚动条把手 */
            QScrollBar::handle:vertical {
                background: #c0c0c0; /* 把手的颜色 */
                min-height: 20px;
                border-radius: 5px; /* 把手圆角 */
            }

            /* 鼠标悬停时把手的颜色 */
            QScrollBar::handle:vertical:hover {
                background: #a0a0a0;
            }

            /* 滚动条空白区域 */
            QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {
                background: none;
            }

            /* 滚动条按钮（上下箭头） */
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
                height: 0px; /* 隐藏上下箭头 */
            }
        """)

        main_layout.addWidget(self.text_edit)

        # 底部区域（用于拖动和放置按钮）
        bottom_bar = QWidget()
        bottom_bar.setFixedHeight(60)
        bottom_bar.setStyleSheet("background-color: #efebe0; border-top: 1px solid #d0d0d0;")

        bottom_layout = QHBoxLayout(bottom_bar)
        bottom_layout.setContentsMargins(10, 5, 10, 5)

        # 拖动区域
        self.drag_area = QWidget()
        self.drag_area.setStyleSheet("background-color: transparent;")
        self.drag_area.setMouseTracking(True)
        self.drag_area.setFixedHeight(10)
        self.drag_area.mousePressEvent = self.drag_press_event
        self.drag_area.mouseMoveEvent = self.drag_move_event
        main_layout.addWidget(self.drag_area)

        # 置顶按钮
        self.pin_button = QPushButton()
        self.pin_button.setCheckable(True)
        self.pin_button.clicked.connect(self.toggle_pin)
        self.pin_button.setFixedSize(45, 45)
        # 修改为圆形
        self.pin_button.setStyleSheet("""
            QPushButton {
                background-color: white;
                border: 1px solid #d0d0d0; /* 添加一个浅色边框 */
                border-radius: 10px;      /* 圆形 */
            }
        """)
        # 字体缩小按钮
        self.font_down_button = QPushButton("-")
        self.font_down_button.setFixedSize(32, 32)
        self.font_down_button.clicked.connect(self.decrease_font_size)
        self.font_down_button.setStyleSheet("""
            QPushButton {
                background-color: #555555; /* 深灰色背景 */
                color: white; /* 白色字体 */
                border: none;
                border-radius: 16px;
                font-weight: bold;
                font-size: 32px;
            }
            QPushButton:pressed { /* 点击时变暗 */
                background-color: #333333;
            }
        """)
        # 字体放大按钮
        self.font_up_button = QPushButton("+")
        self.font_up_button.setFixedSize(32, 32)
        self.font_up_button.clicked.connect(self.increase_font_size)
        self.font_up_button.setStyleSheet("""
            QPushButton {
                background-color: #555555; /* 深灰色背景 */
                color: white; /* 白色字体 */
                border: none;
                border-radius: 16px;
                font-weight: bold;
                font-size: 32px;
            }
            QPushButton:pressed { /* 点击时变暗 */
                background-color: #333333;
            }
        """)
        # 将按钮添加到布局中，并让它们靠左
        bottom_layout.addWidget(self.pin_button)
        bottom_layout.addWidget(self.font_down_button)
        bottom_layout.addWidget(self.font_up_button)
        bottom_layout.addStretch()

        main_layout.addWidget(bottom_bar)

        # 窗口尺寸调整控制点
        self.grip = QSizeGrip(self)
        self.grip.setFixedSize(30, 30)
        self.grip.move(self.width() - self.grip.width(), self.height() - self.grip.height())

        self.old_pos = None
        self.is_pinned = False

        # 首次设置字体
        self.set_font_size()

    def set_font_size(self):
        """设置文本编辑框的字体和大小"""
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

    def drag_press_event(self, event):
        if event.button() == Qt.LeftButton:
            self.old_pos = event.globalPos()

    def drag_move_event(self, event):
        if self.old_pos is not None:
            delta = QPoint(event.globalPos() - self.old_pos)
            self.move(self.x() + delta.x(), self.y() + delta.y())
            self.old_pos = event.globalPos()

    def drag_release_event(self, event):
        self.old_pos = None

    def contextMenuEvent(self, event):
        """
        处理右键点击事件，显示上下文菜单。
        """
        menu = QMenu(self)
        close_action = menu.addAction("close")

        # 将 "关闭" 选项与关闭窗口的方法连接起来
        close_action.triggered.connect(self.close)

        # 在鼠标点击的位置显示菜单
        menu.exec_(event.globalPos())

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton and event.pos().y() > self.height() - 50:
            self.old_pos = event.globalPos()

    def mouseMoveEvent(self, event):
        if self.old_pos is not None:
            delta = QPoint(event.globalPos() - self.old_pos)
            self.move(self.x() + delta.x(), self.y() + delta.y())
            self.old_pos = event.globalPos()

    def mouseReleaseEvent(self, event):
        self.old_pos = None

    def toggle_pin(self):
        self.is_pinned = not self.is_pinned
        if self.is_pinned:
            self.setWindowFlags(self.windowFlags() | Qt.WindowStaysOnTopHint)
            self.pin_button.setStyleSheet("""
                QPushButton {
                    background-color: #d8d8d8; /* 置顶时的背景色 */
                    border: 1px solid #c0c0c0;
                    border-radius: 10px;
                }
            """)
        else:
            self.setWindowFlags(self.windowFlags() & ~Qt.WindowStaysOnTopHint)
            self.pin_button.setStyleSheet("""
                QPushButton {
                    background-color: white;
                    border: 1px solid #d0d0d0;
                    border-radius: 10px;
                }
            """)
        self.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    note = StickyNote()
    note.show()
    sys.exit(app.exec_())