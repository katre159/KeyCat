import sys
from mouse_events import FullscreenMouseEventCreator, MouseEventListener, MouseClickEventListener, \
    FixedSizeScreenshotEventCreator
from events import EventReceiver
from screen import ScreenshotTaker, ScreenManager
from keyboard_events import KeyboardEventListener, KeyboardListener, KeyboardStateManager
from repository import ButtonRepository
from button_matcher import ButtonMatcher
from template_matcher import CCOEFFNORMEDTemplateMatcher
from database import *
from program_identifier import *

import gi
gi.require_version("Gtk", "3.0")
gi.require_version("AppIndicator3", "0.1")
from gi.repository import Gtk
from gi.repository import AppIndicator3 as appindicator


def main():
    session = get_database_scoped_session()
    button_repository = ButtonRepository(session)
    load_data_to_database(button_repository)

    program_identifier = ProgramIdentifier()
    button_matcher = ButtonMatcher(CCOEFFNORMEDTemplateMatcher(), button_repository)

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


def menuitem_response(w, buf):
    print buf


if __name__ == "__main__":
    ind = appindicator.Indicator.new(
        "example-simple-client",
        "indicator-messages",
        appindicator.IndicatorCategory.APPLICATION_STATUS)
    ind.set_status(appindicator.IndicatorStatus.ACTIVE)
    ind.set_attention_icon("indicator-messages-new")

    menu = Gtk.Menu()

    for i in range(3):
        buf = "Test-undermenu - %d" % i

        menu_items = Gtk.MenuItem(buf)

        menu.append(menu_items)

        menu_items.show()

    ind.set_menu(menu)

    Gtk.main()
    sys.exit(main())
