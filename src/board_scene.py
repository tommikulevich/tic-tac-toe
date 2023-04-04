from PySide2.QtGui import QPixmap, Qt, QIcon, QTransform
from PySide2.QtWidgets import QGraphicsScene, QMessageBox, QApplication, QStyle

from src.tile_item import TileItem
from src.piece_item import PieceItem
from src.current_piece_item import CurrentPieceItem


class BoardScene(QGraphicsScene):
    def __init__(self, parent=None):
        super().__init__()
        self.window = parent
        self.size = 200
        self.grid = 3

        # Texture parameters (pieces)
        self.oTexture = QPixmap(":/o/standard")
        self.xTexture = QPixmap(":/x/standard")
        self.bonusTexture = QPixmap(":/bonus")

        # Input configuration
        self.playerInput = self.window.inputField
        self.playerInput.returnPressed.connect(self.performTextMove)

        # Game logic parameters
        self.currentPiece = " "
        self.board = [['' for _ in range(self.grid)] for _ in range(self.grid)]
        self.focusedField = None

        self.currentPieceStatus = CurrentPieceItem(self.oTexture, self.xTexture, self.bonusTexture, parent=self)
        self.window.actualPlayerView.scene().addItem(self.currentPieceStatus)

        self.circleScore = 0
        self.crossScore = 0

        # Creating tiles on board
        self.createTiles()

    def createTiles(self):
        tiles = [TileItem(i, j, self.size) for i in range(self.grid) for j in range(self.grid)]
        list(map(self.addItem, tiles))

    # -------------- Game logic functions --------------

    def performMove(self, x, y):
        self.window.warnings.clear()

        if self.board[y][x] != '':
            self.window.warnings.setText("It's already a piece in that tile!")
            return

        piece = PieceItem(self.currentPiece, self.oTexture, self.xTexture, self.size)
        piece.setPos(x * self.size, y * self.size)

        self.addItem(piece)
        self.board[y][x] = self.currentPiece

        if self.checkWinner(self.currentPiece):
            self.showGameOverMessage()

            self.circleScore += 1 if self.currentPieceStatus.currentPiece == 'o' else 0
            self.crossScore += 1 if self.currentPieceStatus.currentPiece == 'x' else 0
            self.window.score.setText(f"O: {self.circleScore} | X: {self.crossScore}")

            self.window.inputField.setReadOnly(True)
            self.window.inputField.setText("Start new game!")
            self.currentPieceStatus.currentPiece = ' '

            return

        if self.checkDraw():
            self.showDrawMessage()

            self.window.inputField.setReadOnly(True)
            self.window.inputField.setText("Start new game!")
            self.currentPieceStatus.currentPiece = ' '

            return

        self.currentPieceStatus.changeSide()
        self.currentPiece = self.currentPieceStatus.currentPiece
        self.window.inputField.setPlaceholderText(f"Input | {self.currentPiece.upper()}")

    def performTextMove(self):
        self.currentPiece = self.currentPieceStatus.currentPiece

        if self.currentPiece == ' ':
            self.window.warnings.setText("Click Game -> Start | Restart")
            return

        moveText = self.playerInput.text()

        if moveText == '':
            self.window.warnings.setText("You have not entered a move!")
            return

        move = int(moveText)

        x = (move - 1) % 3
        y = (move - 1) // 3

        self.performMove(x, y)

        self.playerInput.clear()
        self.playerInput.clearFocus()
        self.views()[0].setFocus()

    def checkWinner(self, piece):
        if any(all(self.board[row][col] == piece for col in range(self.grid)) for row in range(self.grid)):
            return True

        if any(all(self.board[row][col] == piece for row in range(self.grid)) for col in range(self.grid)):
            return True

        if all([self.board[i][i] == piece for i in range(self.grid)]):
            return True

        if all([self.board[i][self.grid - 1 - i] == piece for i in range(self.grid)]):
            return True

    def checkDraw(self):
        return all(self.board[row][col] != '' for row in range(self.grid) for col in range(self.grid))

    def restartGame(self):
        pieces = [item for item in self.items() if isinstance(item, PieceItem)]
        list(map(self.removeItem, pieces))

        self.board = [['' for _ in range(self.grid)] for _ in range(self.grid)]

    # -------------- Additional windows and click events --------------

    def showGameOverMessage(self):
        msg = QMessageBox(self.views()[0])
        msg.setWindowIcon(QIcon(QApplication.instance().style().standardPixmap(QStyle.SP_FileDialogInfoView)))
        msg.setIcon(QMessageBox.Information)
        msg.setText(f"Winner: {self.currentPiece.upper()}!")
        msg.setWindowTitle("Game over")
        msg.show()

    def showDrawMessage(self):
        msg = QMessageBox(self.views()[0])
        msg.setWindowIcon(QIcon(QApplication.instance().style().standardPixmap(QStyle.SP_FileDialogInfoView)))
        msg.setIcon(QMessageBox.Information)
        msg.setText("Game ended in a draw!")
        msg.setWindowTitle("Game over")
        msg.show()

    def mousePressEvent(self, event):
        if event.button() != Qt.LeftButton:
            return

        self.currentPiece = self.currentPieceStatus.currentPiece

        self.window.warnings.clear()
        if self.currentPiece == ' ':
            self.window.warnings.setText("Click Game -> Start | Restart")
            return

        x = int(event.scenePos().x() // self.size)
        y = int(event.scenePos().y() // self.size)

        self.performMove(x, y)

        super().mousePressEvent(event)

    def keyPressEvent(self, event):
        if event.key() in (Qt.Key_Up, Qt.Key_Down, Qt.Key_Left, Qt.Key_Right):
            self.currentPiece = self.currentPieceStatus.currentPiece

            if self.currentPiece == ' ':
                self.window.warnings.setText("Click Game -> Start | Restart")
                return

            if self.focusedField is None:
                self.focusedField = [item for item in self.items() if isinstance(item, TileItem)][0]
                self.focusedField.focused = True
                self.focusedField.update()

                return

            x = int(self.focusedField.x() // self.size)
            y = int(self.focusedField.y() // self.size)

            if event.key() == Qt.Key_Up:
                y -= 1
            elif event.key() == Qt.Key_Down:
                y += 1
            elif event.key() == Qt.Key_Left:
                x -= 1
            elif event.key() == Qt.Key_Right:
                x += 1

            x %= self.grid
            y %= self.grid

            self.focusedField.focused = False
            self.focusedField.update()
            newFocusedField = [item for item in self.items()
                               if isinstance(item, TileItem)
                               and item == self.itemAt(x * self.size, y * self.size, QTransform())][0]

            if newFocusedField is not None:
                self.focusedField = newFocusedField
                self.focusedField.focused = True
                self.focusedField.update()
        elif event.key() == Qt.Key_Enter or event.key() == Qt.Key_Return:
            self.currentPiece = self.currentPieceStatus.currentPiece

            if self.focusedField is not None and self.currentPiece != ' ':
                x = int(self.focusedField.x() // self.size)
                y = int(self.focusedField.y() // self.size)

                self.performMove(x, y)
        elif event.key() == Qt.Key_Backspace:
            if self.focusedField is not None:
                self.focusedField.focused = False
                self.focusedField.update()
                self.focusedField = None
        else:
            super().keyPressEvent(event)
