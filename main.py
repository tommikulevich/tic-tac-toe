import sys
from PySide2.QtWidgets import QApplication

from src.main_window import MainWindow


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ticTacToe = MainWindow()
    sys.exit(app.exec_())
