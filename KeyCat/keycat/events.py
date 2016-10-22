from notify import *


class EventReceiver(object):

    @staticmethod
    def receive_mouse_event(event):
        Notify.show_notification("MouseEvent: x = %s, y = %s, screenshot = %s" % (event.click_x, event.click_y, event.screenshot))

    @staticmethod
    def receive_keyboard_state_change_event(event):
        Notify.show_notification("Keys pressed : %s" % event.pressed_keys)
