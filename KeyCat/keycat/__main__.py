import sys
from mouse_events import FullscreenMouseEventCreator, MouseEventListener, MouseClickEventListener
from events import EventReceiver
from screenshot_taker import ScreenshotTaker
from keyboard_events import KeyboardEventListener, KeyboardListener, KeyboardStateManager


def main(argv):

    event_receiver = EventReceiver()

    keyboard_event_listener = KeyboardEventListener(KeyboardListener(KeyboardStateManager(event_receiver)))
    keyboard_event_listener.daemon = False
    keyboard_event_listener.start()

    mouse_click_listener = MouseClickEventListener(
        MouseEventListener(FullscreenMouseEventCreator(ScreenshotTaker()), event_receiver))
    mouse_click_listener.daemon = False
    mouse_click_listener.start()


if __name__ == '__main__':
    sys.exit(main(sys.argv))
