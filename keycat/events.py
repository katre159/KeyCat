from notify import *
from button_matcher import Click


class EventReceiver(object):
    def __init__(self, button_matcher, shortcut_repository, statistic_collector):
        self.button_matcher = button_matcher
        self.shortcut_repository = shortcut_repository
        self.statistic_collector = statistic_collector

    def receive_mouse_event(self, event):

        button = self.button_matcher.find_button_on_clicked_position(Click(event.click_x, event.click_y),
                                                                     event.screenshot, event.program)
        if button is not None:
            button_stat = self.statistic_collector.button_pressed(button)
            message = "You can use these shortcuts for this action : " \
                      + " or ".join(map(lambda x: x.get_keycodes_in_readable_format(), button.shortcuts))
            message += " button pressed count " + str(button_stat.hit_count)
            Notify.show_notification(message)

    def receive_keyboard_state_change_event(self, event):

        shortcut = self.shortcut_repository.find_shortcut_by_keycode_and_program(",".join(map(str, event.pressed_keys))
                                                                                 , event.program)
        if shortcut is not None:
            shortcut_stat = self.statistic_collector.shortcut_pressed(shortcut)
            Notify.show_notification("You have used this shortcut %d times" % (shortcut_stat.hit_count))

    def _save_event_screenshot(self, event):
        event.screenshot.save("screenshot_x_" + str(event.click_x) + "_y_" + str(event.click_y) + ".png", "PNG")
