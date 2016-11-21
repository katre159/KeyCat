import unittest
from mock import MagicMock
from keycat.events import EventReceiver
from keycat.keyboard_events import KeyboardListener, KeyboardStateManager, KeyboardStateChangedEvent
from keycat.program_identifier import ProgramIdentifier


class KeyboardListenerTest(unittest.TestCase):
    def setUp(self):
        self.mock_keyboard_state_manager = KeyboardStateManager(None, None)
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
        self.mock_event_receiver = EventReceiver(
            button_matcher=None, shortcut_repository=None, statistic_collector=None)
        self.mock_event_receiver.receive_keyboard_state_change_event = MagicMock()
        self.mock_program_identifier = ProgramIdentifier
        self.expected_program = "MockProgram"
        self.mock_program_identifier.get_active_program = MagicMock(return_value=self.expected_program)
        self.keyboard_state_manager = KeyboardStateManager(self.mock_event_receiver, self.mock_program_identifier)

    def test_single_key_pressed(self):
        self.keyboard_state_manager.key_pressed(37)
        self.assertEqual(self.keyboard_state_manager.get_pressed_keys(), [37])
        self.mock_program_identifier.get_active_program.assert_called_with()
        self.mock_event_receiver.receive_keyboard_state_change_event.assert_called_with(
            KeyboardStateChangedEvent([37], self.expected_program))

    def test_single_key_pressed_and_released(self):
        self.keyboard_state_manager.key_pressed(37)
        self.keyboard_state_manager.key_released(37)
        self.mock_program_identifier.get_active_program.assert_called_with()
        self.assertEqual(self.keyboard_state_manager.get_pressed_keys(), [])
        self.mock_event_receiver.receive_keyboard_state_change_event.assert_called_with(
            KeyboardStateChangedEvent([], self.expected_program))

    def test_multiple_keys_pressed(self):
        self.keyboard_state_manager.key_pressed(37)
        self.keyboard_state_manager.key_pressed(30)
        self.keyboard_state_manager.key_pressed(40)
        self.mock_program_identifier.get_active_program.assert_called_with()
        self.assertEqual(self.keyboard_state_manager.get_pressed_keys(), [37, 30, 40])
        self.mock_event_receiver.receive_keyboard_state_change_event.assert_called_with(
            KeyboardStateChangedEvent([37, 30, 40], self.expected_program))

    def test_multiple_keys_pressed_and_released(self):
        self.keyboard_state_manager.key_pressed(37)
        self.keyboard_state_manager.key_pressed(30)
        self.keyboard_state_manager.key_pressed(40)
        self.keyboard_state_manager.key_released(37)
        self.keyboard_state_manager.key_released(40)
        self.mock_program_identifier.get_active_program.assert_called_with()
        self.assertEqual(self.keyboard_state_manager.get_pressed_keys(), [30])
        self.mock_event_receiver.receive_keyboard_state_change_event.assert_called_with(
            KeyboardStateChangedEvent([30], self.expected_program))

    def test_same_key_pressed(self):
        self.keyboard_state_manager.key_pressed(37)
        self.keyboard_state_manager.key_pressed(37)
        self.mock_program_identifier.get_active_program.assert_called_once_with()
        self.assertEqual(self.keyboard_state_manager.get_pressed_keys(), [37])
        self.mock_event_receiver.receive_keyboard_state_change_event.assert_called_once_with(
            KeyboardStateChangedEvent([37], self.expected_program))

    def test_key_released_but_not_pressed(self):
        self.keyboard_state_manager.key_released(37)
        self.assertEqual(self.keyboard_state_manager.get_pressed_keys(), [])
        self.mock_program_identifier.get_active_program.assert_not_called()
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
        self.mock_program_identifier.get_active_program.assert_called_with()
        self.mock_event_receiver.receive_keyboard_state_change_event.assert_called_with(
            KeyboardStateChangedEvent([37, 40, 35], self.expected_program))
