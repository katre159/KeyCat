from models import ShortcutStat, ButtonStat


class StatisticCollector(object):
    def __init__(self, shortcut_stat_repository, button_stat_repository):
        self.shortcut_stat_repository = shortcut_stat_repository
        self.button_stat_repository = button_stat_repository

    def calculate_button_effectiveness_statistic(self, button):
        button_hit_count = 0
        shortcuts_hit_count = 0

        button_stat = self._get_button_stat(button)
        if button_stat is not None:
            button_hit_count = button_stat.hit_count

        shortcuts_hit_count = sum(map(lambda x: self._get_shortcut_stat(x).hit_count, button.shortcuts))

        total_action_count = button_hit_count + shortcuts_hit_count

        if total_action_count > 0:
            return (float(shortcuts_hit_count) / float(total_action_count))*100
        else:
            return 0

    def collect_button_statistics(self, button):
        button_stat = self._get_button_stat(button)
        button_stat.hit_count += 1
        self.button_stat_repository.save(button_stat)

    def collect_shortcut_statistics(self, shortcut):
        shortcut_stat = self._get_shortcut_stat(shortcut)
        shortcut_stat.hit_count += 1
        self.shortcut_stat_repository.save(shortcut_stat)

    def _get_shortcut_stat(self, shortcut):
        shortcut_stat = self.shortcut_stat_repository.find_shortcut_stat_by_keycode_and_program(
            shortcut.keycodes, shortcut.button.program)
        if shortcut_stat is None:
            shortcut_stat = ShortcutStat(shortcut, 0)

        return shortcut_stat

    def _get_button_stat(self, button):
        button_stat = self.button_stat_repository.find_button_stat_by_button(button)
        if button_stat is None:
            button_stat = ButtonStat(button, 0)

        return button_stat
