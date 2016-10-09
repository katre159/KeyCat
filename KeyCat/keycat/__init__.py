

import sys
from keycat.mouse_events import FullscreenMouseEventCreator, MouseEventListener, MouseClickEventListener, EventReceiver
from keycat.screenshot_taker import ScreenshotTaker

def main(argv):

    mouseClickListener = MouseClickEventListener(MouseEventListener(FullscreenMouseEventCreator(ScreenshotTaker()),EventReceiver()))
    mouseClickListener.run()


if __name__ == '__main__':
    sys.exit(main(sys.argv))
