import unittest
from unittest.mock import MagicMock
from keycat.mouse_events import FullscreenMouseEventCreator, MouseEventListener, AbstractMouseEventCreator, MouseEvent, EventReceiver
from keycat.screenshot_taker import ScreenshotTaker

class FullscreenMouseEventCreatorTest(unittest.TestCase):

    def setUp(self):
        self.mockScreenShotTaker = ScreenshotTaker
        self.mockScreenShotTaker.take_full_screenshot = MagicMock(return_value=None)
        self.mouseEventCreator = FullscreenMouseEventCreator(self.mockScreenShotTaker)

    def test_getMouseEvent(self):
        event = self.mouseEventCreator.get_mouse_event(10, 15)
        self.mockScreenShotTaker.takeFullScreenshot.assert_called_with()
        self.assertEqual(event.clickX, 10)
        self.assertEqual(event.clickY, 15)


class MouseEventListenerTest(unittest.TestCase):

    def setUp(self):
        self.mockMouseEventCreator = AbstractMouseEventCreator(None)
        self.mockMouseEventCreator.get_mouse_event = MagicMock(return_value=MouseEvent(10, 15, None))
        self.mockEventReceiver = EventReceiver()
        self.mockEventReceiver.receive_event = MagicMock()
        self.mouseEventListener = MouseEventListener(self.mockMouseEventCreator, self.mockEventReceiver)

    def test_left_click_press(self):
        self.mouseEventListener.click(10,15,1,True)
        self.mockMouseEventCreator.get_mouse_event.assert_called_with(10, 15)
        self.mockEventReceiver.receiveEvent.assert_called_with(MouseEvent(10,15,None))

    def test_left_click_NotPressed(self):
        self.mouseEventListener.click(10,15,1,False)
        self.mockMouseEventCreator.get_mouse_event.assert_not_called()
        self.mockEventReceiver.receiveEvent.assert_not_called()

    def test_right_click_press(self):
        self.mouseEventListener.click(10,15,2,True)
        self.mockMouseEventCreator.get_mouse_event.assert_not_called()
        self.mockEventReceiver.receiveEvent.assert_not_called()

    def test_right_click_NotPressed(self):
        self.mouseEventListener.click(10,15,2,False)
        self.mockMouseEventCreator.get_mouse_event.assert_not_called()
        self.mockEventReceiver.receiveEvent.assert_not_called()


