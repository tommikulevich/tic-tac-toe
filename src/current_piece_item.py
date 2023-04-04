from PySide2.QtGui import QPixmap, Qt
from PySide2.QtWidgets import QGraphicsPixmapItem


class CurrentPieceItem(QGraphicsPixmapItem):
    def __init__(self, oTexture, xTexture, bonusTexture, size=40, parent=None):
        super().__init__()
        self.board = parent
        self.size = size
        self.currentPiece = ' '

        self.oTexture = oTexture
        self.xTexture = xTexture
        self.bonusTexture = bonusTexture
        self.updateItem()

    def loadTexture(self):
        if self.currentPiece == "o":
            self.setPixmap(self.oTexture.scaled(self.size, self.size, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        elif self.currentPiece == "x":
            self.setPixmap(self.xTexture.scaled(self.size, self.size, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        else:
            self.setPixmap(self.bonusTexture.scaled(self.size, self.size, Qt.KeepAspectRatio, Qt.SmoothTransformation))

    def changePieceTexture(self, pieceStyle):
        self.oTexture = QPixmap(f":/o/{pieceStyle}")
        self.xTexture = QPixmap(f":/x/{pieceStyle}")
        self.updateItem()

    def updateItem(self):
        self.loadTexture()
        self.update()

    def changeSide(self):
        self.currentPiece = "x" if self.currentPiece == "o" else "o"
        self.updateItem()
