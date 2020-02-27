from uuid import uuid4
from PyQt5.QtCore import pyqtSlot, pyqtSignal, QObject


class ProjectEntity(QObject):
    def __init__(self):
        super(ProjectEntity, self).__init__()
        self.uuid = str(uuid4())
        self.notes = ""

        _register_entity(self)

    def __del__(self):
        _unregister_entity(self)

    def serialize(self):
        return dict(uuid=self.uuid, notes=self.notes)

    def deserialize(self, q):
        self.uuid = q['uuid']
        self.notes = q['notes']
        return self


class Annotation(ProjectEntity):
    """ The baseclass of all annotations """
    onClassificationKeywordAdded = pyqtSignal(object)
    onClassificationKeywordRemoved = pyqtSignal(object)

    def __init__(self):
        super(Annotation, self).__init__()
        self.keywords = set()

    def add_tag(self, k):
        self.keywords.add(k)
        self.onClassificationKeywordAdded.emit(k)

    def remove_tag(self, k):
        self.keywords.remove(k)
        self.onClassificationKeywordRemoved.emit(k)

    def get_start(self):
        """ returns the start of the annotation in ms """
        return 0

    def get_end(self):
        """ return s the end of the annotation in ms """
        return 0


_entity_map = dict()


def _register_entity(e: ProjectEntity):
    """ Registers a projectentity in the entity map """
    if e.uuid not in _entity_map:
        _entity_map[e.uuid] = e


def _unregister_entity(e: ProjectEntity):
    """ unegisters a projectentity in the entity map """
    if e.uuid in _entity_map:
        _entity_map.pop(e.uuid)


def get_by_uuid(uuid):
    if uuid in _entity_map:
        return _entity_map[uuid]
    else:
        return None