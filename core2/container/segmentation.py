from typing import Union, List
from PyQt5.QtCore import pyqtSlot, pyqtSignal

from core2.container.annotation import Annotation, ProjectEntity, _entity_map


class Segmentation(ProjectEntity):

    onSegmentAdded = pyqtSignal(object)
    onSegmentRemoved = pyqtSignal(object)
    onSegmentationChanged = pyqtSignal(object)

    def __init__(self, name = "New Segmentation"):
        super(Segmentation, self).__init__()
        self.name = name
        self.segments = [] #type:List[Segment]

    @pyqtSlot(str)
    def set_name(self, name):
        self.name = name
        self.onSegmentationChanged.emit(self)

    def add_segment(self, segment):
        if segment not in self.segments:
            self.segments.append(segment)
            segment.segmentation = self
            self.onSegmentAdded.emit(segment)

    def remove_segment(self, segment):
        if segment in self.segments:
            self.segments.remove(segment)
            segment.segmentation = None
            self.onSegmentRemoved.emit(segment)

    def serialize(self):
        q = super(Segmentation, self).serialize()
        q['name'] = self.name
        q['segments'] = [s.serialize for s in self.segments]
        return q

    def deserialize(self, q):
        super(Segmentation, self).deserialize(q)
        self.name = q['name']
        for s in q['segments']:
            self.add_segment(Segment().deserialize(s))

class Segment(Annotation):
    onSegmentChanged = pyqtSignal(object)

    def __init__(self, t_start=0, t_end=1, text=""):
        super(Segment, self).__init__()
        self.segmentation = None # type:Union[Segmentation, None]

        if t_start < t_end:
            raise ValueError("Segment: t_start is not smaller than t_end")

        self.t_start = t_start
        self.t_end = t_end

        self.text = text

    @pyqtSlot(int)
    def set_start(self, t_start):
        self.t_start = t_start
        self.onSegmentChanged.emit(self)

    @pyqtSlot(int)
    def set_end(self, t_end):
        self.t_end = t_end
        self.onSegmentChanged.emit(self)

    @pyqtSlot(str)
    def set_text(self, text):
        self.text = text
        self.onSegmentChanged.emit(self)

    def get_start(self):
        return self.t_start

    def get_end(self):
        return self.t_end

    def serialize(self):
        q = self.__dict__
        q.pop("segmentation")
        return q

    def deserialize(self, q):
        for k, v in q.items():
            setattr(self, k, v)
        return self