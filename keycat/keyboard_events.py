from pykeyboard import PyKeyboardEvent
from program_identifier import *


class KeyboardEventListener(PyKeyboardEvent):
    def __init__(self, keyboard_listener):
        self.keyboard_listener = keyboard_listener
        PyKeyboardEvent.__init__(self)

    def tap(self, keycode, character, press):
        self.keyboard_listener.tap(keycode, character, press)


class KeyboardListener(object):
    def __init__(self, keyboard_state_manager):
        self.keyboard_state_manager = keyboard_state_manager

    def tap(self, keycode, character, press):
        if press:
            self.keyboard_state_manager.key_pressed(keycode)
        else:
            self.keyboard_state_manager.key_released(keycode)


class KeyboardStateChangedEvent(object):
    def __init__(self, pressed_keys, program):
        self.pressed_keys = pressed_keys
        self.program = program

    def __eq__(self, other):
        return self.pressed_keys == other.pressed_keys and self.program == other.program


class KeyboardStateManager(object):
    def __init__(self, event_receiver, program_identifier):
        self.event_receiver = event_receiver
        self.program_identifier = program_identifier
        self.pressed_keys = []

    def key_pressed(self, keycode):
        if keycode not in self.pressed_keys:
            self.pressed_keys.append(keycode)
            try:
                self.event_receiver.receive_keyboard_state_change_event(
                    KeyboardStateChangedEvent(self.get_pressed_keys(), self.program_identifier.get_active_program()))
            except(NoTopWindowFoundError, CantGetPIDOfWindowError) as e:
                # TODO logging
                pass

    def key_released(self, keycode):
        if keycode in self.pressed_keys:
            self.pressed_keys.remove(keycode)
            try:
                self.event_receiver.receive_keyboard_state_change_event(
                    KeyboardStateChangedEvent(self.get_pressed_keys(), self.program_identifier.get_active_program()))
            except(NoTopWindowFoundError, CantGetPIDOfWindowError) as e:
                # TODO logging
                pass

    def get_pressed_keys(self):
        return self.pressed_keys
