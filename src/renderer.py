from PyQt5.QtGui import QBrush, QColor
from PyQt5.QtCore import QPointF, Qt

class Renderer():
    def __init__(self, planetRadius, x, y):

        # Colors initialization
        self.background = QBrush(QColor(64, 32, 64))
        self.satelliteColor = QBrush(QColor(64, 192, 64))
        self.planetColor = QBrush(QColor(192, 32, 128))
        self.wayColor = Qt.yellow

        self.satelliteRadius = 10
        self.planetRadius = planetRadius

        self.points = [QPointF(x, y)]

        self.zoomValue = 1
        self.dragX = 0
        self.dragY = 0

    def drawCircle(self, painter, x, y, radius, color):
        painter.setBrush(color)
        if (radius < 7):
            radius = 7
        painter.drawEllipse(int(round(x - radius / 2)), int(round(y - radius / 2)), radius, radius)

    # Callback for zoom event
    def zoom(self, delta, x, y):
        if delta == 1:
            self.zoomValue *= 1.1
        else:
            self.zoomValue /= 1.1

    # Callback for drag event
    def drag(self, dx, dy):
        self.dragX += dx
        self.dragY += dy

    def addPoint(self, x, y):
        if (len(self.points) < 2 or QPointF(x, y) != self.points[-1]):
            self.points.append(QPointF(x, y))

    def draw(self, painter, event):
        size = event.rect() # Get size and params of the current drawing area

        x = self.points[-1].x()
        y = self.points[-1].y()

        # Remove figures borders
        painter.setPen(Qt.NoPen)

        # Fill background
        painter.fillRect(size, self.background)

        # Width and height of the widget
        w = size.width()
        h = size.height()

        dx = w / 2 + self.dragX
        dy = h / 2 + self.dragY

        # Draw satellite
        self.drawCircle(painter, x * self.zoomValue + dx, y * self.zoomValue + dy, self.satelliteRadius * self.zoomValue, self.satelliteColor)

        # Draw central planet
        self.drawCircle(painter, dx, dy, self.planetRadius * self.zoomValue, self.planetColor)

        # Draw satellite way
        painter.setPen(self.wayColor)

        # Fastest way to move a lot of points
        painter.translate(dx, dy)
        for i in range(len(self.points) - 1):
            painter.drawLine(self.points[i] * self.zoomValue, self.points[i + 1] * self.zoomValue)
