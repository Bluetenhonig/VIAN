import unittest
import os
import cv2

from core2.container.project import VIANProject

uuid = "83646205-fcb7-4311-8bb7-2c5a3a7feaa4"
PROJECT = "C:\\Users\\gaude\\Documents\\VIAN\\projects\\TemplateProject22\\TemplateProject22.eext"
SETTINGS_PATH = "settings.json"

class TestSerialization(unittest.TestCase):
    def setUp(self) -> None:
        os.mkdir("data")

    def tearDown(self) -> None:
        shutil.rmtree("data")

    def test_check_project_existence(self):
        with VIANProject().load_project(path=PROJECT) as project: