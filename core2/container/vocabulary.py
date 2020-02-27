from PyQt5.QtCore import pyqtSlot, pyqtSignal

from core2.container.annotation import ProjectEntity

class Vocabulary(ProjectEntity):
    onVocabularyWordAdded = pyqtSignal(object)
    onVocabularyWordRemoved = pyqtSignal(object)
    onVocabularyChanged = pyqtSignal(object)

    def __init__(self, name = "New Vocabulary", category = "", description=""):
        super(Vocabulary, self).__init__()
        self.name = name

        self.category = category
        self.description = description
        self.words = []

    @pyqtSlot(str)
    def set_name(self, name):
        self.name = name
        self.onVocabularyChanged.emit(self)

    def get_words_plain(self):
        result = []
        for w in self.words:
            w.get_words_plain(result)
        result.extend(self.words)
        return result

    def add_word(self, word, parent = None):
        if parent is None:
            parent = self
        if word not in parent.words:
            word.parent = parent
            parent.append(word)
            word.vocabulary = self
            self.onVocabularyWordAdded.emit(word)

    def remove_word(self, word):
        if word in word.parent.words:
            word.parent.words.remove(word)
            self.onVocabularyWordRemoved.emit(word)


class VocabularyWord(ProjectEntity):
    onVocabularyWordChanged = pyqtSignal(object)

    def __init__(self, name="", parent=None):
        super(VocabularyWord, self).__init__()

        self.name = name
        self.vocabulary = None
        self.parent = parent
        self.words = []

    @pyqtSlot(str)
    def set_name(self, name):
        self.name = name
        self.onVocabularyWordChanged.emit(self)

    def get_words_plain(self, res):
        for c in self.words:
            c.get_words_plain(res)
        res.extend(self.words)
        return res
