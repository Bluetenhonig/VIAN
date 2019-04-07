"""
This file contains the decorators for VIAN's 
event system. All functions decorated with the respective decorators can be used 
as within VIAN to be called once a selector is created. 
"""

from PyQt5.QtCore import QObject, pyqtSlot, pyqtSignal
from PyQt5.QtWidgets import QMessageBox
import traceback
import cv2

EVENT_C_SEGMENT =       dict(on_segment_created = None)
EVENT_C_SCREENSHOT =    dict(on_screenshot_created = None)
EVENT_C_ANNOTATION =    dict(on_annotation_created = None)

class VIANEventHandler(QObject):
    onException = pyqtSignal(str)
    def __init__(self, parent):
        super(VIANEventHandler, self).__init__(parent)
        self.main_window = parent
        self.project = None

    @pyqtSlot(object)
    def set_project(self, project):
        self.project = project

        # Hook the project to the events
        self.project.onScreenshotAdded.connect(self.run_on_screenshot_created_event)
        self.project.onAnnotationAdded.connect(self.run_on_annotation_created_event)
        self.project.onSegmentAdded.connect(self.run_segment_created_event)


    @pyqtSlot(object)
    def run_segment_created_event(self, segment):
        try:
            cap = cv2.VideoCapture(self.project.movie_descriptor.movie_path)
            if EVENT_C_SEGMENT['on_segment_created'] is None:
                return
            EVENT_C_SEGMENT['on_segment_created'](self.project, segment, cap)
        except Exception as e:
            self.onException.emit(traceback.format_exc())

    @pyqtSlot(object)
    def run_on_screenshot_created_event(self, screenshot):
        if EVENT_C_SCREENSHOT['on_screenshot_created'] is None:
            return
        try:
            EVENT_C_SCREENSHOT['on_screenshot_created'](self.project, screenshot, None)
        except Exception as e:
            self.onException.emit(traceback.format_exc())

    @pyqtSlot(object)
    def run_on_annotation_created_event(self, annotation):
        if EVENT_C_ANNOTATION['on_annotation_created'] is None:
            return
        try:
            EVENT_C_ANNOTATION['on_annotation_created'](self.project, annotation, None)
        except Exception as e:
            self.onException.emit(traceback.format_exc())




def segment_created_event(func):
    """Register a function as a plug-in"""
    EVENT_C_SEGMENT[func.__name__] = func
    return func


def screenshot_created_event(func):
    """Register a function as a plug-in"""
    EVENT_C_SCREENSHOT[func.__name__] = func
    return func


def annotation_created_event(func):
    """Register a function as a plug-in"""
    EVENT_C_ANNOTATION[func.__name__] = func
    return func


@segment_created_event
def default_segment_c_inform(project, segment, capture):
    print("Segment Created")

@screenshot_created_event
def default_screenshot_c_inform(project, screenshot, img):
    print("Screenshot Created")

@annotation_created_event
def default_annotation_c_inform(project, annotation, sub_img):
    print("Annotation Created")