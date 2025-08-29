# text_editor.py
from PySide6.QtWidgets import QTextEdit, QColorDialog, QFontDialog
from PySide6.QtCore import Qt  # 添加这一行

class CustomTextEdit(QTextEdit):
    def __init__(self):
        super().__init__()
        self.setup_ui()
        self.current_font_size = 12
        self.set_font_size()

    def setup_ui(self):
        """设置文本编辑区域的UI样式"""
        self.setStyleSheet("""
            QTextEdit {
                border: none;
                padding: 10px;
                background-color: white;
            }
            QTextEdit[hideScroll="true"] QScrollBar:vertical {
                width: 0px;
                background: transparent;
            }
        """)

    def set_font_size(self):
        """设置字体大小"""
        # 获取当前字体并只修改字体大小
        font = self.font()
        font.setPointSize(max(8, self.current_font_size))
        self.setFont(font)

    def increase_font_size(self):
        """放大字体"""
        self.current_font_size += 2
        self.set_font_size()

    def decrease_font_size(self):
        """缩小字体"""
        if self.current_font_size > 8:
            self.current_font_size -= 2
            self.set_font_size()

    def paste_plain_text(self):
        """粘贴纯文本"""
        from PySide6.QtWidgets import QApplication
        clipboard = QApplication.clipboard()
        plain_text = clipboard.text()
        if plain_text:
            self.insertPlainText(plain_text)

    def copy_plain_text(self):
        """复制纯文本"""
        from PySide6.QtWidgets import QApplication
        clipboard = QApplication.clipboard()
        plain_text = self.textCursor().selectedText()
        if plain_text:
            clipboard.setText(plain_text)

def change_background_color(parent):
    """
    更改文本编辑区域的背景颜色
    """
    # 获取当前背景颜色作为默认选择
    current_bg_color = parent.text_edit.palette().base().color()
    current_text_color = parent.text_edit.palette().base().color()

    # 弹出颜色选择对话框
    color = QColorDialog.getColor(current_bg_color, parent, "选择背景颜色")

    if color.isValid():
        # 构建新的样式表，保持其他样式属性不变
        style = f"""
            QTextEdit {{
                border: none;
                padding: 10px;
                background-color: {color.name()};  /* 设置新的背景颜色 */
                color: {current_text_color.name()};           /* 设置原来字体颜色 */
            }}
            /* 保持滚动条样式 */
            QTextEdit[hideScroll="true"] QScrollBar:vertical {{
                width: 0px;
                background: transparent;
            }}
        """
        parent.text_edit.setStyleSheet(style)

def change_font_color(parent):
    """
    更改文本编辑区域的字体颜色
    """
    # 获取当前字体颜色作为默认选择
    current_color = parent.text_edit.palette().text().color()

    # 弹出颜色选择对话框
    color = QColorDialog.getColor(current_color, parent, "选择字体颜色")

    if color.isValid():
        # 获取当前背景颜色以保持背景样式不变
        current_bg = parent.text_edit.palette().base().color().name()

        # 构建新的样式表，同时保持背景颜色和滚动条样式
        style = f"""
            QTextEdit {{
                border: none;
                padding: 10px;
                background-color: {current_bg};  /* 保持背景颜色 */
                color: {color.name()};           /* 设置新的字体颜色 */
            }}
            /* 保持滚动条样式 */
            QTextEdit[hideScroll="true"] QScrollBar:vertical {{
                width: 0px;
                background: transparent;
            }}
        """
        parent.text_edit.setStyleSheet(style)

def hide_scrollbars(parent, hide):
    """隐藏或显示滚动条"""
    if hide:
        parent.text_edit.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
    else:
        parent.text_edit.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)


def change_font(parent):
    """
    更改文本编辑区域的字体
    """
    # 获取当前字体作为默认选择
    current_font = parent.text_edit.font()

    ok,font = QFontDialog.getFont(current_font, parent)

    if ok:
        parent.text_edit.setFont(font)
        parent.text_edit.current_font_size = font.pointSize()