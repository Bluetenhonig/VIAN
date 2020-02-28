from .vian_dock import VIANDockWidget


class ShotManager(VIANDockWidget):
    def __init__(self, main_window):
        super(ShotManager, self).__init__(main_window, "Screenshot Manager")
