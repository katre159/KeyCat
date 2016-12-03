from notify import *
from button_matcher import Click


class EventReceiver(object):

    def __init__(self, button_matcher, shortcut_repository, statistic_collector):
        self.button_matcher = button_matcher
        self.shortcut_repository = shortcut_repository
        self.statistic_collector = statistic_collector
        self.effectiveness_change_threshold = 5.0

    def receive_mouse_event(self, event):

        button = self.button_matcher.find_button_on_clicked_position(Click(event.click_x, event.click_y),
                                                                     event.screenshot, event.program)
        if button is not None:
            old_effectiveness = self.statistic_collector.calculate_button_effectiveness_statistic(button)
            self.statistic_collector.collect_button_statistics(button)
            new_effectiveness = self.statistic_collector.calculate_button_effectiveness_statistic(button)

            message = "To do this action try pressing : " \
                      + " or ".join(map(lambda x: x.get_keycodes_in_readable_format(), button.shortcuts))
            message += " " + self._get_effectiveness_message(old_effectiveness, new_effectiveness)
            Notify.show_notification(message)

    def receive_keyboard_state_change_event(self, event):

        shortcut = self.shortcut_repository.find_shortcut_by_keycode_and_program(",".join(map(str, event.pressed_keys))
                                                                                 , event.program)
        if shortcut is not None:
            old_effectiveness = self.statistic_collector.calculate_button_effectiveness_statistic(shortcut.button)
            self.statistic_collector.collect_shortcut_statistics(shortcut)
            new_effectiveness = self.statistic_collector.calculate_button_effectiveness_statistic(shortcut.button)

            message = self._get_effectiveness_message(old_effectiveness, new_effectiveness)
            if message != "":
                Notify.show_notification(message)

    def _save_event_screenshot(self, event):
        event.screenshot.save("screenshot_x_" + str(event.click_x) + "_y_" + str(event.click_y) + ".png", "PNG")

    def _get_effectiveness_message(self, old_effectiveness, new_effectiveness):
        effectiveness_change = old_effectiveness - new_effectiveness
        if effectiveness_change > self.effectiveness_change_threshold:
            return "Your effectiveness has decreased by %.2f %%. Try to work a bit harder" % effectiveness_change
        elif -effectiveness_change > self.effectiveness_change_threshold:
            return "Your effectiveness has increased by %.2f %%. Keep up the good work" % -effectiveness_change
        else:
            return ""
