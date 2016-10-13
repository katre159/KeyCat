import sys
from mouse_events import FullscreenMouseEventCreator, MouseEventListener, MouseClickEventListener, EventReceiver
from screenshot_taker import ScreenshotTaker


def main(argv):
    mouse_click_listener = MouseClickEventListener(
        MouseEventListener(FullscreenMouseEventCreator(ScreenshotTaker()), EventReceiver()))

    mouse_click_listener.run()


if __name__ == '__main__':
    sys.exit(main(sys.argv))
