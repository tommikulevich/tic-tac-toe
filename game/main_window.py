from PySide2.QtCore import QFile
from PySide2.QtGui import QIcon, QIntValidator
from PySide2.QtUiTools import QUiLoader
from PySide2.QtWidgets import QGraphicsView, QMainWindow, QLineEdit, QLabel, QGraphicsScene, QAction, QStyle, \
    QMessageBox, QApplication

from game.clock_item import Clock
from game.board_scene import BoardScene


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # Loading UI created in Qt Designer
        ui = QFile(':/window_ui')
        ui.open(QFile.ReadOnly)
        self.ui = QUiLoader().load(ui, None)
        self.setCentralWidget(self.ui)
        ui.close()

        self.setWindowTitle("Tic Tac Toe [ASK-Lab]")
        self.setWindowIcon(QIcon(":/o/standard"))

        # Finding board components
        self.gameBoardView = self.findChild(QGraphicsView, 'gameBoard')
        self.clockView = self.findChild(QGraphicsView, 'clockView')
        self.actualPlayerView = self.findChild(QGraphicsView, 'actualPlayer')
        self.inputField = self.findChild(QLineEdit, 'inputField')
        self.score = self.findChild(QLabel, 'score')
        self.warnings = self.findChild(QLabel, 'labelWarnings')
        self.startGameAction = self.findChild(QAction, 'startGame')
        self.exitGameAction = self.findChild(QAction, 'exitGame')
        self.aboutProjectAction = self.findChild(QAction, 'about')

        # Window components configuration
        self.startGameAction.triggered.connect(self.startNewGame)
        self.startGameAction.setIcon(self.style().standardIcon(QStyle.SP_ArrowForward))
        self.exitGameAction.triggered.connect(self.exitGame)
        self.exitGameAction.setIcon(self.style().standardIcon(QStyle.SP_BrowserStop))
        self.aboutProjectAction.triggered.connect(self.aboutProjectWindow)
        self.aboutProjectAction.setIcon(self.style().standardIcon(QStyle.SP_MessageBoxInformation))

        # Creating clock
        self.clock = Clock(parent=self)
        self.clockView.setScene(QGraphicsScene(self))
        self.clockView.scene().addItem(self.clock)

        # Input field configuration
        self.inputValidator = QIntValidator()
        self.inputValidator.validate = lambda inputStr, pos: self.validate(inputStr, pos)
        self.inputField.setValidator(self.inputValidator)
        self.actualPlayerView.setScene(QGraphicsScene(self))

        # Creating board
        self.board = BoardScene(parent=self)
        self.gameBoardView.setScene(self.board)

        self.show()

    @staticmethod
    def validate(inputStr, pos):
        # Checking if input is number 1-9
        if inputStr == '' or (inputStr.isdigit() and 1 <= int(inputStr) <= 9):
            return QIntValidator.Acceptable, inputStr, pos

        return QIntValidator.Invalid, inputStr, pos

    def startNewGame(self):
        self.warnings.clear()
        self.inputField.clear()
        self.inputField.setReadOnly(False)
        self.inputField.setPlaceholderText("Input | O")

        self.board.currentPieceStatus.currentPiece = "o"
        self.board.currentPieceStatus.updateItem()
        self.board.restartGame()

    def exitGame(self):
        self.close()

    def aboutProjectWindow(self):
        msg = QMessageBox(self)
        msg.setWindowIcon(QIcon(QApplication.instance().style().standardPixmap(QStyle.SP_FileDialogInfoView)))
        msg.setIcon(QMessageBox.Information)
        msg.setText("Authors: \n - Radosław Dębiński | 184818 \n - Tomash Mikulevich | 187720")
        msg.setWindowTitle("About project")
        msg.show()
