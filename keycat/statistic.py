from models import ShortcutStat


class StatisticCollector(object):
    def __init__(self, shortcut_stat_repository):
        self.shortcut_stat_repository = shortcut_stat_repository

    def shortcut_pressed(self, shortcut):
        shortcut_stat = self.shortcut_stat_repository.find_shortcut_stat_by_keycode_and_program(
            shortcut.keycodes, shortcut.button.program)
        if shortcut_stat is not None:
            shortcut_stat.hit_count += 1
        else:
            shortcut_stat = ShortcutStat(shortcut, 1)

        self.shortcut_stat_repository.save_shortcut_stat(shortcut_stat)
        return shortcut_stat
