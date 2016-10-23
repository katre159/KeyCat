from pykeyboard import PyKeyboardEvent


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
    def __init__(self, pressed_keys):
        self.pressed_keys = pressed_keys

    def __eq__(self, other):
        return self.pressed_keys == other.pressed_keys


class KeyboardStateManager(object):
    def __init__(self, event_receiver):
        self.event_receiver = event_receiver
        self.pressed_keys = []

    def key_pressed(self, keycode):
        if keycode not in self.pressed_keys:
            self.pressed_keys.append(keycode)
            self.event_receiver.receive_keyboard_state_change_event(KeyboardStateChangedEvent(self.get_pressed_keys()))

    def key_released(self, keycode):
        if keycode in self.pressed_keys:
            self.pressed_keys.remove(keycode)
            self.event_receiver.receive_keyboard_state_change_event(KeyboardStateChangedEvent(self.get_pressed_keys()))

    def get_pressed_keys(self):
        return self.pressed_keys
