from typing import List, Union, Dict

from uuid import uuid4

from PyQt5.QtCore import pyqtSlot, pyqtSignal, QObject

from core2.container.annotation import ProjectEntity
from core2.container.screenshot import Screenshot, ScreenshotGroup
from core2.container.segmentation import Segment, Segmentation
from core2.container.vocabulary import Vocabulary, VocabularyWord
from core2.container.classification import Classification, ClassificationObject, ClassificationKeyword
from core2.container.media_descriptor import MediaDescriptor


class VIANProject(QObject):
    onScreenshotGroupAdded = pyqtSignal(object)
    onScreenshotGroupRemoved = pyqtSignal(object)

    onSegmentationAdded = pyqtSignal(object)
    onSegmentationRemoved = pyqtSignal(object)

    onClassificationAdded = pyqtSignal(object)
    onClassificationRemoved = pyqtSignal(object)

    onProjectChanged = pyqtSignal(object)

    def __init__(self, name = "New Project"):
        super(VIANProject, self).__init__()
        self.uuid = str(uuid4())
        self.name = name
        self.file_path = None
        self.file_dir = None

        self.hdf5_file = None

        self.media_descriptor = None    # type: Union[MediaDescriptor, None]

        self.screenshot_groups = []     # type: List[ScreenshotGroup]
        self.segmentations = []         # type: List[Segmentation]
        # self.svg_annotation_groups = []

        self.classifications = []       # type: List[Classification]
        self.authors = []               # type: List[Contributor]

        self.entity_map = dict()        # type: Dict[str, ProjectEntity]

    def add_segmentation(self, s:Segmentation):
        """ Adds a segmentation to the project, dispatches a onSegmentationAdded signal"""
        if s not in self.segmentations:
            self.segmentations.append(s)
            self.onSegmentationAdded.emit(s)

    def remove_segmentation(self, s:Segmentation):
        """ removes a segmentation from the project, dispatches a onSegmentationRemoved signal """
        if s in self.segmentations:
            self.segmentations.remove(s)
            self.onSegmentationRemoved.emit(s)

    def add_screenshot_group(self, s:ScreenshotGroup):
        """ Adds a screenshot group to the project, dispatches a onScreenshotGroupAdded signal"""
        if s not in self.screenshot_groups:
            self.screenshot_groups.append(s)
            self.onScreenshotGroupAdded.emit(s)

    def remove_screenshot_group(self, s:ScreenshotGroup):
        """ removes a screenshot group from the project, dispatches a onScreenshotGroupRemoved signal """
        if s in self.screenshot_groups:
            self.screenshot_groups.remove(s)
            self.onScreenshotGroupRemoved.emit(s)

    def save(self):
        d = dict(
            uuid = self.uuid,
            name = self.name,
            file_path = self.file_path,
            file_dir = self.file_dir,
            screenshot_groups = [s.serialize() for s in self.screenshot_groups],
            segmentations = [s.serialize() for s in self.segmentations],
            classifications = [s.serialize() for s in self.classifications],
            authors=[s.serialize() for s in self.authors]
        )
        return d

    def load(self, d):
        self.uuid = str(uuid4())
        self.name = d['name']
        self.file_path = d['file_path']
        self.file_dir = d['file_dir']

        self.hdf5_file = None

        # self.media_descriptor = MediaDescriptor().deserialize(d['media_descriptor'])

        for q in d['screenshot_groups']:
            self.add_screenshot_group(ScreenshotGroup().deserialize(q))
        for q in d['segmentations']:
            self.add_segmentation(Segmentation().deserialize(q))

        # self.svg_annotation_groups = []

        # self.classifications = []  # type: List[Classification]
        # self.authors = []  # type: List[Contributor]
        #
        # self.entity_map = dict()  # type: Dict[str, ProjectEntity]

        pass


class Contributor:
    def __init__(self, name = "New Contributor"):
        self.uuid = str(uuid4())
        self.name = name



if __name__ == '__main__':
    v = VIANProject("Some Project")
    g1 = ScreenshotGroup()
    v.add_screenshot_group(g1)
    g1.add_screenshot(Screenshot(10))
    g1.add_screenshot(Screenshot(20))


    q = v.save()
    v.load(q)