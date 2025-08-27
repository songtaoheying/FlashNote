import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QPlainTextEdit
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor, QPalette


class NotepadWidget(QMainWindow):
    def __init__(self):
        super().__init__()

        # 1. 设置窗口属性
        self.setWindowFlags(
            Qt.Tool |  # 启用Qt.Tool标志，使其不显示在任务栏，并能被其他普通窗口覆盖
            Qt.WindowStaysOnBottomHint |  # 关键标志：保持窗口在所有普通窗口下方
            Qt.CustomizeWindowHint |  # 启用自定义窗口边框
            Qt.WindowMinMaxButtonsHint |  # 启用最小化和最大化按钮
            Qt.FramelessWindowHint  # 如果想完全自定义边框，可以启用此项，但会失去拖动功能
        )
        # 我们可以通过Qt.Tool和Qt.WindowStaysOnBottomHint来实现类似桌面组件的效果。
        # Qt.WindowStaysOnBottomHint 使得窗口保持在底部，而Qt.Tool则让它不出现在任务栏上。

        # 2. 窗口标题栏和大小
        self.setWindowTitle("")  # 5. 标题栏无内容
        self.setGeometry(100, 100, 400, 300)  # 初始位置和大小 (100,100,400,300)
        self.setMinimumSize(200, 150)  # 限制最小尺寸

        # 3. 窗口颜色和透明度
        self.setAutoFillBackground(True)
        palette = self.palette()
        palette.setColor(QPalette.Window, QColor(255, 255, 255))  # 3. 窗口白色
        self.setPalette(palette)

        # 4. 创建文本编辑区域
        self.text_editor = QPlainTextEdit(self)
        self.text_editor.setPlaceholderText("请输入文本")  # 默认展示文本
        self.text_editor.setStyleSheet("background-color: white; border: none;")
        self.setCentralWidget(self.text_editor)

        # 6. 拖动窗口功能
        # 通过重写鼠标事件来实现窗口的拖动
        self.oldPos = None

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.oldPos = event.globalPos()
            event.accept()

    def mouseMoveEvent(self, event):
        if self.oldPos is not None and event.buttons() == Qt.LeftButton:
            delta = event.globalPos() - self.oldPos
            self.move(self.pos() + delta)
            self.oldPos = event.globalPos()
            event.accept()

    def mouseReleaseEvent(self, event):
        self.oldPos = None
        event.accept()


if __name__ == "__main__":
    app = QApplication(sys.argv)

    # 关键步骤：设置应用程序的属性
    # Qt.AA_UseHighDpiPixmaps 可以在高分辨率屏幕上更好地显示
    # QApplication.setDesktopSettingsAware(False) 可以在某些情况下防止窗口隐藏
    app.setAttribute(Qt.AA_UseHighDpiPixmaps)
    app.setDesktopSettingsAware(False)

    note = NotepadWidget()
    note.show()
    sys.exit(app.exec_())