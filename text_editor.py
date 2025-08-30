# text_editor.py
from PySide6.QtWidgets import QTextEdit, QColorDialog, QFontDialog
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QApplication

class CustomTextEdit(QTextEdit):

    def __init__(self):
        super().__init__()
        self.current_font_size = 12
        self.set_font_size()
        self.style_manager = StyleSheetManager(self)
        # 添加用户主题偏好属性
        self.user_theme_preference = None  # None表示跟随系统，"dark"表示深色，"light"表示浅色,"custom"
        # 启动时检测并设置系统主题
        self.set_system_theme_mode()

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

    def convert_to_plain_text(self):
        """
        将所有文本转换为普通格式（纯文本格式）
        """
        from PySide6.QtGui import QTextCursor, QTextCharFormat, QTextBlockFormat

        # 获取文档
        doc = self.document()

        # 创建普通字符格式和段落格式
        char_format = QTextCharFormat()
        block_format = QTextBlockFormat()

        # 创建光标并选择整个文档
        cursor = QTextCursor(doc)
        cursor.select(QTextCursor.SelectionType.Document)

        # 应用普通格式（清除所有格式）
        cursor.setCharFormat(char_format)
        cursor.setBlockFormat(block_format)

    def clear_all(self):
        """
        彻底清空所有内容和格式
        """
        # 先转换为纯文本格式
        self.convert_to_plain_text()
        # 然后清除内容
        self.clear()


    def copy_plain_text(self):
        """复制纯文本"""
        from PySide6.QtWidgets import QApplication
        clipboard = QApplication.clipboard()
        plain_text = self.textCursor().selectedText()
        if plain_text:
            clipboard.setText(plain_text)

    def update_style(self, bg_color=None, text_color=None):
        """更新文本编辑器样式"""
        self.style_manager.update_style(bg_color=bg_color, text_color=text_color)

    def change_background_color(self):
        """更改背景颜色"""
        current_bg_color = self.palette().base().color()
        color = QColorDialog.getColor(current_bg_color, self, "选择背景颜色")
        self.user_theme_preference = "custom"
        if color.isValid():
            self.update_style(bg_color=color)

    def change_font_color(self):
        """更改字体颜色"""
        current_color = self.palette().text().color()
        color = QColorDialog.getColor(current_color, self, "选择字体颜色")
        self.user_theme_preference = "custom"
        if color.isValid():
            self.update_style(text_color=color)

    def hide_scrollbars(self, hide):
        """隐藏或显示滚动条"""
        self.style_manager.update_style(scroll_hidden=hide)

    def change_font_dialog(self):
        """更改字体"""
        current_font = self.font()
        ok, font = QFontDialog.getFont(current_font, self)

        if ok:
            self.setFont(font)
            self.current_font_size = font.pointSize()
    def set_dark_mode(self):
        """设置深色模式"""
        from PySide6.QtGui import QColor
        dark_bg = QColor(45, 45, 45)      # 深灰色背景
        dark_text = QColor(240, 240, 240) # 浅灰色文字
        self.update_style(bg_color=dark_bg, text_color=dark_text)
        # 记录用户偏好
        self.user_theme_preference = "dark"

    def set_light_mode(self):
        """设置浅色模式"""
        from PySide6.QtGui import QColor
        light_bg = QColor(255, 255, 255)  # 白色背景
        light_text = QColor(0, 0, 0)      # 黑色文字
        self.update_style(bg_color=light_bg, text_color=light_text)
        # 记录用户偏好
        self.user_theme_preference = "light"

    def set_system_theme_mode(self):
        """根据系统主题设置深色或浅色模式"""
        # 记录用户偏好为跟随系统
        self.user_theme_preference = None

        # 尝试检测系统主题
        try:
            # 对于 Windows 系统
            if hasattr(Qt, 'ColorScheme'):
                # Qt 6.5+ 提供了系统主题检测
                color_scheme = QApplication.styleHints().colorScheme()
                if color_scheme == Qt.ColorScheme.Dark:
                    self.set_dark_mode()
                else:
                    self.set_light_mode()
                self.user_theme_preference = None
            else:
                # 对于较老版本的 Qt，使用默认浅色模式
                self.set_light_mode()

        except Exception as e:
            print(f"设置系统主题时出错: {e}")
            self.set_light_mode()





class StyleSheetManager:
    def __init__(self, text_edit):
        self.text_edit = text_edit
        self.bg_color = "#ffffff"
        self.text_color = "#000000"
        self.scroll_hidden = False
        self._apply_initial_style()  # 初始化样式

    def _apply_initial_style(self):
        """应用初始样式"""
        self.update_style()

    def update_style(self, bg_color=None, text_color=None, scroll_hidden=None):
        """统一更新样式"""
        if bg_color is not None:
            self.bg_color = bg_color.name() if bg_color.isValid() else self.bg_color
        if text_color is not None:
            self.text_color = text_color.name() if text_color.isValid() else self.text_color
        if scroll_hidden is not None:
            self.scroll_hidden = scroll_hidden

        scrollbar_style = self._get_scrollbar_style()

        style = f"""
            QTextEdit {{
                border: none;
                padding: 10px;
                background-color: {self.bg_color};
                color: {self.text_color};
            }}
            {scrollbar_style}
        """

        self.text_edit.setStyleSheet(style)

    def _get_scrollbar_style(self):
        """获取滚动条样式"""
        if self.scroll_hidden:
            return """
                QScrollBar:vertical {
                    width: 0px;
                    background: transparent;
                }
            """
        else:
            return """
                   QScrollBar:vertical {
                       background: rgba(0, 0, 0, 0.05);
                       width: 10px;
                       border-radius: 5px;
                   }
                   QScrollBar::handle:vertical {
                       background: rgba(0, 0, 0, 0.25);
                       border-radius: 5px;
                       min-height: 20px;
                   }
                   QScrollBar::handle:vertical:hover {
                       background: rgba(0, 0, 0, 0.4);
                   }
                   QScrollBar::handle:vertical:pressed {
                       background: rgba(0, 0, 0, 0.5);
                   }
                   QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
                       height: 0px;
                       background: none;
                   }
                   QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {
                       background: none;
                   }
                   """
