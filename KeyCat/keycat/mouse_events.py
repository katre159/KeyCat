import abc

from pymouse import PyMouseEvent
from collections import namedtuple


class Error(Exception):
    """Base class for exceptions in this module."""
    pass


class FixedSizeScreenshotSizeError(Error):
    def __init__(self, message):
        self.message = message


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


class FixedSizeScreenshotEventCreator(AbstractMouseEventCreator):
    def __init__(self, screenshot_taker, screen_manager, width, height):
        AbstractMouseEventCreator.__init__(self, screenshot_taker)
        self.screen_manager = screen_manager
        self.width = width
        self.height = height

    def get_mouse_event(self, x, y):
        def get_transformed_coordinates():
            ScreenSize = namedtuple('ScreenSize', 'width height')
            TransformedCoords = namedtuple('TransformedCoords', 'x y screenshot_x screenshot_y')
            screen_size = ScreenSize(*self.screen_manager.get_screen_size())
            if x - self.width / 2 >= 0 and x + self.width / 2 <= screen_size.width \
                    and y - self.height / 2 >= 0 and y + self.height / 2 <= screen_size.height:  # middle
                return TransformedCoords(self.width / 2, self.height / 2, x - self.width / 2, y - self.height / 2)
            elif x - self.width / 2 >= 0 and x + self.width / 2 <= screen_size.width \
                    and y - self.height / 2 >= 0 and y + self.height / 2 > screen_size.height:  # lower limit
                height_diff = (y + self.height / 2) - screen_size.height
                return TransformedCoords(self.width / 2, self.height / 2 + height_diff, x - self.width / 2,
                                         screen_size.height - self.height)
            elif x - self.width / 2 >= 0 and x + self.width / 2 <= screen_size.width \
                    and y - self.height / 2 < 0 and y + self.height / 2 <= screen_size.height:  # upper limit
                return TransformedCoords(self.width / 2, y, x - self.width / 2, 0)
            elif x - self.width / 2 < 0 and x + self.width / 2 <= screen_size.width \
                    and y - self.height / 2 >= 0 and y + self.height / 2 <= screen_size.height:  # left limit
                return TransformedCoords(x, self.height / 2, 0, y - self.height / 2)
            elif x - self.width / 2 >= 0 and x + self.width / 2 > screen_size.width \
                    and y - self.height / 2 >= 0 and y + self.height / 2 <= screen_size.height:  # right limit
                width_diff = (x + self.width / 2) - screen_size.width
                return TransformedCoords(self.width / 2 + width_diff, self.height / 2, screen_size.width - self.width,
                                         y - self.height / 2)
            elif x - self.width / 2 < 0 and x + self.width / 2 <= screen_size.width \
                    and y - self.height / 2 < 0 and y + self.height / 2 <= screen_size.height:  # left upper limit
                return TransformedCoords(x, y, 0, 0)
            elif x - self.width / 2 >= 0 and x + self.width / 2 > screen_size.width \
                    and y - self.height / 2 < 0 and y + self.height / 2 <= screen_size.height:  # right upper limit
                width_diff = (x + self.width / 2) - screen_size.width
                return TransformedCoords(self.width / 2 + width_diff, y, screen_size.width - self.width, 0)
            elif x - self.width / 2 < 0 and x + self.width / 2 <= screen_size.width \
                    and y - self.height / 2 >= 0 and y + self.height / 2 > screen_size.height:  # left lower limit
                height_diff = (y + self.height / 2) - screen_size.height
                return TransformedCoords(x, self.height / 2 + height_diff, 0, screen_size.height - self.height)
            if x - self.width / 2 >= 0 and x + self.width / 2 > screen_size.width \
                    and y - self.height / 2 >= 0 and y + self.height / 2 > screen_size.height:  # right lower
                width_diff = (x + self.width / 2) - screen_size.width
                height_diff = (y + self.height / 2) - screen_size.height
                return TransformedCoords(self.width / 2 + width_diff, self.height / 2 + height_diff,
                                         screen_size.width - self.width, screen_size.height - self.height)
            else:
                raise FixedSizeScreenshotSizeError("Fixed size screenshot size is too small for screen")

        transformed_coordinates = get_transformed_coordinates()

        screenshot = self.screenshot_taker.take_fixed_size_screen_shot(
            bbox=(transformed_coordinates.screenshot_x, transformed_coordinates.screenshot_y,
                  transformed_coordinates.screenshot_x + self.width,
                  transformed_coordinates.screenshot_y + self.height))  # X1,Y1,X2,Y2

        return MouseEvent(transformed_coordinates.x, transformed_coordinates.y, screenshot)


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
                self.event_receiver.receive_mouse_event(event)
