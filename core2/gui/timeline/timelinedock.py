import os

import numpy as np


from PyQt5.QtWidgets import QWidget, QLabel
from PyQt5.QtGui import QColor, QPixmap, QImage, QGradient
from PyQt5.QtCore import QPoint, QPointF, QTimer, pyqtSignal, pyqtSlot, Qt, QRectF, QRect

from PyQt5 import QtCore, QtWidgets, QtGui, uic

from core2.container.project import Segmentation, Segment
from core2.gui.docks.vian_dock import VIANDockWidget
from core2.gui.timeline.timeline_dataset import TimelineDataset

from core.data.computation import ms_to_string, ms_to_frames, frame2ms

class TimelineDock(VIANDockWidget):
    def __init__(self, main_window):
        super(TimelineDock, self).__init__(main_window, "Timeline")


class Timeline(QtWidgets.QWidget):
    def __init__(self, parent):
        super(Timeline, self).__init__(parent)
        self.entries = []


class TimelineControl(QWidget):
    def __init__(self, parent):
        super(TimelineControl, self).__init__(parent)


class TimelineBar(QWidget):
    def __init__(self, parent):
        super(TimelineBar, self).__init__(parent)


class TimeBar(QWidget):
    def __init__(self, parent):
        super(TimeBar, self).__init__(parent)


class TimeScrubber(QWidget):
    def __init__(self, parent):
        super(TimeScrubber, self).__init__(parent)