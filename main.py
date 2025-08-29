import os
import sys


from PySide6.QtWidgets import QApplication, QMainWindow, QTextEdit, QPushButton, QVBoxLayout, QWidget, QSizeGrip, \
    QHBoxLayout, QMenu
from PySide6.QtCore import Qt, QPoint, QSize, QEvent
from PySide6.QtGui import QFont, QIcon, QPixmap


def resource_path(relative_path):
    """获取资源文件的绝对路径"""
    try:
        # PyInstaller创建的临时文件夹
        base_path = getattr(sys, '_MEIPASS', os.path.abspath("."))# noqa
    except AttributeError:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


# 使用 resource_path 函数获取图标路径
ICON_PATH_DEFAULT = resource_path("resources/setTop_default.svg")
ICON_PATH_CHECKED = resource_path("resources/setTop_checked.svg")


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
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(1, 1, 1, 1)
        main_layout.setSpacing(0)

        # 创建文本编辑区域
        self.text_edit = QTextEdit()
        self.set_text_edit()
        main_layout.addWidget(self.text_edit)

        # 连接文本编辑区域的上下文菜单信号
        self.text_edit.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.text_edit.customContextMenuRequested.connect(self.extend_text_edit_context_menu)

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




        # 创建图标对象，使用 resource_path 获取正确路径
        pin_icon_default =QIcon(QPixmap(ICON_PATH_DEFAULT))
        self.pin_button.setIcon(pin_icon_default)
        self.pin_button.setIconSize(QSize(20, 20))

        # 使用样式表来控制图标和背景颜色
        self.pin_button.setStyleSheet(f"""
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

    def changeEvent(self, event):
        """
        监听窗口状态变化事件
        """
        # 只关注 ActivationChange 事件
        if event.type() == QEvent.Type.ActivationChange:
            # 检查窗口是否处于激活状态
            if not self.isActiveWindow():
                # print("失去焦点")
                # 失去焦点时隐藏底栏
                self.bottom_bar.hide()
                self.hide_scrollbars(True)
            else:
                # print("获得焦点")
                self.bottom_bar.show()
                self.hide_scrollbars(False)

        super().changeEvent(event)

    def hide_scrollbars(self, hide):
        """隐藏或显示滚动条"""
        if hide:
            self.text_edit.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        else:
            self.text_edit.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)

    def set_text_edit(self):
        """创建并配置文本编辑区域"""
        # 文本编辑区域
        self.text_edit.setStyleSheet("""
            QTextEdit {
                border: none;
                padding: 10px;
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
            
            /* 当hideScroll属性为true时隐藏滚动条 */
            QTextEdit[hideScroll="true"] QScrollBar:vertical {
                width: 0px;
            background: transparent;
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

    def extend_text_edit_context_menu(self, position):
        """
        扩展现有的文本编辑区域右键菜单，添加自定义选项
        """
        # 创建标准上下文菜单
        menu = self.text_edit.createStandardContextMenu()

        # 添加分隔符
        menu.addSeparator()

        # 添加自定义选项
        paste_plain_action = menu.addAction("粘贴为纯文本")
        paste_plain_action.setShortcut("Ctrl+Shift+V")
        paste_plain_action.triggered.connect(self.paste_plain_text)

        # 添加复制为纯文本选项
        copy_plain_action = menu.addAction("复制为纯文本")
        copy_plain_action.setShortcut("Ctrl+Shift+C")
        copy_plain_action.triggered.connect(self.copy_plain_text)
        # 检查是否有选中的文本，如果没有则禁用复制为纯文本选项
        has_selection = self.text_edit.textCursor().hasSelection()
        copy_plain_action.setEnabled(has_selection)

        # 添加其他自定义选项（示例）
        clear_action = menu.addAction("清空内容")
        clear_action.triggered.connect(self.text_edit.clear)

        # 显示菜单
        menu.exec(self.text_edit.mapToGlobal(position))
    def contextMenuEvent(self, event):
        """
        处理右键点击事件，显示上下文菜单。
        """
        menu = QMenu(self)

        close_action = menu.addAction("关闭窗口")
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

    def paste_plain_text(self):
        """
        粘贴纯文本内容，去除格式
        """
        clipboard = QApplication.clipboard()
        plain_text = clipboard.text()
        if plain_text:
            self.text_edit.insertPlainText(plain_text)

    def copy_plain_text(self):
        """
        复制选中的纯文本内容，去除格式
        """
        clipboard = QApplication.clipboard()
        plain_text = self.text_edit.textCursor().selectedText()
        if plain_text:
            clipboard.setText(plain_text)
    def mouseMoveEvent(self, event):
        if self.old_pos is not None and event.buttons() & Qt.MouseButton.LeftButton:
            delta = QPoint(event.globalPosition().toPoint() - self.old_pos)
            self.move(self.x() + delta.x(), self.y() + delta.y())
            self.old_pos = event.globalPosition().toPoint()

    def mouseReleaseEvent(self, event):
        self.old_pos = None

    # 在 keyPressEvent 方法之后添加以下代码
    def wheelEvent(self, event):
        """
        处理鼠标滚轮事件，支持 Ctrl + 滚轮进行字体缩放
        """
        # 检查是否按下了 Ctrl 键
        if event.modifiers() & Qt.KeyboardModifier.ControlModifier:
            # 根据滚轮方向调整字体大小
            if event.angleDelta().y() > 0:
                self.increase_font_size()
            else:
                self.decrease_font_size()
            # 阻止事件继续传播
            return
        # 如果没有按下 Ctrl 键，则使用默认的滚轮行为
        super().wheelEvent(event)

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
            elif event.modifiers() & Qt.KeyboardModifier.ShiftModifier and event.key() == Qt.Key.Key_V:
                self.paste_plain_text()
                return
            elif event.modifiers() & Qt.KeyboardModifier.ShiftModifier and event.key() == Qt.Key.Key_C:
                self.copy_plain_text()
                return
        super().keyPressEvent(event)

    def toggle_pin(self):
        self.is_pinned = not self.is_pinned
        self.pin_button.setChecked(self.is_pinned)  # 确保按钮状态与逻辑同步

        # 动态切换图标
        if self.is_pinned:
            self.pin_button.setIcon(QIcon(QPixmap(ICON_PATH_CHECKED)))
        else:
            self.pin_button.setIcon(QIcon(QPixmap(ICON_PATH_DEFAULT)))

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