import os
import unittest
from PIL.PngImagePlugin import PngImageFile
from keycat.picture_util import convert_picture_to_grayscale, convert_picture_to_numpy_array
from keycat.template_matcher import CCOEFFNORMEDTemplateMatcher


class CCOEFFNORMEDTemplateMatcherTest(unittest.TestCase):
    def setUp(self):
        self.directory = os.path.dirname(os.path.abspath(__file__))
        self.screenshot = PngImageFile(os.path.join(self.directory, 'data/new_tab_selected_chrome.png'))
        self.template = PngImageFile(os.path.join(self.directory, 'data/new_tab_template_chrome.png'))
        self.template = convert_picture_to_grayscale(self.template)
        self.template = convert_picture_to_numpy_array(self.template)
        self.template_mather = CCOEFFNORMEDTemplateMatcher()

    def test_template_matching(self):
        found_loc = self.template_mather.get_template_location(self.template, self.screenshot)
        expected_location = (47, 60)
        self.assertEqual(expected_location, found_loc)

    def test_not_selected(self):
        self.screenshot_not_selected = PngImageFile(os.path.join(self.directory, 'data/new_window_selected_chrome.png'))
        found_loc = self.template_mather.get_template_location(self.template, self.screenshot_not_selected)
        self.assertIsNone(found_loc)
