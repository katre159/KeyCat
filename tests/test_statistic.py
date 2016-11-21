from keycat.repository import AbstractShortcutStatRepository, AbstractButtonStatRepository
from keycat.statistic import StatisticCollector
from keycat.models import Shortcut, Button, ShortcutStat, ButtonStat
import unittest
from mock import MagicMock


class StatisticCollectorTest(unittest.TestCase):
    def setUp(self):
        self.mock_shortcut_stat_repository = AbstractShortcutStatRepository(None)
        self.mock_shortcut_stat_repository.find_shortcut_stat_by_keycode_and_program = MagicMock(return_value=None)
        self.mock_shortcut_stat_repository.save = MagicMock()

        self.mock_button_stat_repository = AbstractButtonStatRepository(None)
        self.mock_button_stat_repository.find_button_stat_by_button = MagicMock(return_value=None)
        self.mock_button_stat_repository.save = MagicMock()

        self.statistic_collector = StatisticCollector(
            self.mock_shortcut_stat_repository, self.mock_button_stat_repository)

    def test_calculate_shortcut_statistics_not_exists_in_database_added_with_hitcount_1(self):
        keycodes = "37,42"
        program = "test_program"
        shortcut = Shortcut(keycodes)
        shortcut.button = Button(program, [], [])

        returned_stat = self.statistic_collector.calculate_shortcut_statistics(shortcut)
        self.mock_shortcut_stat_repository.find_shortcut_stat_by_keycode_and_program.assert_called_with(
            keycodes, program)
        self.mock_shortcut_stat_repository.save.assert_called_with(ShortcutStat(shortcut, 1))
        self.assertEqual(returned_stat, ShortcutStat(shortcut, 1))

    def test_calculate_shortcut_statistics_exists_added_with_inc_hitcount(self):
        keycodes = "37,42"
        program = "test_program"
        shortcut = Shortcut(keycodes)
        shortcut.button = Button(program, [], [])
        self.mock_shortcut_stat_repository.find_shortcut_stat_by_keycode_and_program = MagicMock(
            return_value=ShortcutStat(shortcut, 1))
        returned_stat = self.statistic_collector.calculate_shortcut_statistics(shortcut)
        self.mock_shortcut_stat_repository.find_shortcut_stat_by_keycode_and_program.assert_called_with(
            keycodes, program)
        self.mock_shortcut_stat_repository.save.assert_called_with(ShortcutStat(shortcut, 2))
        self.assertEqual(returned_stat, ShortcutStat(shortcut, 2))

    def test_calculate_button_statistics_not_exists_in_database_added_with_hitcount_1(self):
        program = "test_program"
        button = Button(program, [], [])
        returned_stat = self.statistic_collector.calculate_button_statistics(button)
        self.mock_button_stat_repository.find_button_stat_by_button.assert_called_with(button)
        self.mock_button_stat_repository.save.assert_called_with(ButtonStat(button, 1))
        self.assertEqual(returned_stat, ButtonStat(button, 1))

    def test_calculate_button_statistics_exists_added_with_inc_hitcount(self):
        program = "test_program"
        button = Button(program, [], [])
        self.mock_button_stat_repository.find_button_stat_by_button = MagicMock(return_value=ButtonStat(button, 1))
        returned_stat = self.statistic_collector.calculate_button_statistics(button)
        self.mock_button_stat_repository.find_button_stat_by_button.assert_called_with(button)
        self.mock_button_stat_repository.save.assert_called_with(ButtonStat(button, 2))
        self.assertEqual(returned_stat, ButtonStat(button, 2))
