from models import ShortcutStat, ButtonStat


class StatisticCollector(object):
    def __init__(self, shortcut_stat_repository, button_stat_repository):
        self.shortcut_stat_repository = shortcut_stat_repository
        self.button_stat_repository = button_stat_repository

    def button_pressed(self, button):
        button_stat = self.button_stat_repository.find_button_stat_by_button(button)
        if button_stat is not None:
            button_stat.hit_count += 1
        else:
            button_stat = ButtonStat(button, 1)

        self.button_stat_repository.save(button_stat)

        return button_stat


    def shortcut_pressed(self, shortcut):
        shortcut_stat = self.shortcut_stat_repository.find_shortcut_stat_by_keycode_and_program(
            shortcut.keycodes, shortcut.button.program)
        if shortcut_stat is not None:
            shortcut_stat.hit_count += 1
        else:
            shortcut_stat = ShortcutStat(shortcut, 1)

        self.shortcut_stat_repository.save(shortcut_stat)
        return shortcut_stat
