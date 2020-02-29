import sys
import os
import cv2

import vlc

from PyQt5 import QtWidgets, QtGui
from PyQt5.QtWidgets import QWidget, QFrame, QHBoxLayout, QVBoxLayout
from PyQt5.QtCore import pyqtSignal, pyqtSlot, QTimer, Qt

from core2.gui.docks.vian_dock import VIANDockWidget
from core2.container.media_descriptor import MediaDescriptor, MovieDescriptor, ImagesDescriptor


class VideoPlayer(QFrame):
    timeChanged = pyqtSignal(int)
    movieOpened = pyqtSignal()
    started = pyqtSignal()
    stopped = pyqtSignal()

    def __init__(self, parent):
        super(VideoPlayer, self).__init__(parent)

    def open_movie(self, m: MovieDescriptor):
        pass

    def play(self):
        pass

    def pause(self):
        pass

    def toggle_play(self):
        pass

    def set_rate(self, fps):
        pass

    def get_rate(self):
        pass

    def get_subtitles(self):
        pass

    def set_subtitle(self, s):
        pass

    def next_frame(self):
        pass

    def previous_frame(self):
        pass

    def set_media_time(self, time):
        pass

    def get_media_time(self):
        pass

    def set_volume(self, volume):
        pass

    def get_volume(self):
        pass

    def set_mute(self, mute):
        pass

    def get_mute(self):
        pass


class PlayerVLC(VideoPlayer):
    def __init__(self, parent):
        super(PlayerVLC, self).__init__(parent)
        self.vlc_arguments = "--no-keyboard-events --no-mouse-events --no-embedded-video"  # --verbose 0 --quiet
        self.media_player = None
        self.vlc_instance = None

        self.movie_path = ""
        self.media = None

        self.playing = False

        self.vboxlayout = QVBoxLayout()
        self.setLayout(self.vboxlayout)

        if sys.platform == "darwin":  # for MacOS
            self.videoframe = QtWidgets.QMacCocoaViewContainer(0, None)
        else:
            self.videoframe = QFrame()

        self.videoframe.setParent(self)
        self.palette = self.videoframe.palette()
        self.palette.setColor(QtGui.QPalette.Window, QtGui.QColor(100, 0, 0))
        self.videoframe.setPalette(self.palette)
        self.videoframe.setAutoFillBackground(True)
        self.layout().addWidget(self.videoframe)

        self.init_vlc()
        # self.pause_timer = QTimer()
        # self.pause_timer.setInterval(1000)
        # self.pause_timer.setSingleShot(True)
        # self.pause_timer.timeout.connect(self.pause)

    # *** EXTENSION METHODS *** #
    def init_vlc(self):
        self.vlc_instance = vlc.Instance(self.vlc_arguments)
        self.media_player = self.vlc_instance.media_player_new()
        self.init_ui()

    def release_player(self):
        if self.media_player is not None:
            self.media_player.set_pause(-1)

        if self.media is not None:
            self.media.release()
            self.media = None

        if self.vlc_instance is not None:
            self.vlc_instance.release()

        self.vlc_instance = None
        self.media_player = None
        self.media = None

    def get_frame(self):
        # fps = self.media_player.get_fps()
        pos = float(self.get_media_time()) / 1000 * self.fps
        vid = cv2.VideoCapture(self.movie_path)
        vid.set(cv2.CAP_PROP_POS_FRAMES, pos)
        ret, frame = vid.read()
        return frame

    def init_ui(self):
        # In this widget, the video will be drawn
        # self.videoframe = QtWidgets.QFrame()

        # the media player has to be 'connected' to the QFrame
        # (otherwise a video would be displayed in it's own window)
        # this is platform specific!
        # you have to give the id of the QFrame (or similar object) to
        # vlc, different platforms have different functions for this
        if sys.platform.startswith('linux'):  # for Linux using the X Server
            self.media_player.set_xwindow(self.videoframe.winId())
        elif sys.platform == "win32":  # for Windows
            self.media_player.set_hwnd(self.videoframe.winId())
        elif sys.platform == "darwin":  # for MacOS
            self.media_player.set_nsobject(int(self.videoframe.winId()))
            self.videoframe.setAttribute(Qt.WA_TransparentForMouseEvents, True)

    def get_size(self):
        return self.media_player.video_get_size()

    def get_subtitles(self):
        subs = self.media_player.video_get_spu_description()
        return subs

    def set_subtitle(self, index):
        self.media_player.video_set_spu(index)

    def open_movie(self, m: MovieDescriptor):
        if self.media_player is not None:
            self.media_player.set_pause(-1)

        if self.vlc_instance is None:
            self.init_vlc()

        self.movie_path = m.movie_path
        self.media = self.vlc_instance.media_new(self.movie_path)

        # put the media in the media player
        self.media_player.set_media(self.media)

        # parse the metadata of the file
        self.media.parse()

        # Running the movie, to ensure the initial values can be read by the VLC framework
        self.play()

        # Wait for a little
        # time.sleep(0.5)

        # self.set_initial_values()

        self.set_media_time(0)
        self.movieOpened.emit()
        print("Movie Opened Done")

    def toggle_play(self):
        if not self.is_playing():
            self.play()
        else:
            self.pause()
        return self.is_playing()

    def play(self):
        if self.media_player is None:
            return

        self.media_player.play()
        self.playing = True
        self.started.emit()


    def pause(self):
        if self.media_player is None:
            return
        self.media_player.set_pause(-1)
        self.playing = False
        self.stopped.emit()

    def is_playing(self):
        """
        :return: bool
        """
        return self.playing

    def next_frame(self):
        if self.media_player is None:
            return
        self.media_player.next_frame()

    def previous_frame(self):
        pass

    def set_media_time(self, time):
        if self.media_player is None:
            return
        self.media_player.set_time(int(time))
        self.timeChanged.emit(time)

    def get_media_time(self):
        if self.media_player is None:
            return 0
        return self.media_player.get_time()

    def set_rate(self, rate):
        if self.media_player is None:
            return 1.0
        self.media_player.set_rate(float(rate))

    def get_rate(self):
        if self.media_player is None:
            return 1.0
        return self.media_player.get_rate()

    def set_volume(self, volume):
        if self.media_player is None:
            return
        self.media_player.audio_set_volume(volume)

    def get_volume(self):
        if self.media_player is None:
            return 0
        return self.media_player.audio_get_volume()

    def set_mute(self, mute):
        if self.media_player is None:
            return
        self.media_player.audio_set_mute(bool(mute))

    def get_mute(self):
        if self.media_player is None:
            return 0
        return self.media_player.audio_get_mute()

    def stop(self):
        if self.media_player is None:
            return

        print("Stopping and Release")
        self.media_player.stop()
        self.media_player.set_pause(-1)
        self.playing = False

        if self.media is not None:
            print("Release")
            self.media.release()
            self.media = None