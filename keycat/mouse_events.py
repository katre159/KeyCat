import abc

from pymouse import PyMouseEvent
from collections import namedtuple
from program_identifier import *


class Error(Exception):
    """Base class for exceptions in this module."""
    pass


class FixedSizeScreenshotSizeError(Error):
    def __init__(self, message):
        self.message = message


class MouseEvent(object):
    def __init__(self, click_x, click_y, screenshot, program):
        self.click_x = click_x
        self.click_y = click_y
        self.screenshot = screenshot
        self.program = program

    def __eq__(self, other):
        return self.click_x == other.click_x and self.click_y == other.click_y and self.screenshot == other.screenshot \
               and self.program == other.program


class AbstractMouseEventCreator(object):
    def __init__(self, screenshot_taker, program_identifier):
        self.screenshot_taker = screenshot_taker
        self.program_identifier = program_identifier

    @abc.abstractmethod
    def get_mouse_event(self, x, y):
        return


class FullscreenMouseEventCreator(AbstractMouseEventCreator):
    def get_mouse_event(self, x, y):
        screenshot = self.screenshot_taker.take_full_screenshot()
        program = self.program_identifier.get_active_program()
        return MouseEvent(x, y, screenshot, program)


class FixedSizeScreenshotEventCreator(AbstractMouseEventCreator):
    def __init__(self, screenshot_taker, screen_manager, program_identifier, width, height):
        AbstractMouseEventCreator.__init__(self, screenshot_taker, program_identifier)
        self.screen_manager = screen_manager
        self.width = width
        self.height = height

    def get_mouse_event(self, x, y):

        transformed_coordinates = self._get_transformed_coordinates(x, y)

        screenshot = self.screenshot_taker.take_fixed_size_screen_shot(
            bbox=(transformed_coordinates.screenshot_x, transformed_coordinates.screenshot_y,
                  transformed_coordinates.screenshot_x + self.width,
                  transformed_coordinates.screenshot_y + self.height))  # X1,Y1,X2,Y2

        program = self.program_identifier.get_active_program()

        return MouseEvent(transformed_coordinates.x, transformed_coordinates.y, screenshot, program)

    def _get_transformed_coordinates(self, x, y):
        ScreenSize = namedtuple('ScreenSize', 'width height')
        TransformedCoords = namedtuple('TransformedCoords', 'x y screenshot_x screenshot_y')
        screen_size = ScreenSize(*self.screen_manager.get_screen_size())

        def is_x_coord_in_middle():
            return x - self.width / 2 >= 0 and x + self.width / 2 <= screen_size.width

        def is_y_coord_in_middle():
            return y - self.height / 2 >= 0 and y + self.height / 2 <= screen_size.height

        def is_y_coord_in_lower_limit():
            return y - self.height / 2 >= 0 and y + self.height / 2 > screen_size.height

        def is_y_coord_in_upper_limit():
            return y - self.height / 2 < 0 and y + self.height / 2 <= screen_size.height

        def is_x_in_left_limit():
            return x - self.width / 2 < 0 and x + self.width / 2 <= screen_size.width

        def is_x_in_right_limit():
            return x - self.width / 2 >= 0 and x + self.width / 2 > screen_size.width

        transformed_x = 0
        transformed_y = 0
        screenshot_x = 0
        screenshot_y = 0
        x_coord_transformed = False
        y_coord_transformed = False

        if is_x_coord_in_middle():
            transformed_x = self.width / 2
            screenshot_x = x - self.width / 2
            x_coord_transformed = True

        if is_y_coord_in_middle():
            transformed_y = self.height / 2
            screenshot_y = y - self.height / 2
            y_coord_transformed = True

        if is_y_coord_in_lower_limit():
            height_diff = (y + self.height / 2) - screen_size.height
            transformed_y = self.height / 2 + height_diff
            screenshot_y = screen_size.height - self.height
            y_coord_transformed = True

        if is_y_coord_in_upper_limit():
            transformed_y = y
            screenshot_y = 0
            y_coord_transformed = True

        if is_x_in_left_limit():
            transformed_x = x
            screenshot_x = 0
            x_coord_transformed = True

        if is_x_in_right_limit():
            width_diff = (x + self.width / 2) - screen_size.width
            transformed_x = self.width / 2 + width_diff
            screenshot_x = screen_size.width - self.width
            x_coord_transformed = True

        if x_coord_transformed and y_coord_transformed:
            return TransformedCoords(transformed_x, transformed_y, screenshot_x, screenshot_y)
        else:
            raise FixedSizeScreenshotSizeError("Fixed size screenshot size is too small for screen")


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
                try:
                    event = self.mouse_event_creator.get_mouse_event(x, y)
                    self.event_receiver.receive_mouse_event(event)
                except(NoTopWindowFoundError, CantGetPIDOfWindowError, FixedSizeScreenshotSizeError) as e:
                    # TODO logging
                    pass
