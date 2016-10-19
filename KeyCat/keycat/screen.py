from pyscreenshot import grab
from screeninfo import get_monitors


class Error(Exception):
    """Base class for exceptions in this module."""
    pass


class NoMonitorsFoundError(Error):
    def __init__(self, message):
        self.message = message


class ScreenshotTaker(object):
    @staticmethod
    def take_full_screenshot():
        return grab()

    @staticmethod
    def take_fixed_size_screen_shot(bbox):
        return grab(bbox=bbox)


class ScreenManager(object):
    @staticmethod
    def get_screen_size():
        monitors = get_monitors()
        if len(monitors) == 0:
            raise NoMonitorsFoundError("No monitors found")
        else:
            monitor = monitors[0]
            return (monitor.width, monitor.height)
