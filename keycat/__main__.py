import sys
from mouse_events import FullscreenMouseEventCreator, MouseEventListener, MouseClickEventListener, \
    FixedSizeScreenshotEventCreator
from events import EventReceiver
from screen import ScreenshotTaker, ScreenManager
from keyboard_events import KeyboardEventListener, KeyboardListener, KeyboardStateManager
from repository import HardCodedButtonReposotory
from button_matcher import ButtonMatcher
from template_matcher import CCOEFFNORMEDTemplateMatcher
from program_identifier import *
from desktop_entry import create_desktop_entry


def main(argv):
    create_desktop_entry()

    program_identifier = ProgramIdentifier()

    button_matcher = ButtonMatcher(CCOEFFNORMEDTemplateMatcher(), HardCodedButtonReposotory())

    event_receiver = EventReceiver(button_matcher)

    keyboard_event_listener = KeyboardEventListener(KeyboardListener(
        KeyboardStateManager(event_receiver, program_identifier)))
    keyboard_event_listener.daemon = False
    keyboard_event_listener.start()

    mouse_event_creator = FixedSizeScreenshotEventCreator(ScreenshotTaker(), ScreenManager(), program_identifier,
                                                          700, 100)

    mouse_click_listener = MouseClickEventListener(
        MouseEventListener(mouse_event_creator, event_receiver))
    mouse_click_listener.daemon = False
    mouse_click_listener.start()


if __name__ == '__main__':
    sys.exit(main(sys.argv))
