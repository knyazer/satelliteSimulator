from PyQt5.QtGui import QPainter
from PyQt5.QtWidgets import QWidget, QToolButton, QLineEdit, QSlider
from PyQt5.QtCore import Qt

from src.empty import emptyFunc

import math

class Slider(QSlider):
    def __init__(self, parent, min, max):
        super(Slider, self).__init__(parent)

        # Startup configuration
        self.setMinimum(min)
        self.setMaximum(max)
        self.setValue(math.sqrt(min * max))

        self.callback = emptyFunc

    def setCallback(self, callback):
        self.callback = callback
        self.callback(self.value())

    def mouseMoveEvent(self, event):
        super(Slider, self).mouseMoveEvent(event)

        # Update current value
        self.callback(self.value())

# Wrapper for line edit parameters
class LineEdit(QLineEdit):
    def __init__(self, parent, default = 0):
        super(LineEdit, self).__init__(parent)

        self.current = default
        self.setText(str(self.current))

    def keyPressEvent(self, event):
        super(LineEdit, self).keyPressEvent(event)
        self.current = self.text()

# Wrapper for tool button
class ToolButton(QToolButton):
    def __init__(self, parent, *states):
        super(ToolButton, self).__init__(parent)

        # Set default text
        self.setText(states[0])

        # Setup states and callbacks list
        self.states = states
        self.callbacks = [emptyFunc() for _ in states]

        # Setup current state index
        self.stateIndex = 0

        # Connect click event
        self.clicked.connect(self.onClick)

    def onClick(self, event):
        self.stateIndex += 1
        index = self.stateIndex % len(self.states)

        # Set current text
        self.setText(self.states[index])

        # Start specific callback
        self.callbacks[index]()

    def setCallback(self, callback, index = 0):
        self.callbacks[index] = callback

# Wrapper for widget with canvas
class CanvasWidget(QWidget):
    def __init__(self, parent):
      super(CanvasWidget, self).__init__(parent)
      self.setMouseTracking(True)

      self.pressed = False

      self.paintCallback = emptyFunc
      self.zoomCallback = emptyFunc
      self.dragCallback = emptyFunc

    def setPaintCallback(self, callback):
        self.paintCallback = callback

    def setZoomCallback(self, callback):
        self.zoomCallback = callback

    def setDragCallback(self, callback):
        self.dragCallback = callback

    def wheelEvent(self, event):
        delta = event.angleDelta().y()

        if delta > 0:
            delta = 1
        if delta < 0:
            delta = -1

        self.zoomCallback(delta, event.x(), event.y())

    def mouseMoveEvent(self, event):
        if event.buttons() == Qt.LeftButton:
            x = event.x()
            y = event.y()

            if self.pressed == False:
                self.oldx = x
                self.oldy = y

            self.pressed = True

            self.dragCallback(x - self.oldx, y - self.oldy)

            self.oldx = x
            self.oldy = y

        else:
            self.pressed = False

    def animate(self):
        self.repaint()

    def paintEvent(self, event):
        painter = QPainter()

        painter.begin(self)
        painter.setRenderHint(QPainter.Antialiasing)

        self.paintCallback(painter, event)

        painter.end()
