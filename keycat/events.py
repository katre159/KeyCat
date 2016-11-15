from notify import *
from button_matcher import Click


class EventReceiver(object):
    def __init__(self, button_matcher):
        self.button_matcher = button_matcher

    def receive_mouse_event(self, event):
        print(
            "MouseEvent: x = %s, y = %s, program = %s  screenshot = %s" % (event.click_x, event.click_y,
                                                                           event.program, event.screenshot))

        button = self.button_matcher.find_button_on_clicked_position(Click(event.click_x, event.click_y),
                                                                     event.screenshot, event.program)

        if button is not None:
            Notify.show_notification("You clicked on button,"
                                     " shortcuts = " + " or ".join(map(lambda x: x.keycodes, button.shortcuts)))

    def receive_keyboard_state_change_event(self, event):
        print("Keys pressed = %s, program = %s" % (event.pressed_keys, event.program))

    def _save_event_screenshot(self, event):
        event.screenshot.save("screenshot_x_" + str(event.click_x) + "_y_" + str(event.click_y) + ".png", "PNG")
