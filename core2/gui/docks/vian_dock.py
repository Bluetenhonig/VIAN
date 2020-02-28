from PyQt5.QtWidgets import QDockWidget, QMainWindow, QWidget


class VIANDockWidget(QDockWidget):
    def __init__(self, main_window, title = "New Dock"):
        super(VIANDockWidget, self).__init__(main_window)
        self.main_window = main_window
        self.setWindowTitle(title)

        self._mw = None

    def setWidget(self, widget: QWidget) -> None:
        if self.widget() is None:
            self._mw = QMainWindow()
            super(VIANDockWidget, self).setWidget(self._mw)
            self._mw.setCentralWidget(widget)

    def get_settings(self):
        return dict()

    def apply_settings(self, d):
        for k, val in d.items():
            setattr(self, k, val)