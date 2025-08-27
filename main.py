import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPlainTextEdit, QSizeGrip
from PyQt5.QtCore import Qt, QPoint
from PyQt5.QtGui import QColor, QPalette


class DesktopNote(QWidget):
    def __init__(self):
        super().__init__()
        self.set_window_properties()
        self.init_ui()

    def set_window_properties(self):
        # 设置窗口标志，实现类似桌面便签的效果
        # Qt.Tool: 工具窗口，通常在主窗口上方，不会出现在任务栏
        # Qt.WindowStaysOnBottomHint: 窗口置于底层
        # 结合这两个标志，可以实现你想要的效果
        self.setWindowFlags(
            Qt.Tool |
            Qt.WindowStaysOnBottomHint |
            Qt.FramelessWindowHint
        )
        self.setAttribute(Qt.WA_TranslucentBackground)  # 禁用默认背景，以便自定义
        self.setMouseTracking(True)  # 启用鼠标跟踪

        # 设置窗口背景颜色
        palette = self.palette()
        palette.setColor(QPalette.Window, QColor(255, 255, 255))
        self.setPalette(palette)
        self.setStyleSheet("background-color: white;")

        # 设置窗口初始大小
        self.setGeometry(100, 100, 300, 200)

    def init_ui(self):
        # 创建布局
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)  # 移除布局边距

        # 自定义标题栏
        self.title_bar = QWidget()
        self.title_bar.setFixedHeight(25)
        self.title_bar.setStyleSheet("background-color: #efebe0;")
        self.title_bar.setMouseTracking(True)
        layout.addWidget(self.title_bar)

        # 创建文本编辑框
        self.text_edit = QPlainTextEdit()
        self.text_edit.setPlaceholderText("请输入文本")
        layout.addWidget(self.text_edit)

        # 添加右下角调整大小的把手
        self.size_grip = QSizeGrip(self)
        self.size_grip.setFixedSize(16, 16)
        layout.addWidget(self.size_grip, 0, Qt.AlignRight | Qt.AlignBottom)

        self.setLayout(layout)

        # 记录鼠标位置，用于窗口拖动
        self.old_pos = None

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.old_pos = event.globalPos()
            # 检查点击位置是否在标题栏
            if self.title_bar.underMouse():
                self.is_dragging = True
            else:
                self.is_dragging = False

    def mouseMoveEvent(self, event):
        if self.old_pos and self.is_dragging:
            delta = event.globalPos() - self.old_pos
            self.move(self.pos() + delta)
            self.old_pos = event.globalPos()

    def mouseReleaseEvent(self, event):
        self.old_pos = None
        self.is_dragging = False


if __name__ == '__main__':
    app = QApplication(sys.argv)

    # 确保应用程序在Windows上正常工作
    if sys.platform == "win32":
        app.setStyle("Fusion")

    note = DesktopNote()
    note.show()
    sys.exit(app.exec_())