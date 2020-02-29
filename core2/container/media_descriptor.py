from PyQt5.QtCore import pyqtSlot, pyqtSignal

from core2.container.annotation import ProjectEntity


class MediaDescriptor(ProjectEntity):
    """ Baseclass for all media descriptors """
    def __init__(self):
        super(MediaDescriptor, self).__init__()
        self.meta_data = dict()


class MovieDescriptor(MediaDescriptor):
    """ A Media Descriptor for a movie file """
    def __init__(self, movie_path = "", movie_title = "", duration=1000):
        super(MovieDescriptor, self).__init__()
        self.movie_path = movie_path
        self.movie_title = movie_title
        self.duration = duration


class ImagesDescriptor(MediaDescriptor):
    """ A media descriptor for a list of images """
    def __init__(self):
        super(ImagesDescriptor, self).__init__()
        self.images = []


class Image(ProjectEntity):
    def __init__(self, file_path):
        super(Image, self).__init__()
        self.file_path = file_path
        self.meta_data = dict()