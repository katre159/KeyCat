from pyscreenshot import grab
from screeninfo import get_monitors
from pyscreenshot.plugins import wxscreen, gtkpixbuf, qtgrabwindow, scrot, \
    imagemagick, mac_quartz, mac_screencapture, pil
import pyscreenshot

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
        return grab(bbox=bbox, backend="imagemagick")


class ScreenManager(object):
    @staticmethod
    def get_screen_size():
        monitors = get_monitors()
        if len(monitors) == 0:
            raise NoMonitorsFoundError("No monitors found")
        else:
            monitors_combined_width = 0
            highest_monitor_height = 0
            for monitor in monitors:
                monitors_combined_width += monitor.width
                if monitor.height > highest_monitor_height:
                    highest_monitor_height = monitor.height

            return (monitors_combined_width, highest_monitor_height)
