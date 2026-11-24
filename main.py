import sys

from PySide6 import QtGui
from PySide6.QtCore import Qt
from PySide6.QtWidgets import (QMainWindow,
                               QApplication, 
                               QPushButton, 
                               QWidget, 
                               QHBoxLayout,
                               QVBoxLayout, 
                               QSplitter, QSlider)
import pyqtgraph as pg
import numpy as np


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.freq = None
        self.cos = None
        self.sin = None
        self.splitter = None
        self.plot_widget = None
        self.sin_slider = None
        self.figure_layout = None
        self.figure_widget = None
        self.cos_btn = None
        self.sin_btn = None
        self.settings_layout = None
        self.settings_widget = None
        self.setWindowTitle("Harmonic Viewer")
        self.setupUi()
        self.__create_callbacks()

        self.dt = 1e-3
        self.time = np.arange(0, 1 + self.dt, self.dt)

    def setupUi(self):
        self.settings_widget = QWidget()
        self.settings_layout = QVBoxLayout(self.settings_widget)
        self.sin_btn = QPushButton("sin(t)")
        self.cos_btn = QPushButton("cos(t)")
        self.settings_layout.addWidget(self.sin_btn)
        self.settings_layout.addWidget(self.cos_btn)
        self.settings_layout.addStretch()

        self.figure_widget = QWidget()
        self.figure_layout = QVBoxLayout(self.figure_widget)
        
        self.sin_slider = QSlider(Qt.Orientation.Horizontal)
        self.sin_slider.setMinimum(1)
        self.sin_slider.setMaximum(25)
        self.sin_slider.setValue(1)

        self.cos_slider = QSlider(Qt.Orientation.Horizontal)
        self.cos_slider.setMinimum(1)
        self.cos_slider.setMaximum(25)
        self.cos_slider.setValue(1)

        self.freq = self.sin_slider.value()
        self.sin_slider.hide()
        
        self.plot_widget = pg.PlotWidget()
        self.plot_widget.setBackground(None)
        self.figure_layout.addWidget(self.plot_widget)
        self.figure_layout.addWidget(self.sin_slider)
        self.figure_layout.addWidget(self.cos_slider)

        self.splitter = QSplitter(Qt.Orientation.Horizontal)
        self.splitter.addWidget(self.settings_widget)
        self.splitter.addWidget(self.figure_widget)
        self.splitter.setChildrenCollapsible(False)
        self.splitter.setSizes([200, 800])
        self.splitter.setStretchFactor(0, 0)
        self.splitter.setStretchFactor(1, 1)

        self.setCentralWidget(self.splitter)

    def __create_callbacks(self):
        self.sin_btn.clicked.connect(self.plot_sin)
        self.cos_btn.clicked.connect(self.plot_cos)
        self.sin_slider.valueChanged.connect(self.set_sin_frequency)
        self.cos_slider.valueChanged.connect(self.set_cos_frequency)
    
    def set_sin_frequency(self):
        self.freq = self.sin_slider.value()
        self.plot_sin()

    def set_cos_frequency(self):
        self.freq = self.cos_slider.value()
        self.plot_cos()
    
    def plot_sin(self):
        self.cos_slider.hide()
        self.sin_slider.show()
        self.plot_widget.clear()
        self.sin = np.sin(2 * np.pi * self.time * self.freq)

        self.plot_widget.plot(self.time, self.sin, pen=pg.mkPen(color='red', width=2))

    def plot_cos(self):
        self.sin_slider.hide()
        self.cos_slider.show()
        self.plot_widget.clear()
        self.cos = np.cos(2 * np.pi * self.time * self.freq)
        self.plot_widget.plot(self.time, self.cos, pen=pg.mkPen(color='blue', width=2))


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.setWindowIcon(QtGui.QIcon('./app.ico'))
    window.show()
    sys.exit(app.exec())