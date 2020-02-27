from typing import List, Union

from PyQt5.QtCore import pyqtSlot, pyqtSignal

from core2.container.annotation import Annotation, ProjectEntity


class ScreenshotGroup(ProjectEntity):
    onScreenshotGroupChanged = pyqtSignal(object)
    onScreenshotAdded = pyqtSignal(object)
    onScreenshotRemoved = pyqtSignal(object)

    def __init__(self, name = "New Screenshot Group"):
        super(ScreenshotGroup, self).__init__()
        self.name = name
        self.screenshots = []

    @pyqtSlot(str)
    def set_name(self, name):
        self.name = name
        self.onScreenshotGroupChanged.emit(self)

    def add_screenshot(self, s):
        if s not in self.screenshots:
            self.screenshots.append(s)
            s.screenshot_group = self
            self.onScreenshotAdded.emit(s)

    def remove_screenshot(self, s):
        if s in self.screenshots:
            self.screenshots.remove(s)
            s.screenshot_group = None
            self.onScreenshotRemoved.emit(s)


    def serialize(self):
        q = super(ScreenshotGroup, self).serialize()
        q['name'] = self.name
        q['screenshots'] = [s.serialize() for s in self.screenshots]
        return q

    def deserialize(self, q):
        super(ScreenshotGroup, self).deserialize(q)
        self.name = q['name']
        for s in q['screenshots']:
            self.add_screenshot(Screenshot().deserialize(s))
        return self


class Screenshot(Annotation):
    onScreenshotChanged = pyqtSignal(object)

    def __init__(self, time_ms=0):
        super(Screenshot, self).__init__()
        self.screenshot_group = None # type: Union[ScreenshotGroup, None]
        self.time_ms = time_ms

    @pyqtSlot(int)
    def set_start(self, t_start):
        self.time_ms = t_start
        self.onScreenshotChanged.emit(self)

    @pyqtSlot(int)
    def set_end(self, t_end):
        self.time_ms = t_end - 1
        self.onScreenshotChanged.emit(self)

    def get_start(self):
        return self.time_ms

    def get_end(self):
        return self.time_ms + 1

    def serialize(self):
        q = self.__dict__
        q.pop("screenshot_group")
        return q

    def deserialize(self, q):
        for k, v in q.items():
            setattr(self, k, v)
        return self