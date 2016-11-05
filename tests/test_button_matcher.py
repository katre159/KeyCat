import os
import unittest
import numpy
from mock import MagicMock
from keycat.button_matcher import ButtonMatcher, Click
from keycat.models import ProgramButton
from keycat.repository import AbstractButtonRepository
from keycat.template_matcher import AbstractTemplateMatcher


class ButtonMatcherTest(unittest.TestCase):
    def setUp(self):
        self.mock_button_reposotory = AbstractButtonRepository()
        self.directory = os.path.dirname(os.path.abspath(__file__))
        self.array_shape = (24, 324)
        button_template = numpy.empty(self.array_shape, dtype=numpy.uint8)
        button_templates = [button_template]
        self.button = ProgramButton(button_templates, [])
        buttons = [self.button]
        self.mock_button_reposotory.find_all_buttons = MagicMock(return_value=buttons)
        self.mock_template_matcher = AbstractTemplateMatcher()
        self.mock_template_location = (40, 50)
        self.mock_template_matcher.get_template_location = MagicMock(return_value=self.mock_template_location)
        self.button_matcher = ButtonMatcher(self.mock_template_matcher, self.mock_button_reposotory)

    def test_find_button_on_clicked_position(self):
        found_button = self.button_matcher.find_button_on_clicked_position(Click(40, 50), None)
        self.assertEqual(self.button, found_button)

    def test_template_found_but_not_clicked_on(self):
        found_button = self.button_matcher.find_button_on_clicked_position(Click(500, 50), None)
        self.assertIsNone(found_button)

    def test_template_not_found(self):
        self.mock_template_matcher.get_template_location = MagicMock(return_value=None)
        found_button = self.button_matcher.find_button_on_clicked_position(Click(500, 50), None)
        self.assertIsNone(found_button)

    def test_first_template_not_matching(self):
        button_template = numpy.empty(self.array_shape, dtype=numpy.uint8)
        button_templates = [button_template, button_template]
        button = ProgramButton(button_templates, [])
        buttons = [button]
        self.mock_button_reposotory.find_all_buttons = MagicMock(return_value=buttons)
        self.mock_template_matcher.get_template_location = MagicMock(side_effect=[None, self.mock_template_location])
        found_button = self.button_matcher.find_button_on_clicked_position(Click(40, 50), None)
        self.assertEqual(button, found_button)
