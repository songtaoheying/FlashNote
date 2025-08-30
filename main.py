# main.py
from PySide6.QtWidgets import QApplication
import sys
from sticky_note import create_window

if __name__ == '__main__':
    app = QApplication(sys.argv)

    # 创建第一个窗口
    note = create_window()
    note.show()

    sys.exit(app.exec())
