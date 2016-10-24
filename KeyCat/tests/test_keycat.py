import unittest
import os
from keycat.picture_util import *
from unittest.mock import MagicMock
from keycat.events import EventReceiver
from keycat.mouse_events import FullscreenMouseEventCreator, MouseEventListener, AbstractMouseEventCreator, \
    MouseEvent, FixedSizeScreenshotEventCreator, FixedSizeScreenshotSizeError
from keycat.screen import ScreenshotTaker, ScreenManager
from keycat.keyboard_events import KeyboardListener, KeyboardStateManager, KeyboardStateChangedEvent
from keycat.template_matcher import CCOEFFNORMEDTemplateMatcher, AbstractTemplateMatcher
from PIL.PngImagePlugin import PngImageFile
from keycat.repository import AbstractButtonRepository
from keycat.models import ProgramButton
from keycat.button_matcher import ButtonMatcher, Click
import numpy


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


class FullscreenMouseEventCreatorTest(unittest.TestCase):
    def setUp(self):
        self.mock_screenshot_taker = ScreenshotTaker
        self.mock_screenshot_taker.take_full_screenshot = MagicMock(return_value=None)
        self.mouse_event_creator = FullscreenMouseEventCreator(self.mock_screenshot_taker)

    def test_get_mouse_event(self):
        event = self.mouse_event_creator.get_mouse_event(10, 15)
        self.mock_screenshot_taker.take_full_screenshot.assert_called_with()
        self.assertEqual(event.click_x, 10)
        self.assertEqual(event.click_y, 15)


class FixedSizeScreenshotEventCreatorTest(unittest.TestCase):
    def setUp(self):
        self.mock_screenshot_taker = ScreenshotTaker
        self.mock_screenshot_taker.take_full_screenshot = MagicMock(return_value=None)
        self.mock_screenshot_taker.take_fixed_size_screen_shot = MagicMock(return_value=None)
        self.mock_screen_manager = ScreenManager()
        self.mock_screen_manager.get_screen_size = MagicMock(return_value=(1900, 975))
        self.mouse_event_creator = FixedSizeScreenshotEventCreator(self.mock_screenshot_taker, self.mock_screen_manager,
                                                                   300, 300)

    def test_get_mouse_event_click_middle(self):
        event = self.mouse_event_creator.get_mouse_event(500, 600)
        self.mock_screenshot_taker.take_full_screenshot.assert_not_called()
        self.mock_screenshot_taker.take_fixed_size_screen_shot.assert_called_with(bbox=(350.0, 450.0, 650.0, 750.0))
        self.assertEqual(event.click_x, 150.0)
        self.assertEqual(event.click_y, 150.0)

    def test_get_mouse_event_click_lower_limit(self):
        event = self.mouse_event_creator.get_mouse_event(500, 900)
        self.mock_screenshot_taker.take_full_screenshot.assert_not_called()
        self.mock_screenshot_taker.take_fixed_size_screen_shot.assert_called_with(bbox=(350.0, 675.0, 650.0, 975.0))
        self.assertEqual(event.click_x, 150.0)
        self.assertEqual(event.click_y, 225.0)

    def test_get_mouse_event_click_upper_limit(self):
        event = self.mouse_event_creator.get_mouse_event(500, 50)
        self.mock_screenshot_taker.take_full_screenshot.assert_not_called()
        self.mock_screenshot_taker.take_fixed_size_screen_shot.assert_called_with(bbox=(350.0, 0, 650.0, 300))
        self.assertEqual(event.click_x, 150.0)
        self.assertEqual(event.click_y, 50.0)

    def test_get_mouse_event_click_left_limit(self):
        event = self.mouse_event_creator.get_mouse_event(50, 600)
        self.mock_screenshot_taker.take_full_screenshot.assert_not_called()
        self.mock_screenshot_taker.take_fixed_size_screen_shot.assert_called_with(bbox=(0.0, 450.0, 300.0, 750.0))
        self.assertEqual(event.click_x, 50.0)
        self.assertEqual(event.click_y, 150.0)

    def test_get_mouse_event_click_right_limit(self):
        event = self.mouse_event_creator.get_mouse_event(1800, 600)
        self.mock_screenshot_taker.take_full_screenshot.assert_not_called()
        self.mock_screenshot_taker.take_fixed_size_screen_shot.assert_called_with(bbox=(1600, 450.0, 1900, 750.0))
        self.assertEqual(event.click_x, 200.0)
        self.assertEqual(event.click_y, 150.0)

    def test_get_mouse_event_click_left_upper_limit(self):
        event = self.mouse_event_creator.get_mouse_event(50, 50)
        self.mock_screenshot_taker.take_full_screenshot.assert_not_called()
        self.mock_screenshot_taker.take_fixed_size_screen_shot.assert_called_with(bbox=(0.0, 0.0, 300.0, 300.0))
        self.assertEqual(event.click_x, 50.0)
        self.assertEqual(event.click_y, 50.0)

    def test_get_mouse_event_click_right_upper_limit(self):
        event = self.mouse_event_creator.get_mouse_event(1800, 50)
        self.mock_screenshot_taker.take_full_screenshot.assert_not_called()
        self.mock_screenshot_taker.take_fixed_size_screen_shot.assert_called_with(bbox=(1600.0, 0.0, 1900.0, 300.0))
        self.assertEqual(event.click_x, 200.0)
        self.assertEqual(event.click_y, 50.0)

    def test_get_mouse_event_click_left_lower_limit(self):
        event = self.mouse_event_creator.get_mouse_event(50, 900)
        self.mock_screenshot_taker.take_full_screenshot.assert_not_called()
        self.mock_screenshot_taker.take_fixed_size_screen_shot.assert_called_with(bbox=(0.0, 675.0, 300.0, 975.0))
        self.assertEqual(event.click_x, 50.0)
        self.assertEqual(event.click_y, 225.0)

    def test_get_mouse_event_click_right_lower_limit(self):
        event = self.mouse_event_creator.get_mouse_event(1800, 900)
        self.mock_screenshot_taker.take_full_screenshot.assert_not_called()
        self.mock_screenshot_taker.take_fixed_size_screen_shot.assert_called_with(bbox=(1600.0, 675.0, 1900, 975.0))
        self.assertEqual(event.click_x, 200.0)
        self.assertEqual(event.click_y, 225.0)

    def test_get_mouse_event_fixed_size_too_big(self):
        self.mock_screen_manager.get_screen_size = MagicMock(return_value=(400, 400))
        self.mouse_event_creator = FixedSizeScreenshotEventCreator(self.mock_screenshot_taker, self.mock_screen_manager,
                                                                   500, 500)
        self.assertRaises(FixedSizeScreenshotSizeError, self.mouse_event_creator.get_mouse_event, 200, 200)


class MouseEventListenerTest(unittest.TestCase):
    def setUp(self):
        self.mock_mouseevent_creator = AbstractMouseEventCreator(None)
        self.mock_mouseevent_creator.get_mouse_event = MagicMock(return_value=MouseEvent(10, 15, None))
        self.mock_event_receiver = EventReceiver(None)
        self.mock_event_receiver.receive_mouse_event = MagicMock()
        self.mouse_event_listener = MouseEventListener(self.mock_mouseevent_creator, self.mock_event_receiver)

    def test_left_click_press(self):
        self.mouse_event_listener.click(10, 15, 1, True)
        self.mock_mouseevent_creator.get_mouse_event.assert_called_with(10, 15)
        self.mock_event_receiver.receive_mouse_event.assert_called_with(MouseEvent(10, 15, None))

    def test_left_click_NotPressed(self):
        self.mouse_event_listener.click(10, 15, 1, False)
        self.mock_mouseevent_creator.get_mouse_event.assert_not_called()
        self.mock_event_receiver.receive_mouse_event.assert_not_called()

    def test_right_click_press(self):
        self.mouse_event_listener.click(10, 15, 2, True)
        self.mock_mouseevent_creator.get_mouse_event.assert_not_called()
        self.mock_event_receiver.receive_mouse_event.assert_not_called()

    def test_right_click_NotPressed(self):
        self.mouse_event_listener.click(10, 15, 2, False)
        self.mock_mouseevent_creator.get_mouse_event.assert_not_called()
        self.mock_event_receiver.receive_mouse_event.assert_not_called()


class KeyboardListenerTest(unittest.TestCase):
    def setUp(self):
        self.mock_keyboard_state_manager = KeyboardStateManager(None)
        self.mock_keyboard_state_manager.key_pressed = MagicMock()
        self.mock_keyboard_state_manager.key_released = MagicMock()
        self.keyboard_listener = KeyboardListener(self.mock_keyboard_state_manager)

    def test_key_pressed(self):
        self.keyboard_listener.tap(37, "Control_L", True)
        self.mock_keyboard_state_manager.key_pressed.assert_called_with(37)
        self.mock_keyboard_state_manager.key_released.assert_not_called()

    def test_key_released(self):
        self.keyboard_listener.tap(37, "Control_L", False)
        self.mock_keyboard_state_manager.key_released.assert_called_with(37)
        self.mock_keyboard_state_manager.key_pressed.assert_not_called()


class KeyboardStateManagerTest(unittest.TestCase):
    def setUp(self):
        self.mock_event_receiver = EventReceiver(None)
        self.mock_event_receiver.receive_keyboard_state_change_event = MagicMock()
        self.keyboard_state_manager = KeyboardStateManager(self.mock_event_receiver)

    def test_single_key_pressed(self):
        self.keyboard_state_manager.key_pressed(37)
        self.assertEqual(self.keyboard_state_manager.get_pressed_keys(), [37])
        self.mock_event_receiver.receive_keyboard_state_change_event.assert_called_with(KeyboardStateChangedEvent([37]))

    def test_single_key_pressed_and_released(self):
        self.keyboard_state_manager.key_pressed(37)
        self.keyboard_state_manager.key_released(37)
        self.assertEqual(self.keyboard_state_manager.get_pressed_keys(), [])
        self.mock_event_receiver.receive_keyboard_state_change_event.assert_called_with(KeyboardStateChangedEvent([]))

    def test_multiple_keys_pressed(self):
        self.keyboard_state_manager.key_pressed(37)
        self.keyboard_state_manager.key_pressed(30)
        self.keyboard_state_manager.key_pressed(40)
        self.assertEqual(self.keyboard_state_manager.get_pressed_keys(), [37, 30, 40])
        self.mock_event_receiver.receive_keyboard_state_change_event.assert_called_with(
            KeyboardStateChangedEvent([37, 30, 40]))

    def test_multiple_keys_pressed_and_released(self):
        self.keyboard_state_manager.key_pressed(37)
        self.keyboard_state_manager.key_pressed(30)
        self.keyboard_state_manager.key_pressed(40)
        self.keyboard_state_manager.key_released(37)
        self.keyboard_state_manager.key_released(40)
        self.assertEqual(self.keyboard_state_manager.get_pressed_keys(), [30])
        self.mock_event_receiver.receive_keyboard_state_change_event.assert_called_with(KeyboardStateChangedEvent([30]))

    def test_same_key_pressed(self):
        self.keyboard_state_manager.key_pressed(37)
        self.keyboard_state_manager.key_pressed(37)
        self.assertEqual(self.keyboard_state_manager.get_pressed_keys(), [37])
        self.mock_event_receiver.receive_keyboard_state_change_event.assert_called_once_with(
            KeyboardStateChangedEvent([37]))

    def test_key_released_but_not_pressed(self):
        self.keyboard_state_manager.key_released(37)
        self.assertEqual(self.keyboard_state_manager.get_pressed_keys(), [])
        self.mock_event_receiver.receive_keyboard_state_change_event.assert_not_called()

    def test_keys_pressed_and_released(self):
        self.keyboard_state_manager.key_pressed(37)
        self.keyboard_state_manager.key_pressed(30)
        self.keyboard_state_manager.key_pressed(40)
        self.keyboard_state_manager.key_released(30)
        self.keyboard_state_manager.key_pressed(36)
        self.keyboard_state_manager.key_pressed(35)
        self.keyboard_state_manager.key_released(36)
        self.assertEqual(self.keyboard_state_manager.get_pressed_keys(), [37, 40, 35])
        self.mock_event_receiver.receive_keyboard_state_change_event.assert_called_with(
            KeyboardStateChangedEvent([37, 40, 35]))
