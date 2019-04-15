from core.gui.ewidgetbase import EDockWidget
from PyQt5 import uic, QtWidgets
from PyQt5.QtWidgets import *
from PyQt5 import uic
from PyQt5.QtCore import Qt, pyqtSignal, pyqtSlot
from PyQt5.QtGui import QColor
from core.data.interfaces import IProjectChangeNotify
import os
from core.gui.python_script_editor import PythonScriptEditor
from core.data.creation_events import VIANEventHandler, ALL_REGISTERED_PIPELINES, get_path_of_pipeline_script, get_name_of_script_by_path
from core.container.project import VIANProject
from core.data.computation import import_module_from_path

class PipelineDock(EDockWidget):
    def __init__(self, parent, event_manager):
        super(PipelineDock, self).__init__(parent, False)
        self.setWindowTitle("Pipeline Manager")
        self.pipeline = PipelineWidget(self, event_manager)
        self.splitter = QSplitter(Qt.Horizontal)
        self.inner.setCentralWidget(self.splitter)
        self.inner.centralWidget().setLayout(QHBoxLayout())

        #self.setWidget(self.inner)
        self.inner.centralWidget().addWidget(self.pipeline)
        self.editor = PythonScriptEditor(self.inner.centralWidget())
        self.inner.centralWidget().layout().addWidget(self.editor)
        self.editor.onReload.connect(self.pipeline.on_reload_scripts)

        self.pipeline.onPipelineActivated.connect(self.on_active_pipeline_changed)

        self.splitter.setStretchFactor(0, 1)
        self.splitter.setStretchFactor(1, 3)

    def on_active_pipeline_changed(self, name):
        script_path = get_path_of_pipeline_script(name)
        if script_path is not None and os.path.isfile(script_path):
            self.editor.load(script_path)


class PipelineWidget(QWidget):
    onPipelineActivated = pyqtSignal(str)
    onPipelineFinalize = pyqtSignal()
    onToComputeChanged = pyqtSignal(bool, bool, bool)

    def __init__(self, parent, event_manager: VIANEventHandler):
        super(PipelineWidget, self).__init__(parent)
        path = os.path.abspath("qt_ui/PipelineWidget.ui")
        uic.loadUi(path, self)

        self.project = None #type: VIANProject

        self.btn_onSegment.setStyleSheet("QPushButton{background-color: rgb(100, 10, 10);}" + "QPushButton:checked{background-color: rgb(10, 100, 10);}")
        self.btn_onScreenshot.setStyleSheet("QPushButton{background-color: rgb(100, 10, 10);}" + "QPushButton:checked{background-color: rgb(10, 100, 10);}")
        self.btn_onAnnotation.setStyleSheet("QPushButton{background-color: rgb(100, 10, 10);}" + "QPushButton:checked{background-color: rgb(10, 100, 10);}")

        self.btn_onSegment.clicked.connect(self.on_update_to_compute)
        self.btn_onScreenshot.clicked.connect(self.on_update_to_compute)
        self.btn_onAnnotation.clicked.connect(self.on_update_to_compute)
        self.btn_Finalize.clicked.connect(self.on_pipeline_finalize)

        self.btn_usePipeline.clicked.connect(self.on_use_pipeline)
        self.current_item = None
        self.all_items = dict()

        self.event_manager = event_manager
        self.on_reload_scripts()

    def on_reload_scripts(self):
        last_selection = None
        if self.current_item is not None:
            last_selection = self.current_item.text()
            self.current_item = None

        self.listWidget_Pipelines.clear()
        self.all_items.clear()
#        self.listWidget_Pipelines = QListWidget()
        for pipeline in ALL_REGISTERED_PIPELINES.keys():
            itm = QListWidgetItem(pipeline)
            self.listWidget_Pipelines.addItem(itm)
            if last_selection is not None and pipeline == last_selection:
                self.listWidget_Pipelines.setCurrentItem(itm)
                self.on_use_pipeline()
            self.all_items[pipeline] = itm

    def on_update_to_compute(self):
        comp_segments = self.btn_onSegment.isChecked()
        comp_annotations = self.btn_onAnnotation.isChecked()
        comp_screenshots = self.btn_onScreenshot.isChecked()

        if self.project is not None:
            self.project.compute_pipeline_settings = dict(segments=comp_segments,
                                                          screenshots=comp_screenshots,
                                                          annotations=comp_annotations)

        self.onToComputeChanged.emit(comp_segments, comp_screenshots, comp_annotations)

    def on_use_pipeline(self):
        if self.current_item is not None:
            self.current_item.setForeground(QColor(69,69,69))

        if self.listWidget_Pipelines.currentItem() is None:
            return

        pipeline_name = self.listWidget_Pipelines.currentItem().text()

        self.current_item = self.listWidget_Pipelines.currentItem()
        if self.current_item is not None:
            self.current_item.setForeground(QColor(69, 200, 69))
            print("Done")

        self.onPipelineActivated.emit(pipeline_name)
        if self.project is not None and pipeline_name in ALL_REGISTERED_PIPELINES:
            self.project.add_pipeline_script(get_path_of_pipeline_script(pipeline_name))
            self.project.active_pipeline_script = get_path_of_pipeline_script(pipeline_name)

    def on_pipeline_finalize(self):
        self.onPipelineFinalize.emit()

    @pyqtSlot(object)
    def on_loaded(self, project:VIANProject):
        for p in project.pipeline_scripts:
            try:
                import_module_from_path(p)
            except Exception as e:
                print("Exception during loading of Script:", e)
        self.on_reload_scripts()
        module_name = get_name_of_script_by_path(project.active_pipeline_script)
        if module_name is not None and module_name in self.all_items:
            self.listWidget_Pipelines.setCurrentItem(self.all_items[module_name])

        self.btn_onSegment.setChecked(project.compute_pipeline_settings['segments'])
        self.btn_onScreenshot.setChecked(project.compute_pipeline_settings['screenshots'])
        self.btn_onAnnotation.setChecked(project.compute_pipeline_settings['annotations'])

        self.on_use_pipeline()
        self.on_update_to_compute()
        self.project = project