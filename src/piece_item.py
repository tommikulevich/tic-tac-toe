from PySide2.QtGui import QPixmap, Qt
from PySide2.QtWidgets import QMenu, QAction, QGraphicsPixmapItem


class PieceItem(QGraphicsPixmapItem):
    def __init__(self, piece, oTexture, xTexture, size=200):
        super().__init__()
        self.piece = piece
        self.size = size

        self.oTexture = oTexture
        self.xTexture = xTexture
        self.loadTexture()

    def loadTexture(self):
        if self.piece == "o":
            self.setPixmap(self.oTexture.scaled(self.size, self.size, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        elif self.piece == "x":
            self.setPixmap(self.xTexture.scaled(self.size, self.size, Qt.KeepAspectRatio, Qt.SmoothTransformation))

    def contextMenuEvent(self, event):
        # Menu to change pieces style
        menu = QMenu()

        pieceStyleMenu = QMenu("Change pieces style", menu)
        standardAction = QAction("Standard", pieceStyleMenu)
        neonAction = QAction("Neon", pieceStyleMenu)
        skyAction = QAction("Sky", pieceStyleMenu)

        pieceStyleMenu.addAction(standardAction)
        pieceStyleMenu.addAction(neonAction)
        pieceStyleMenu.addAction(skyAction)
        menu.addMenu(pieceStyleMenu)

        standardAction.triggered.connect(lambda: self.changePieceTexture("standard"))
        neonAction.triggered.connect(lambda: self.changePieceTexture("neon"))
        skyAction.triggered.connect(lambda: self.changePieceTexture("sky"))

        menu.exec_(event.screenPos())

    def changePieceTexture(self, pieceStyle):
        # Updating BoardScene texture parameters
        self.scene().oTexture = QPixmap(f":/o/{pieceStyle}")
        self.scene().xTexture = QPixmap(f":/x/{pieceStyle}")

        # Updating texture of CurrentPieceItem initialized in BoardScene
        self.scene().currentPieceStatus.changePieceTexture(pieceStyle)

        # Updating piece items
        [self.updatePieceItem(item) for item in self.scene().items() if isinstance(item, PieceItem)]

    @staticmethod
    def updatePieceItem(piece):
        piece.oTexture = piece.scene().oTexture
        piece.xTexture = piece.scene().xTexture

        piece.loadTexture()
        piece.update()
