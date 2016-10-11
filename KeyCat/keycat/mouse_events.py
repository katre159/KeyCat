import abc
from pymouse import PyMouseEvent


class MouseEvent(object):
    def __init__(self, clickX, clickY, screenShot):
        self.clickX = clickX
        self.clickY = clickY
        self.screenShot = screenShot

    def __eq__(self, other):
        return self.clickX == other.clickX and self.clickY == other.clickY and self.screenShot == other.screenShot



class AbstractMouseEventCreator(object):

    def __init__(self, screenShotTaker):
        self.screenShotTaker = screenShotTaker


    @abc.abstractmethod
    def getMouseEvent(self, x, y):
        return

class FullscreenMouseEventCreator(AbstractMouseEventCreator):

    def getMouseEvent(self, x, y):
        screenShot = self.screenShotTaker.takeFullScreenshot()
        return MouseEvent(x, y, screenShot)


class MouseClickEventListener(PyMouseEvent):


    def __init__(self, mouseEventListener):
        PyMouseEvent.__init__(self)
        self.mouseEventListener = mouseEventListener

    def click(self, x, y, button, press):
        self.mouseEventListener.click(x, y, button, press)

class MouseEventListener(object):
    def __init__(self, mouseEventCreator, eventReceiver):
        self.mouseEventCreator = mouseEventCreator
        self.eventReceiver = eventReceiver

    def click(self, x, y, button, press):
        if button == 1:
            if press:
                event = self.mouseEventCreator.getMouseEvent(x ,y)
                self.eventReceiver.receiveEvent(event);



class EventReceiver(object):

    def receiveEvent(self, event):
        print("MouseEvent x=" + str(event.clickX) + " y=" + str(event.clickY))

