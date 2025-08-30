# event_handlers.py
from PySide6.QtCore import Qt, QPoint, QEvent
from PySide6.QtWidgets import QMenu


class WindowEventHandler:
    def __init__(self, parent):
        super().__init__()
        self.parent = parent

    def event_filter(self,_obj,event):
        """
        监听系统主题变化事件
        """
        if event.type() == QEvent.Type.ApplicationPaletteChange:
            # 当系统主题发生变化时，更新应用主题
            if self.parent.text_edit.user_theme_preference is None:
                self.parent.text_edit.set_system_theme_mode()
            return True
        return False
    def mouse_press_event(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            # 只有在底部拖动栏区域点击时才允许拖动
            if self.parent.bottom_bar.underMouse():
                self.parent.old_pos = event.globalPosition().toPoint()
            else:
                self.parent.old_pos = None  # 在其他区域点击不记录位置
        # 调用父类事件处理


    def mouse_move_event(self, event):
        if self.parent.old_pos is not None and event.buttons() & Qt.MouseButton.LeftButton:
            delta = QPoint(event.globalPosition().toPoint() - self.parent.old_pos)
            self.parent.move(self.parent.x() + delta.x(), self.parent.y() + delta.y())
            self.parent.old_pos = event.globalPosition().toPoint()

    def mouse_release_event(self, _event):
        self.parent.old_pos = None

    def wheel_event(self, event):
        """
        处理鼠标滚轮事件，支持 Ctrl + 滚轮进行字体缩放
        """
        # 检查是否按下了 Ctrl 键
        if event.modifiers() & Qt.KeyboardModifier.ControlModifier:
            # 根据滚轮方向调整字体大小
            if event.angleDelta().y() > 0:
                self.parent.increase_font_size()
            else:
                self.parent.decrease_font_size()
            # 阻止事件继续传播
            return
        # 如果没有按下 Ctrl 键，则使用默认的滚轮行为


    def key_press_event(self, event):
        if event.modifiers() & Qt.KeyboardModifier.ControlModifier:
            if event.key() in [Qt.Key.Key_Plus, Qt.Key.Key_Equal]:
                self.parent.increase_font_size()
                return
            elif event.key() == Qt.Key.Key_Minus:
                self.parent.decrease_font_size()
                return
            elif event.key() == Qt.Key.Key_T:
                self.parent.toggle_pin()
                return
            elif event.modifiers() & Qt.KeyboardModifier.ShiftModifier and event.key() == Qt.Key.Key_V:
                self.parent.paste_plain_text()
                return
            elif event.modifiers() & Qt.KeyboardModifier.ShiftModifier and event.key() == Qt.Key.Key_C:
                self.parent.copy_plain_text()
                return


    def resize_event(self, _event):
        # 调整 QSizeGrip 的位置
        self.parent.grip.move(self.parent.width() - self.parent.grip.width(),
                             self.parent.height() - self.parent.grip.height())


    def context_menu_event(self, event):
        """
        处理右键点击事件，显示上下文菜单。
        """
        menu = QMenu(self.parent)



        # 添加背景颜色选项
        background_menu = menu.addMenu("背景")
        change_bg_action = background_menu.addAction("选择背景颜色")
        change_bg_action.triggered.connect(self.parent.change_background_color)

        # 添加深色模式和浅色模式选项
        dark_mode_action = background_menu.addAction("深色模式")
        dark_mode_action.triggered.connect(self.parent.text_edit.set_dark_mode)

        light_mode_action = background_menu.addAction("浅色模式")
        light_mode_action.triggered.connect(self.parent.text_edit.set_light_mode)

        # 在浅色模式选项后添加系统主题选项
        system_theme_action = background_menu.addAction("跟随系统主题")
        system_theme_action.triggered.connect(self.parent.text_edit.set_system_theme_mode)


        font_menu = menu.addMenu("字体")
        change_font_color_action = font_menu.addAction("选择字体颜色")
        change_font_color_action.triggered.connect(self.parent.change_font_color)

        # 添加更改字体选项
        change_font_action = font_menu.addAction("选择字体")
        change_font_action.triggered.connect(self.parent.change_font)

        # 添加新建便签选项
        new_note_action = menu.addAction("新建便签")
        new_note_action.triggered.connect(self.parent.create_new_note)

        close_action = menu.addAction("关闭窗口")
        close_action.triggered.connect(self.parent.close_and_update_count)
        menu.popup(event.globalPos())

    def change_event(self, event):
        """
        监听窗口状态变化事件
        """
        # 只关注 ActivationChange 事件
        if event.type() == QEvent.Type.ActivationChange:
            # 检查窗口是否处于激活状态
            if not self.parent.isActiveWindow():
                # print("失去焦点")
                # 失去焦点时隐藏底栏
                self.parent.bottom_bar.hide()
                self.parent.hide_scrollbars(True)
            else:
                # print("获得焦点")
                self.parent.bottom_bar.show()
                self.parent.hide_scrollbars(False)


class TextEditEventHandler:
    def __init__(self, parent):
        self.parent = parent
        # 连接文本编辑区域的上下文菜单信号
        self.parent.text_edit.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.parent.text_edit.customContextMenuRequested.connect(self.extend_text_edit_context_menu)

    def extend_text_edit_context_menu(self, position):
        """
        扩展现有的文本编辑区域右键菜单，添加自定义选项
        """
        # 创建标准上下文菜单
        menu = self.parent.text_edit.createStandardContextMenu()

        # 添加分隔符
        menu.addSeparator()

        # 添加自定义选项
        paste_plain_action = menu.addAction("粘贴为纯文本")
        paste_plain_action.setShortcut("Ctrl+Shift+V")
        paste_plain_action.triggered.connect(self.parent.text_edit.paste_plain_text)

        # 添加复制为纯文本选项
        copy_plain_action = menu.addAction("复制为纯文本")
        copy_plain_action.setShortcut("Ctrl+Shift+C")
        copy_plain_action.triggered.connect(self.parent.text_edit.copy_plain_text)
        # 检查是否有选中的文本，如果没有则禁用复制为纯文本选项
        has_selection = self.parent.text_edit.textCursor().hasSelection()
        copy_plain_action.setEnabled(has_selection)

        # 添加转换为纯文本选项
        convert_plain_action = menu.addAction("转换为纯文本(清除格式)")
        convert_plain_action.triggered.connect(self.parent.text_edit.convert_to_plain_text)

        # 添加清空内容与格式选项
        clear_action = menu.addAction("清空内容")
        clear_action.triggered.connect(self.parent.text_edit.clear_all)

        # 显示菜单
        menu.exec(self.parent.text_edit.mapToGlobal(position))
