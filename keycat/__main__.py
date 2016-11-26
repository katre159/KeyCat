import sys
from dependencies import button_repository, keyboard_event_listener, mouse_click_listener
from database import *
from time import sleep
import signal


def exit_program(signal, frame):
    print('Keycat terminated!')
    sys.exit(0)


def main():
    if len(button_repository.find_all_buttons()) == 0:
        load_data_to_database(button_repository)

    keyboard_event_listener.daemon = True
    keyboard_event_listener.start()

    mouse_click_listener.daemon = True
    mouse_click_listener.start()

    while 1:
        signal.signal(signal.SIGINT, exit_program)
        sleep(1)


if __name__ == '__main__':
    sys.exit(main())
