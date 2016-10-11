import pyscreenshot as ImageGrab


class ScreenshotTaker(object):

    def takeFullScreenshot(self):
        return ImageGrab.grab()

    def takeFixedSizeScreenShot(self, bbox):
        return ImageGrab.grab(bbox=bbox)
