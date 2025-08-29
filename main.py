# main.py
from PySide6.QtWidgets import QApplication
import sys
from sticky_note import StickyNote  # 导入分离的类

if __name__ == '__main__':
    app = QApplication(sys.argv)
    note = StickyNote()
    note.show()
    sys.exit(app.exec())
