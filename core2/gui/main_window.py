import os

from PyQt5.QtCore import pyqtSignal, Qt
from PyQt5.QtWidgets import QMainWindow, QSplashScreen, QWidget, QFileDialog
from PyQt5 import uic

# DockWidgets
from core2.gui.timeline.timelinedock import TimelineDock
from core2.gui.player.mediaplayerdock import MediaPlayerDock
from core2.gui.docks.screenshot_manager import ShotManager

from core2.gui.signals import VIANSignals

from core2.container.project import VIANProject, MovieDescriptor

class MainWindow(QMainWindow):

    onTimeStep = pyqtSignal(int)
    onUpdateFrame = pyqtSignal(int, int)
    onSegmentStep = pyqtSignal(object)
    currentSegmentChanged = pyqtSignal(int)
    abortAllConcurrentThreads = pyqtSignal()
    onOpenCVFrameVisibilityChanged = pyqtSignal(bool)
    onCorpusConnected = pyqtSignal(object)
    onCorpusDisconnected = pyqtSignal(object)
    currentClassificationObjectChanged = pyqtSignal(object)
    onAnalysisIntegrated = pyqtSignal()

    onProjectOpened = pyqtSignal(object)
    onMovieOpened = pyqtSignal(object)
    onProjectClosed = pyqtSignal()

    onSave = pyqtSignal()

    def __init__(self, loading_screen:QSplashScreen):
        super(MainWindow, self).__init__()
        path = os.path.abspath("qt_ui2/ui_files/main_window.ui")
        uic.loadUi(path, self)
        loading_screen.show()

        self.project = None

        # Init User Interface
        # Empty central widget
        w = QWidget()
        w.setFixedWidth(0)
        self.setCentralWidget(w)

        # Create Dock Widgets
        self.timeline = self.create_dock_widget(TimelineDock, None, position=Qt.BottomDockWidgetArea)
        self.player = self.create_dock_widget(MediaPlayerDock, None, position=Qt.LeftDockWidgetArea)

        self.shot_manager = self.create_dock_widget(ShotManager, None)

        self.signals = VIANSignals(self)

        loading_screen.close()

        self.actionNewProject.triggered.connect(self.create_new_project)
        self.actionPlayPause.triggered.connect(self.player.toggle_play)
        self.show()

    def create_dock_widget(self, t, ret=None, position = Qt.RightDockWidgetArea, align = Qt.Vertical):
        if ret is None:
            ret = t(self)
            self.addDockWidget(position, ret, align)
        else:
            if not ret.visibleRegion().isEmpty():
                ret.hide()
            else:
                ret.show()
                ret.raise_()
                ret.activateWindow()
        return ret



    def create_new_project(self):
        f = QFileDialog.getOpenFileName()[0]
        if not os.path.isfile(f):
            print("Shit")
            return

        self.project = VIANProject()
        self.project.set_media_descriptor(MovieDescriptor(f))
        self.player.open_media(self.project.media_descriptor)
        print("OK")