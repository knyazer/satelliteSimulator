from src.empty import emptyFunc

class UnitData():
    def __init__(self):
        self.calc = emptyFunc

        self.max = 0
        self.min = 0

        self.multiplier = 1
        self.translate = 0

        self.data = []
        self.dts = []
        self.wholeDts = 0
        self.mergingList = []


    def calculateBy(self, func):
        self.calc = func

    def calculate(self, dt, *args):
        # Update delta time parameter
        self.wholeDts += dt
        self.dts.append(self.wholeDts)

        # Get value of function calculation
        value = self.calc(*args)
        self.data.append(value)

        # Caclulate min and max value for all time
        if (self.max == 0 and self.min == 0):
            self.max = value
            self.min = value

        if value < self.min:
            self.min = value

        if value > self.max:
            self.max = value

        # Calculate size multiplier
        if (self.max != self.min):
            self.multiplier = 1 / (self.max - self.min)

        self.translate = -self.min

    def mergeMultipliers(self, *args):
        self.mergingList = args

    def applyMerge(self):
        if len(self.mergingList) == 0: return

        currentMultiplier = min(min([el.multiplier for el in self.mergingList]), self.multiplier)

        for i in range(len(self.mergingList)):
            self.mergingList[i].multiplier = currentMultiplier

        self.multiplier = currentMultiplier

    def draw(self, painter, w, h, borderSize):
        self.applyMerge()

        l = len(self.data) - 1
        if l < 1: return

        w -= 2 * borderSize
        h -= 2 * borderSize

        # Precalculate step size
        step = w / self.wholeDts

        for i in range(l):
            painter.drawLine(borderSize + self.dts[i + 0] * step, borderSize + h - (self.data[i + 0] + self.translate) * self.multiplier * h,
                             borderSize + self.dts[i + 1] * step, borderSize + h - (self.data[i + 1] + self.translate) * self.multiplier * h)


from src.defaults import G, PLANET_MASS

class PlotterEngine():
    def __init__(self):
        self.stats = {
            "pEnergy": UnitData(),
            "wEnergy": UnitData(),
            "velocity": UnitData(),
        }

        self.stats.get("pEnergy").calculateBy(lambda pos, vel, m: -G * m  * PLANET_MASS / pos.size())
        self.stats.get("wEnergy").calculateBy(lambda pos, vel, m: (-G * m  * PLANET_MASS / pos.size()) + (vel.sqsize() * m / 2))
        self.stats.get("velocity").calculateBy(lambda pos, vel, m: vel.size())

        self.stats.get("wEnergy").mergeMultipliers(self.stats.get("pEnergy"))


        self.renderer = PlotterRenderer()
        self.draw = self.renderer.draw

        # Iterate over all unitData objects
        for graph in self.stats.values():
            self.renderer.addCallback(graph.draw)

    # Update all data values
    def update(self, pos, vel, mass, dt):
        for union in self.stats.values():
            union.calculate(dt, pos, vel, mass)


from PyQt5.QtGui import QBrush, QColor, QPen
from PyQt5.QtCore import Qt

from time import time

class PlotterRenderer():
    def __init__(self):
        # Setup colors
        self.background = QBrush(QColor(48, 36, 48))
        self.colors = [Qt.blue, Qt.green, Qt.red]
        self.borderColor = QPen(QColor(120, 220, 170))

        self.borderStep = 2

        # List for draw callbacks
        self.callbacks = []

    def addCallback(self, callback):
        self.callbacks.append(callback)

    def draw(self, painter, event):
         # Get size and params of the current drawing area
        size = event.rect()

        # Fill background
        painter.fillRect(size, self.background)

        # Get width and height
        w = size.width()
        h = 131

        if (h == 1): return

        # Draw borders
        painter.setPen(self.borderColor)
        painter.drawRect(self.borderStep, self.borderStep, w - self.borderStep * 2, h - self.borderStep * 2)

        # Run graphics callbacks
        for i in range(len(self.callbacks)):
            painter.setPen(self.colors[i])
            self.callbacks[i](painter, w, h, self.borderStep * 2)
