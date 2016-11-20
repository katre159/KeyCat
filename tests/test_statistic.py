from keycat.repository import AbstractShortcutStatRepository
from keycat.statistic import StatisticCollector
from keycat.models import Shortcut, Button, ShortcutStat
import unittest
from mock import MagicMock


class StatisticCollectorTest(unittest.TestCase):
    def setUp(self):
        self.mock_shortcut_stat_repository = AbstractShortcutStatRepository(None)
        self.mock_shortcut_stat_repository.find_shortcut_stat_by_keycode_and_program = \
            MagicMock(return_value=None)
        self.mock_shortcut_stat_repository.save_shortcut_stat = MagicMock()

        self.statistic_collector = StatisticCollector(self.mock_shortcut_stat_repository)

    def test_shortcut_pressed_stat_not_exists(self):
        keycodes = "37,42"
        program = "test_program"
        shortcut = Shortcut(keycodes)
        shortcut.button = Button(program, [], [])

        self.statistic_collector.shortcut_pressed(shortcut)
        self.mock_shortcut_stat_repository. \
            find_shortcut_stat_by_keycode_and_program.assert_called_with(keycodes, program)
        self.mock_shortcut_stat_repository.save_shortcut_stat.assert_called_with(ShortcutStat(shortcut, 1))

    def test_shortcut_pressed_stat_exists(self):
        keycodes = "37,42"
        program = "test_program"
        shortcut = Shortcut(keycodes)
        shortcut.button = Button(program, [], [])
        self.mock_shortcut_stat_repository.find_shortcut_stat_by_keycode_and_program = \
            MagicMock(return_value=ShortcutStat(shortcut, 1))
        self.statistic_collector.shortcut_pressed(shortcut)
        self.mock_shortcut_stat_repository. \
            find_shortcut_stat_by_keycode_and_program.assert_called_with(keycodes, program)
        self.mock_shortcut_stat_repository.save_shortcut_stat.assert_called_with(ShortcutStat(shortcut, 2))
