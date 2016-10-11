from pyscreenshot import grab


class ScreenshotTaker(object):

    @staticmethod
    def take_full_screenshot():
        return grab()

    @staticmethod
    def take_fixed_size_screen_shot(bbox):
        return grab(bbox=bbox)
