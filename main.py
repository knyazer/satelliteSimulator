from PyQt5 import QtWidgets
from PyQt5.QtCore import QTimer, QFile, QTextStream

from src.design import Ui
from src.engine import Engine
from src.plotter import PlotterEngine

import stylesheet.breeze_resources

import sys
import os

import time

class App(QtWidgets.QMainWindow):
    def __init__(self):
        super(App, self).__init__()

        # Main timer
        self.timer = QTimer(self)

        # Restart function used to init environment
        self.restart(True)

        self.timer.stop()
        self.timer.timeout.connect(self.ui.mainCanvas.animate)
        self.timer.timeout.connect(self.ui.statsCanvas.animate)
        self.timer.timeout.connect(self.engine.update)
        self.timer.start(16)

    def restart(self, firstTime = False):
        self.timer.stop()

        if firstTime:
            self.ui = Ui()
            self.ui.setupUi(self)

        if firstTime:
            self.engine = Engine()
        else:
            # Update all parameters to correct
            self.engine.__init__(
                height = self.ui.heightValue.current,
                radius = self.ui.radiusValue.current,
                mass = self.ui.massValue.current,
                velocity = self.ui.velocityValue.current,
                k = self.ui.kValue.current
            )


        # Engine configuration
        self.ui.mainCanvas.setPaintCallback(self.engine.draw)
        self.ui.mainCanvas.setZoomCallback(self.engine.zoom)
        self.ui.mainCanvas.setDragCallback(self.engine.drag)

        # Plotter configuration
        if firstTime:
            self.plotter = PlotterEngine()
        else:
            self.plotter.__init__()

        self.ui.statsCanvas.setPaintCallback(self.plotter.draw)
        self.engine.setDataCallback(self.plotter.update)

        # Buttons configuration
        self.ui.pauseButton.setCallback(self.engine.start, 0)
        self.ui.pauseButton.setCallback(self.engine.stop,  1)

        self.ui.timeHigherButton.setCallback(self.engine.positiveAccelerate)
        self.ui.timeLowerButton.setCallback(self.engine.negativeAccelerate)

        self.ui.restartButton.setCallback(self.restart)

        # Quality/Performance realtime callback
        self.ui.qualityValue.setCallback(self.engine.setQuality)

        self.timer.start(16)

def main():
    app = QtWidgets.QApplication(sys.argv)
    if os.name != "nt":
        file = QFile(":/dark.qss")
        file.open(QFile.ReadOnly | QFile.Text)
        stream = QTextStream(file)
        app.setStyleSheet(stream.readAll())

    application = App()
    application.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
