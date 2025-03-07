import sys
from PyQt6.QtWidgets import QApplication
from auth import AuthWindow

def main():
    app = QApplication(sys.argv)
    auth_window = AuthWindow()
    auth_window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()