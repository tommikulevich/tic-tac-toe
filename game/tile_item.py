from PySide2.QtCore import QRectF
from PySide2.QtGui import QPixmap, QPen, QColor, QFont, Qt
from PySide2.QtWidgets import QGraphicsItem, QMenu, QAction


class TileItem(QGraphicsItem):
    def __init__(self, x, y, size=200):
        super().__init__()
        self.setPos(x * size, y * size)
        self.size = size

        self.texture = QPixmap(":/field/standard")
        self.number = y * 3 + x + 1
        self.focused = False    # when controlling using the arrows

    def boundingRect(self):
        return QRectF(0, 0, self.size, self.size)

    def paint(self, painter, option, widget=None):
        # Drawing a texture
        if self.focused:
            painter.setBrush(QColor(122, 183, 100))
            painter.setPen(Qt.NoPen)
            painter.drawRect(self.boundingRect())
        else:
            painter.drawPixmap(0, 0, self.size, self.size, self.texture)

        # Drawing borders
        pen = QPen()
        pen.setWidth(1)
        pen.setColor(QColor(0, 0, 0))
        painter.setPen(pen)
        painter.drawRect(self.boundingRect())

        # Drawing a text in a corner
        font = QFont()
        font.setPointSize(self.size // 20)
        painter.setFont(font)
        pen.setColor(QColor(222, 49, 99))
        painter.setPen(pen)
        numRect = QRectF(5, 5, self.size, self.size)
        painter.drawText(numRect, Qt.AlignLeft | Qt.AlignTop, str(self.number))

    def contextMenuEvent(self, event):
        # Menu to change the field style
        menu = QMenu()

        boardStyleMenu = QMenu("Change board style", menu)
        standardAction = QAction("Standard", boardStyleMenu)
        rockAction = QAction("Rock", boardStyleMenu)
        woodAction = QAction("Wood", boardStyleMenu)

        boardStyleMenu.addAction(standardAction)
        boardStyleMenu.addAction(rockAction)
        boardStyleMenu.addAction(woodAction)
        menu.addMenu(boardStyleMenu)

        standardAction.triggered.connect(lambda: self.changeBoardTexture("standard"))
        rockAction.triggered.connect(lambda: self.changeBoardTexture("rock"))
        woodAction.triggered.connect(lambda: self.changeBoardTexture("wood"))

        menu.exec_(event.screenPos())

    def changeBoardTexture(self, boardStyle):
        [self.updateTileItem(item, boardStyle) for item in self.scene().items() if isinstance(item, TileItem)]

    @staticmethod
    def updateTileItem(tile, boardStyle):
        tile.texture = f":/field/{boardStyle}"
        tile.update()
