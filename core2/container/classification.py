from typing import List, Union, Dict
from PyQt5.QtCore import pyqtSlot, pyqtSignal

from core2.container.annotation import ProjectEntity, Annotation, get_by_uuid
from core2.container.vocabulary import VocabularyWord, Vocabulary


class ClassificationKeyword(ProjectEntity):
    def __init__(self, voc_word = None, class_obj = None):
        super(ClassificationKeyword, self).__init__()
        self.voc_word_ref = voc_word    # type: VocabularyWord
        self.class_obj_ref = class_obj  # type: ClassificationObject

    def serialize(self):
        return dict(
            voc_word_ref = self.voc_word_ref.uuid,
            class_obj_ref = self.class_obj_ref.uuid
        )

    def deserialize(self, q):
        self.voc_word_ref = get_by_uuid(q['voc_word_ref'])
        self.class_obj_ref = get_by_uuid(q['class_obj_ref'])
        return self


class ClassificationObject(ProjectEntity):
    onClassificationObjectChanged = pyqtSignal(object)
    onVocabularyAdded = pyqtSignal(object)
    onVocabularyRemoved = pyqtSignal(object)

    def __init__(self, name):
        super(ClassificationObject, self).__init__()
        self.name = name
        self.vocabularies_ref = []  # type: List[Vocabulary]
        self.semseg_labels = dict() # type: Dict[str, int]
        self.keywords = []          # type: List[ClassificationKeyword]

    def add_vocabulary(self, v:Vocabulary):
        if v not in self.vocabularies_ref:
            self.vocabularies_ref.append(v)
            for w in v.get_words_plain():
                self.keywords.append(ClassificationKeyword(w, self))
            self.onVocabularyAdded.emit(v)

    def remove_vocabulary(self, v:Vocabulary):
        if v in self.vocabularies_ref:
            self.vocabularies_ref.remove(v)

            to_remove = []
            for kwd in self.keywords:
                if kwd.voc_word_ref.vocabulary == v:
                    to_remove.append(kwd)
            for kwd in self.to_remove:
                self.keywords.remove(kwd)

            self.onVocabularyAdded.emit(v)

    def serialize(self):
        return dict(
            name = self.name,
            vocabularies_ref = [v.uuid for v in self.vocabularies_ref],
            semseg_labels = self.semseg_labels,
            keywords = [k.serialize() for k in self.keywords]
        )

    def deserialize(self, q):
        self.name = q['name']
        self.semseg_labels = q['semseg_labels']

        for v in q['vocabularies_ref']:
            self.vocabularies_ref.append(get_by_uuid(v))
        for k in q['keywords']:
            self.keywords.append(ClassificationKeyword().deserialize(k))

        return self


class Classification(ProjectEntity):
    onClassificationObjectAdded = pyqtSignal(object)
    onClassificationObjectRemoved = pyqtSignal(object)

    def __init__(self, name):
        super(Classification, self).__init__()
        self.name = name
        self.classification_objects = []    # type: List[ClassificationObject]
        self.classification = dict()        # type: Dict[Annotation, List[ClassificationKeyword]]

    def get_keywords(self):
        res = []
        for clobj in self.classification_objects:
            for k, v in clobj.keywords.items():
                res.extend(v)
        return res

    def tag_annotation(self, a:Annotation, k:ClassificationKeyword):

        if a not in self.classification:
            self.classification[a] = []
        self.classification[a].append(k)
        a.add_tag(k)

        pass

    def add_classification_object(self, c:ClassificationObject):
        if c not in self.classification_objects:
            self.classification_objects.append(c)
            self.onClassificationObjectAdded.emit(c)

    def remove_classification_object(self, c:ClassificationObject):
        if c in self.classification_objects:
            self.classification_objects.remove(c)
            self.onClassificationObjectRemoved.emit(c)

    def serialize(self):
        classification = dict()
        for c, k in self.classification.items():
            classification[c.uuid] = [t.uuid for t in k]
        return dict(
            name = self.name,
            classification_objects = [c.serialize() for c in self.classification_objects],
            classification = classification
        )

    def deserialize(self, q):
        pass




