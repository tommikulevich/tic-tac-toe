import sys
from PySide2.QtWidgets import QApplication

from game.main_window import MainWindow
from resources import resources_qrc

if __name__ == "__main__":
    app = QApplication(sys.argv)
    ticTacToe = MainWindow()
    sys.exit(app.exec_())
