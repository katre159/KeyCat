import unittest
from mock import MagicMock
from keycat.events import EventReceiver
from keycat.mouse_events import FullscreenMouseEventCreator, FixedSizeScreenshotEventCreator, \
    FixedSizeScreenshotSizeError, AbstractMouseEventCreator, MouseEvent, MouseEventListener
from keycat.screen import ScreenshotTaker, ScreenManager
from keycat.program_identifier import ProgramIdentifier


class FullscreenMouseEventCreatorTest(unittest.TestCase):
    def setUp(self):
        self.mock_screenshot_taker = ScreenshotTaker
        self.mock_screenshot_taker.take_full_screenshot = MagicMock(return_value=None)
        self.mock_program_identifier = ProgramIdentifier
        self.expected_program = "MockProgram"
        self.mock_program_identifier.get_active_program = MagicMock(return_value=self.expected_program)
        self.mouse_event_creator = FullscreenMouseEventCreator(self.mock_screenshot_taker, self.mock_program_identifier)

    def test_get_mouse_event(self):
        event = self.mouse_event_creator.get_mouse_event(10, 15)
        self.mock_screenshot_taker.take_full_screenshot.assert_called_with()
        self.mock_program_identifier.get_active_program.assert_called_with()
        self.assertEqual(event.click_x, 10)
        self.assertEqual(event.click_y, 15)
        self.assertEqual(event.program, self.expected_program)


class FixedSizeScreenshotEventCreatorTest(unittest.TestCase):
    def setUp(self):
        self.mock_screenshot_taker = ScreenshotTaker
        self.mock_screenshot_taker.take_full_screenshot = MagicMock(return_value=None)
        self.mock_screenshot_taker.take_fixed_size_screen_shot = MagicMock(return_value=None)
        self.mock_screen_manager = ScreenManager()
        self.mock_screen_manager.get_screen_size = MagicMock(return_value=(1900, 975))
        self.mock_program_identifier = ProgramIdentifier
        self.expected_program = "MockProgram"
        self.mock_program_identifier.get_active_program = MagicMock(return_value=self.expected_program)
        self.mouse_event_creator = FixedSizeScreenshotEventCreator(self.mock_screenshot_taker, self.mock_screen_manager,
                                                                   self.mock_program_identifier,
                                                                   300, 300)

    def test_get_mouse_event_click_middle(self):
        event = self.mouse_event_creator.get_mouse_event(500, 600)
        self.mock_screenshot_taker.take_full_screenshot.assert_not_called()
        self.mock_screenshot_taker.take_fixed_size_screen_shot.assert_called_with(bbox=(350.0, 450.0, 650.0, 750.0))
        self.mock_program_identifier.get_active_program.assert_called_with()
        self.assertEqual(event.program, self.expected_program)
        self.assertEqual(event.click_x, 150.0)
        self.assertEqual(event.click_y, 150.0)

    def test_get_mouse_event_click_lower_limit(self):
        event = self.mouse_event_creator.get_mouse_event(500, 900)
        self.mock_screenshot_taker.take_full_screenshot.assert_not_called()
        self.mock_screenshot_taker.take_fixed_size_screen_shot.assert_called_with(bbox=(350.0, 675.0, 650.0, 975.0))
        self.mock_program_identifier.get_active_program.assert_called_with()
        self.assertEqual(event.program, self.expected_program)
        self.assertEqual(event.click_x, 150.0)
        self.assertEqual(event.click_y, 225.0)

    def test_get_mouse_event_click_upper_limit(self):
        event = self.mouse_event_creator.get_mouse_event(500, 50)
        self.mock_screenshot_taker.take_full_screenshot.assert_not_called()
        self.mock_screenshot_taker.take_fixed_size_screen_shot.assert_called_with(bbox=(350.0, 0, 650.0, 300))
        self.mock_program_identifier.get_active_program.assert_called_with()
        self.assertEqual(event.program, self.expected_program)
        self.assertEqual(event.click_x, 150.0)
        self.assertEqual(event.click_y, 50.0)

    def test_get_mouse_event_click_left_limit(self):
        event = self.mouse_event_creator.get_mouse_event(50, 600)
        self.mock_screenshot_taker.take_full_screenshot.assert_not_called()
        self.mock_screenshot_taker.take_fixed_size_screen_shot.assert_called_with(bbox=(0.0, 450.0, 300.0, 750.0))
        self.mock_program_identifier.get_active_program.assert_called_with()
        self.assertEqual(event.program, self.expected_program)
        self.assertEqual(event.click_x, 50.0)
        self.assertEqual(event.click_y, 150.0)

    def test_get_mouse_event_click_right_limit(self):
        event = self.mouse_event_creator.get_mouse_event(1800, 600)
        self.mock_screenshot_taker.take_full_screenshot.assert_not_called()
        self.mock_screenshot_taker.take_fixed_size_screen_shot.assert_called_with(bbox=(1600, 450.0, 1900, 750.0))
        self.mock_program_identifier.get_active_program.assert_called_with()
        self.assertEqual(event.program, self.expected_program)
        self.assertEqual(event.click_x, 200.0)
        self.assertEqual(event.click_y, 150.0)

    def test_get_mouse_event_click_left_upper_limit(self):
        event = self.mouse_event_creator.get_mouse_event(50, 50)
        self.mock_screenshot_taker.take_full_screenshot.assert_not_called()
        self.mock_screenshot_taker.take_fixed_size_screen_shot.assert_called_with(bbox=(0.0, 0.0, 300.0, 300.0))
        self.mock_program_identifier.get_active_program.assert_called_with()
        self.assertEqual(event.program, self.expected_program)
        self.assertEqual(event.click_x, 50.0)
        self.assertEqual(event.click_y, 50.0)

    def test_get_mouse_event_click_right_upper_limit(self):
        event = self.mouse_event_creator.get_mouse_event(1800, 50)
        self.mock_screenshot_taker.take_full_screenshot.assert_not_called()
        self.mock_screenshot_taker.take_fixed_size_screen_shot.assert_called_with(bbox=(1600.0, 0.0, 1900.0, 300.0))
        self.mock_program_identifier.get_active_program.assert_called_with()
        self.assertEqual(event.program, self.expected_program)
        self.assertEqual(event.click_x, 200.0)
        self.assertEqual(event.click_y, 50.0)

    def test_get_mouse_event_click_left_lower_limit(self):
        event = self.mouse_event_creator.get_mouse_event(50, 900)
        self.mock_screenshot_taker.take_full_screenshot.assert_not_called()
        self.mock_screenshot_taker.take_fixed_size_screen_shot.assert_called_with(bbox=(0.0, 675.0, 300.0, 975.0))
        self.mock_program_identifier.get_active_program.assert_called_with()
        self.assertEqual(event.program, self.expected_program)
        self.assertEqual(event.click_x, 50.0)
        self.assertEqual(event.click_y, 225.0)

    def test_get_mouse_event_click_right_lower_limit(self):
        event = self.mouse_event_creator.get_mouse_event(1800, 900)
        self.mock_screenshot_taker.take_full_screenshot.assert_not_called()
        self.mock_screenshot_taker.take_fixed_size_screen_shot.assert_called_with(bbox=(1600.0, 675.0, 1900, 975.0))
        self.mock_program_identifier.get_active_program.assert_called_with()
        self.assertEqual(event.program, self.expected_program)
        self.assertEqual(event.click_x, 200.0)
        self.assertEqual(event.click_y, 225.0)

    def test_get_mouse_event_fixed_size_too_big(self):
        self.mock_screen_manager.get_screen_size = MagicMock(return_value=(400, 400))
        self.mouse_event_creator = FixedSizeScreenshotEventCreator(self.mock_screenshot_taker, self.mock_screen_manager,
                                                                   self.mock_program_identifier,
                                                                   500, 500)
        self.assertRaises(FixedSizeScreenshotSizeError, self.mouse_event_creator.get_mouse_event, 200, 200)


class MouseEventListenerTest(unittest.TestCase):
    def setUp(self):
        self.mock_mouseevent_creator = AbstractMouseEventCreator(None, None)
        self.expected_program = "MockProgram"
        self.mock_mouseevent_creator.get_mouse_event = MagicMock(
            return_value=MouseEvent(10, 15, None, self.expected_program))
        self.mock_event_receiver = EventReceiver(None, None, None)
        self.mock_event_receiver.receive_mouse_event = MagicMock()
        self.mouse_event_listener = MouseEventListener(self.mock_mouseevent_creator, self.mock_event_receiver)

    def test_left_click_press(self):
        self.mouse_event_listener.click(10, 15, 1, True)
        self.mock_mouseevent_creator.get_mouse_event.assert_called_with(10, 15)
        self.mock_event_receiver.receive_mouse_event.assert_called_with(MouseEvent(10, 15, None, self.expected_program))

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
