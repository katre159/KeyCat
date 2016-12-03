import sys
import gi

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk as gtk

gi.require_version('AppIndicator3', '0.1')
from gi.repository import AppIndicator3 as appindicator
from dependencies import button_repository, event_receiver, mouse_event_creator, program_identifier\
    ,shortcut_stat_repository, button_stat_repository
from database import *
from keyboard_events import KeyboardEventListener, KeyboardListener, KeyboardStateManager
from mouse_events import MouseEventListener, MouseClickEventListener
import signal

APPINDICATOR_ID = 'keycatindicator'


def main():
    load_data_to_database(button_repository, shortcut_stat_repository, button_stat_repository)

    keyboard_event_listener = KeyboardEventListener(KeyboardListener(
        KeyboardStateManager(event_receiver, program_identifier)))
    keyboard_event_listener.daemon = True
    keyboard_event_listener.start()

    mouse_click_listener = MouseClickEventListener(
        MouseEventListener(mouse_event_creator, event_receiver))

    mouse_click_listener.daemon = True
    mouse_click_listener.start()

    indicator = appindicator.Indicator.new(APPINDICATOR_ID, gtk.STOCK_INFO,
                                           appindicator.IndicatorCategory.SYSTEM_SERVICES)
    indicator.set_status(appindicator.IndicatorStatus.ACTIVE)
    indicator.set_menu(build_menu())
    signal.signal(signal.SIGINT, signal.SIG_DFL)
    gtk.main()


def build_menu():
    menu = gtk.Menu()
    item_quit = gtk.MenuItem('Quit')
    item_quit.connect('activate', quit)
    menu.append(item_quit)
    menu.show_all()
    return menu


def quit(source):
    gtk.main_quit()


if __name__ == '__main__':
    sys.exit(main())
