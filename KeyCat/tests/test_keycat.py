import unittest
from unittest.mock import MagicMock
from keycat.mouse_events import FullscreenMouseEventCreator, MouseEventListener, AbstractMouseEventCreator, MouseEvent, EventReceiver
from keycat.screenshot_taker import ScreenshotTaker

class FullscreenMouseEventCreatorTest(unittest.TestCase):

    def setUp(self):
        self.mockScreenShotTaker = ScreenshotTaker
        self.mockScreenShotTaker.takeFullScreenshot = MagicMock(return_value=None)
        self.mouseEventCreator = FullscreenMouseEventCreator(self.mockScreenShotTaker)

    def test_getMouseEvent(self):
        event = self.mouseEventCreator.getMouseEvent(10,15)
        self.mockScreenShotTaker.takeFullScreenshot.assert_called_with()
        self.assertEqual(event.clickX, 10)
        self.assertEqual(event.clickY, 15)


class MouseEventListenerTest(unittest.TestCase):

    def setUp(self):
        self.mockMouseEventCreator = AbstractMouseEventCreator(None)
        self.mockMouseEventCreator.getMouseEvent = MagicMock(return_value=MouseEvent(10,15,None))
        self.mockEventReceiver = EventReceiver()
        self.mockEventReceiver.receiveEvent = MagicMock()
        self.mouseEventListener = MouseEventListener(self.mockMouseEventCreator, self.mockEventReceiver)

    def test_left_click_press(self):
        self.mouseEventListener.click(10,15,1,True)
        self.mockMouseEventCreator.getMouseEvent.assert_called_with(10,15)
        self.mockEventReceiver.receiveEvent.assert_called_with(MouseEvent(10,15,None))

    def test_left_click_NotPressed(self):
        self.mouseEventListener.click(10,15,1,False)
        self.mockMouseEventCreator.getMouseEvent.assert_not_called()
        self.mockEventReceiver.receiveEvent.assert_not_called()

    def test_right_click_press(self):
        self.mouseEventListener.click(10,15,2,True)
        self.mockMouseEventCreator.getMouseEvent.assert_not_called()
        self.mockEventReceiver.receiveEvent.assert_not_called()

    def test_right_click_NotPressed(self):
        self.mouseEventListener.click(10,15,2,False)
        self.mockMouseEventCreator.getMouseEvent.assert_not_called()
        self.mockEventReceiver.receiveEvent.assert_not_called()


