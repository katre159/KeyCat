from keycat.repository import AbstractButtonRepository
from keycat.database import *
from keycat.models import Shortcut, Template
from keycat.picture_util import convert_picture_to_grayscale, convert_picture_to_numpy_array
from PIL.PngImagePlugin import PngImageFile
from mock import patch
import unittest
import os


class DatabaseTest(unittest.TestCase):
    def setUp(self):
        self.mock_button_repository = AbstractButtonRepository(None)
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

    def test_merge_shortcuts(self):
        shortcut = Shortcut("32,28")
        existing_shortcut = Shortcut("32,28")
        existing_shortcut.id = 2
        merged_shortcut = merge_shortcuts(shortcut, existing_shortcut)
        self.assertEqual(merged_shortcut.id, 2)
        self.assertEqual(merged_shortcut.keycodes, "32,28")

    def test_merge_shortcuts_with_existing(self):
        shortcuts = [Shortcut("32,28"), Shortcut("32,30"), Shortcut("32,29")]
        existing_shortcut1 = Shortcut("32,28")
        existing_shortcut1.id = 1
        existing_shortcut2 = Shortcut("32,29")
        existing_shortcut2.id = 2
        existing_shortcuts = [existing_shortcut1, existing_shortcut2]
        merged_shortcuts = merge_shortcuts_with_existing(shortcuts, existing_shortcuts)
        self.assertEqual(len(merged_shortcuts), 3)
        self.assertEqual(merged_shortcuts[0].id, 1)
        self.assertEqual(merged_shortcuts[0].keycodes, "32,28")
        self.assertEqual(merged_shortcuts[1].id, None)
        self.assertEqual(merged_shortcuts[1].keycodes, "32,30")
        self.assertEqual(merged_shortcuts[2].id, 2)
        self.assertEqual(merged_shortcuts[2].keycodes, "32,29")

    def test_merge_buttons(self):
        program = "test_program"
        old_name = "test_old"
        new_name = "test_button"
        button_id = "test_button_id"
        shortcuts = [Shortcut("32,28"), Shortcut("32,30"), Shortcut("32,29")]
        existing_shortcut1 = Shortcut("32,28")
        existing_shortcut1.id = 1
        existing_shortcut2 = Shortcut("32,29")
        existing_shortcut2.id = 2
        existing_shortcuts = [existing_shortcut1, existing_shortcut2]
        template = Template("121", 100, 100)
        button = Button(button_id, program, new_name, [template], shortcuts)
        existing_button = Button(button_id, program, old_name, [], existing_shortcuts)
        merged_button = merge_buttons(button, existing_button)
        self.assertEqual(len(merged_button.shortcuts), 3)
        self.assertEqual(len(merged_button.templates), 1)
        self.assertEqual(merged_button.templates[0], template)
        self.assertEqual(merged_button.name, new_name)

        self.assertEqual(merged_button.shortcuts[0].id, 1)
        self.assertEqual(merged_button.shortcuts[0].keycodes, "32,28")
        self.assertEqual(merged_button.shortcuts[1].id, None)
        self.assertEqual(merged_button.shortcuts[1].keycodes, "32,30")
        self.assertEqual(merged_button.shortcuts[2].id, 2)
        self.assertEqual(merged_button.shortcuts[2].keycodes, "32,29")

    def test_merge_buttons_with_existing(self):
        program = "test_program"
        button1 = Button("1", program, "", [], [])
        button2 = Button("2", program, "", [], [])
        button3 = Button("3", program, "", [], [])
        buttons = [button1, button3]
        existing_buttons = [button1, button2]

        original = merge_buttons

        with patch('keycat.database.merge_buttons', side_effect=original) as mock:
            merged_buttons, buttons_for_deletion = merge_buttons_with_existing(buttons, existing_buttons)
            mock.assert_called_with(button1, button1)
        self.assertEqual(merged_buttons, [button1, button3])
        self.assertEqual(buttons_for_deletion, [button2])
