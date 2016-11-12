from keycat.repository import AbstractButtonRepository
from keycat.database import load_buttons_from_config
from keycat.models import Shortcut, Template
from keycat.picture_util import convert_picture_to_grayscale, convert_picture_to_numpy_array
from PIL.PngImagePlugin import PngImageFile
import unittest
import os


class DatabaseTest(unittest.TestCase):
    def setUp(self):
        self.mock_button_reposotory = AbstractButtonRepository(None)
        self.directory = os.path.dirname(os.path.abspath(__file__))
        self.new_tab_template = PngImageFile(
            os.path.join(self.directory, 'data/buttons/chrome/new_tab_template_chrome.png'))
        self.new_tab_template = convert_picture_to_grayscale(self.new_tab_template)
        self.new_tab_template = convert_picture_to_numpy_array(self.new_tab_template)

        self.new_win_template = PngImageFile(
            os.path.join(self.directory, 'data/buttons/chrome/new_windows_template_chrome.png'))
        self.new_win_template = convert_picture_to_grayscale(self.new_win_template)
        self.new_win_template = convert_picture_to_numpy_array(self.new_win_template)

    def test_load_buttons_from_config(self):
        directory = os.path.dirname(os.path.abspath(__file__))
        buttons = load_buttons_from_config(directory, 'data/buttons_config.json')

        self.assertEqual(2, len(buttons))
        first_button = buttons[0]
        second_button = buttons[1]
        self.assertEqual(first_button.program, "chrome")
        self.assertEqual(second_button.program, "chrome2")
        self.assertEqual(first_button.shortcuts, [Shortcut("32,28"), Shortcut("32,78")])
        self.assertEqual(second_button.shortcuts, [Shortcut("32,28")])
        self.assertEqual(first_button.templates, [Template(self.new_tab_template.tobytes(), 24, 324),
                                                  Template(self.new_win_template.tobytes(), 24, 324)])
        self.assertEqual(second_button.templates, [Template(self.new_win_template.tobytes(), 24, 324)])

    def test_load_buttons_from_config_empty_arrays(self):
        directory = os.path.dirname(os.path.abspath(__file__))
        buttons = load_buttons_from_config(directory, 'data/buttons_config_empty.json')
        self.assertEqual(1, len(buttons))
        first_button = buttons[0]
        self.assertEqual(first_button.program, "chrome")
        self.assertEqual(first_button.shortcuts, [])
        self.assertEqual(first_button.templates, [])
