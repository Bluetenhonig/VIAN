from PyQt5.QtWidgets import QFileDialog,QDialog, QComboBox, QFrame, QFormLayout, QHBoxLayout, QMessageBox
from PyQt5 import uic
from core.data.importers import import_elan_segmentation, get_elan_segmentation_identifiers
from core.gui.ewidgetbase import EDialogWidget
from core.data.enums import ScreenshotNamingConventionOptions, ImageType, get_enum
import os
import cv2

class DialogScreenshotExporter(EDialogWidget):
    def __init__(self, parent, manager):
        super(DialogScreenshotExporter, self).__init__(parent, parent)
        path = os.path.abspath("qt_ui/DialogScreenshotExport.ui")
        uic.loadUi(path, self)
        self.manager = manager
        self.folder_path = ""
        self.visibility = False
        self.override_visibility = False

        self.types = [(e.name) for e in ImageType]

        self.checkBox_OverrideV.stateChanged.connect(self.on_override_visibility_changed)
        self.checkBox_Visibility.setEnabled(self.override_visibility)
        self.cB_ImageFormat.addItems(self.types)

        self.folder_path = self.main_window.project.folder + self.main_window.settings.DIR_SCREENSHOTS
        self.lineEdit_Folder.setText(self.folder_path)
        self.lineEdit_Folder.editingFinished.connect(self.on_edit_path_finished)


        self.btn_Browse.clicked.connect(self.on_browse)
        self.btn_Cancel.clicked.connect(self.on_cancel)
        self.btn_OK.clicked.connect(self.on_export)

    def on_override_visibility_changed(self):
        self.override_visibility = self.checkBox_OverrideV.isChecked()
        self.checkBox_Visibility.setEnabled(self.override_visibility)

    def on_browse(self):
        self.folder_path = QFileDialog.getExistingDirectory()
        self.lineEdit_Folder.setText(self.folder_path)

    def on_edit_path_finished(self):
        self.folder_path =  self.lineEdit_Folder.text()

    def on_export(self):
        path = self.folder_path
        visibility = self.visibility
        image_type = get_enum(ImageType,self.types[self.cB_ImageFormat.currentIndex()])
        quality = self.QualitySlider.value()
        if not self.override_visibility:
            visibility = None
        self.manager.export_screenshots(path, visibility, image_type, quality)
        self.close()

    def on_cancel(self):
        self.close()

