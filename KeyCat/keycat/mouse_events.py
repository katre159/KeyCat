import abc

from pymouse import PyMouseEvent


class MouseEvent(object):

    def __init__(self, click_x, click_y, screenshot):
        self.click_x = click_x
        self.click_y = click_y
        self.screenshot = screenshot

    def __eq__(self, other):
        return self.click_x == other.click_x and self.click_y == other.click_y and self.screenshot == other.screenshot


class AbstractMouseEventCreator(object):

    def __init__(self, screenshot_taker):
        self.screenshot_taker = screenshot_taker

    @abc.abstractmethod
    def get_mouse_event(self, x, y):
        return


class FullscreenMouseEventCreator(AbstractMouseEventCreator):

    def get_mouse_event(self, x, y):
        screenshot = self.screenshot_taker.take_full_screenshot()
        return MouseEvent(x, y, screenshot)


class MouseClickEventListener(PyMouseEvent):

    def __init__(self, mouse_event_listener):
        PyMouseEvent.__init__(self)
        self.mouse_event_listener = mouse_event_listener

    def click(self, x, y, button, press):
        self.mouse_event_listener.click(x, y, button, press)


class MouseEventListener(object):

    def __init__(self, mouse_event_creator, event_receiver):
        self.mouse_event_creator = mouse_event_creator
        self.event_receiver = event_receiver

    def click(self, x, y, button, press):
        if button == 1:
            if press:
                event = self.mouse_event_creator.get_mouse_event(x, y)
                self.event_receiver.receive_event(event)


class EventReceiver(object):

    @staticmethod
    def receive_event(event):
        print("MouseEvent: x = %s, y = %s, screenshot = %s" % (event.click_x, event.click_y, event.screenshot))

