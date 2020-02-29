
from PyQt5.QtWidgets import QWidget
from PyQt5.QtCore import pyqtSlot

from core2.gui.docks.vian_dock import VIANDockWidget

from core2.gui.player.video_player import VideoPlayer, PlayerVLC
from core2.container.media_descriptor import MediaDescriptor, MovieDescriptor, ImagesDescriptor


class MediaPlayerDock(VIANDockWidget):
    def __init__(self, main_window):
        super(MediaPlayerDock, self).__init__(main_window, "Media Player")

        self.frame = PlayerVLC(self)
        self.setWidget(self.frame)

    def open_media(self, descriptor:MediaDescriptor):
        if isinstance(descriptor, MovieDescriptor):
            if not isinstance(self.frame, PlayerVLC):
                self.frame = PlayerVLC(self)
                self.setWidget(self.frame)
            self.frame.open_movie(descriptor)
            self.frame.play()

    @pyqtSlot()
    def toggle_play(self):
        if isinstance(self.frame, VideoPlayer):
            self.frame.toggle_play()


