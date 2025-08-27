import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QTextEdit, QPushButton, QVBoxLayout, QWidget, QSizeGrip, \
    QHBoxLayout
from PyQt5.QtCore import Qt, QPoint
from PyQt5.QtGui import QColor, QPalette, QFont


class StickyNote(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.Tool)
        self.setAttribute(Qt.WA_TranslucentBackground, False)
        self.setWindowTitle("桌面便签")

        # 初始尺寸
        self.resize(350, 250)
        self.base_size = self.size()

        # 初始字体大小
        self.current_font_size = 16

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
        self.text_edit.setStyleSheet("border: none; padding: 15px;")
        main_layout.addWidget(self.text_edit)

        # 底部区域（用于拖动和放置按钮）
        bottom_bar = QWidget()
        bottom_bar.setFixedHeight(40)
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
        self.pin_button.setFixedSize(25, 25)
        self.pin_button.setStyleSheet("QPushButton { background-color: white; border: none; }")

        # 字体缩小按钮 (红色)
        self.font_down_button = QPushButton("-")
        self.font_down_button.setFixedSize(25, 25)
        self.font_down_button.clicked.connect(self.decrease_font_size)
        self.font_down_button.setStyleSheet(
            "background-color: #f44336; color: white; border: none; font-weight: bold; font-size: 16px;")

        # 字体放大按钮 (绿色)
        self.font_up_button = QPushButton("+")
        self.font_up_button.setFixedSize(25, 25)
        self.font_up_button.clicked.connect(self.increase_font_size)
        self.font_up_button.setStyleSheet(
            "background-color: #4CAF50; color: white; border: none; font-weight: bold; font-size: 16px;")

        # 将按钮添加到布局中，并让它们靠左
        bottom_layout.addWidget(self.pin_button)
        bottom_layout.addWidget(self.font_down_button)
        bottom_layout.addWidget(self.font_up_button)
        bottom_layout.addStretch()  # 伸展器将右侧空间撑开

        main_layout.addWidget(bottom_bar)

        # 窗口尺寸调整控制点
        self.grip = QSizeGrip(self)
        self.grip.setStyleSheet("background-color: black;")
        self.grip.setFixedSize(20, 20)
        self.grip.move(self.width() - self.grip.width(), self.height() - self.grip.height())

        self.old_pos = None
        self.is_pinned = False

        # 首次设置字体
        self.set_font_size()

    def set_font_size(self):
        """设置文本编辑框的字体大小"""
        font = QFont("Arial", max(8, self.current_font_size))
        self.text_edit.setFont(font)

    def increase_font_size(self):
        """放大字体"""
        self.current_font_size += 2
        self.set_font_size()

    def decrease_font_size(self):
        """缩小字体"""
        if self.current_font_size > 8:  # 设置最小字体大小
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

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton and event.pos().y() > self.height() - 40:
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
            self.pin_button.setStyleSheet("QPushButton { background-color: #d8d8d8; border: none; }")
        else:
            self.setWindowFlags(self.windowFlags() & ~Qt.WindowStaysOnTopHint)
            self.pin_button.setStyleSheet("QPushButton { background-color: white; border: none; }")

        self.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    note = StickyNote()
    note.show()
    sys.exit(app.exec_())