import sys
from ui.YtDlpGui import YtDlpGui
from PyQt6.QtWidgets import QApplication

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = YtDlpGui()
    ex.show()
    sys.exit(app.exec())
