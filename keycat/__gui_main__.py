import sys
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk as gtk
gi.require_version('AppIndicator3', '0.1')
from gi.repository import AppIndicator3 as appindicator
from dependencies import button_repository, keyboard_event_listener, mouse_click_listener
from database import *

APPINDICATOR_ID = 'keycatindicator'

def main():

    if len(button_repository.find_all_buttons()) == 0:
        load_data_to_database(button_repository)

    keyboard_event_listener.daemon = True
    keyboard_event_listener.start()

    mouse_click_listener.daemon = True
    mouse_click_listener.start()

    indicator = appindicator.Indicator.new(APPINDICATOR_ID, gtk.STOCK_INFO,
                                           appindicator.IndicatorCategory.SYSTEM_SERVICES)
    indicator.set_status(appindicator.IndicatorStatus.ACTIVE)
    indicator.set_menu(build_menu())
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