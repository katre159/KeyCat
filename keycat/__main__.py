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
from os.path import expanduser
import signal
import shutil
import fcntl, os

APPINDICATOR_ID = 'keycatindicator'
lock_file = open(os.path.expanduser('~/.keycat.lock'), 'w')


def lock_program():
    try:
        fcntl.lockf(lock_file, fcntl.LOCK_EX | fcntl.LOCK_NB)
    except IOError:
        print('Another instance of KeyCat is already running.')
        sys.exit(0)


def main():
    lock_program()
    load_data_to_database(button_repository, shortcut_stat_repository, button_stat_repository)

    keyboard_event_listener = KeyboardEventListener(KeyboardListener(
        KeyboardStateManager(event_receiver, program_identifier)))
    keyboard_event_listener.daemon = True
    keyboard_event_listener.start()

    mouse_click_listener = MouseClickEventListener(
        MouseEventListener(mouse_event_creator, event_receiver))

    mouse_click_listener.daemon = True
    mouse_click_listener.start()

    icon_destination = os.path.join(
        expanduser("~"), '.local', 'share', 'icons', 'hicolor', '22x22', 'apps','keycat-small.png')
    if not os.path.isfile(icon_destination):
        os.makedirs(os.path.join(expanduser("~"), '.local', 'share', 'icons', 'hicolor', '22x22', 'apps'))
        shutil.copy('keycat-small.png', icon_destination)
    indicator = appindicator.Indicator.new(APPINDICATOR_ID, icon_destination,
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
