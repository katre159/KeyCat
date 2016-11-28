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

    def test_collect_shortcut_statistics_not_exists_in_database_added_with_hitcount_1(self):
        keycodes = "37,42"
        program = "test_program"
        id = "test_button_id"
        shortcut = Shortcut(keycodes)
        shortcut.button = Button(id, program, "", [], [])

        self.statistic_collector.collect_shortcut_statistics(shortcut)
        self.mock_shortcut_stat_repository.find_shortcut_stat_by_keycode_and_program.assert_called_with(
            keycodes, program)
        self.mock_shortcut_stat_repository.save.assert_called_with(ShortcutStat(shortcut, 1))

    def test_collect_shortcut_statistics_exists_added_with_inc_hitcount(self):
        keycodes = "37,42"
        program = "test_program"
        shortcut = Shortcut(keycodes)
        id = "test_button_id"
        shortcut.button = Button(id, program, "", [], [])
        self.mock_shortcut_stat_repository.find_shortcut_stat_by_keycode_and_program = MagicMock(
            return_value=ShortcutStat(shortcut, 1))
        self.statistic_collector.collect_shortcut_statistics(shortcut)
        self.mock_shortcut_stat_repository.find_shortcut_stat_by_keycode_and_program.assert_called_with(
            keycodes, program)
        self.mock_shortcut_stat_repository.save.assert_called_with(ShortcutStat(shortcut, 2))

    def test_collect_button_statistics_not_exists_in_database_added_with_hitcount_1(self):
        program = "test_program"
        id = "test_button_id"
        button = Button(id, program, "", [], [])
        self.statistic_collector.collect_button_statistics(button)
        self.mock_button_stat_repository.find_button_stat_by_button.assert_called_with(button)
        self.mock_button_stat_repository.save.assert_called_with(ButtonStat(button, 1))

    def test_collect_button_statistics_exists_added_with_inc_hitcount(self):
        program = "test_program"
        id = "test_button_id"
        button = Button(id, program, "", [], [])
        self.mock_button_stat_repository.find_button_stat_by_button = MagicMock(return_value=ButtonStat(button, 1))
        self.statistic_collector.collect_button_statistics(button)
        self.mock_button_stat_repository.find_button_stat_by_button.assert_called_with(button)
        self.mock_button_stat_repository.save.assert_called_with(ButtonStat(button, 2))

    def test_collect_button_effectiveness_statistic_one_shortcut(self):
        program = "test_program"
        keycodes = "37,42"
        id = "test_button_id"
        shortcut = Shortcut(keycodes)
        button = Button(id, program, "", [], [shortcut])
        shortcut.button = button
        self.mock_button_stat_repository.find_button_stat_by_button = MagicMock(return_value=ButtonStat(button, 7))
        self.mock_shortcut_stat_repository.find_shortcut_stat_by_keycode_and_program = MagicMock(
            return_value=ShortcutStat(shortcut, 3))
        effectiveness = self.statistic_collector.calculate_button_effectiveness_statistic(button)
        self.assertEqual(effectiveness, 30.0)

    def test_collect_button_effectiveness_statistic_many_shortcuts(self):
        program = "test_program"
        keycodes1 = "37,42"
        keycodes2 = "37,45"
        id = "test_button_id"
        shortcut1 = Shortcut(keycodes1)
        shortcut2 = Shortcut(keycodes2)
        button = Button(id, program, "", [], [shortcut1, shortcut2])
        shortcut1.button = button
        shortcut2.button = button
        self.mock_button_stat_repository.find_button_stat_by_button = MagicMock(return_value=ButtonStat(button, 5))
        self.mock_shortcut_stat_repository.find_shortcut_stat_by_keycode_and_program = MagicMock(
            side_effect=[ShortcutStat(shortcut1, 3), ShortcutStat(shortcut2, 2)])
        effectiveness = self.statistic_collector.calculate_button_effectiveness_statistic(button)
        self.assertEqual(effectiveness, 50.0)

    def test_collect_button_effectiveness_statistic_button_stat_is_none(self):
        program = "test_program"
        id = "test_button_id"
        keycodes = "37,42"
        shortcut = Shortcut(keycodes)
        button = Button(id, program, "", [], [shortcut])
        shortcut.button = button
        self.mock_button_stat_repository.find_button_stat_by_button = MagicMock(return_value=None)
        self.mock_shortcut_stat_repository.find_shortcut_stat_by_keycode_and_program = MagicMock(
            return_value=ShortcutStat(shortcut, 3))
        effectiveness = self.statistic_collector.calculate_button_effectiveness_statistic(button)
        self.assertEqual(effectiveness, 100.0)

    def test_collect_button_effectiveness_statistic_shortcut_stat_is_none(self):
        program = "test_program"
        keycodes = "37,42"
        id = "test_button_id"
        shortcut = Shortcut(keycodes)
        button = Button(id, program, "", [], [shortcut])
        shortcut.button = button
        self.mock_button_stat_repository.find_button_stat_by_button = MagicMock(return_value=ButtonStat(button, 7))
        self.mock_shortcut_stat_repository.find_shortcut_stat_by_keycode_and_program = MagicMock(
            return_value=None)
        effectiveness = self.statistic_collector.calculate_button_effectiveness_statistic(button)
        self.assertEqual(effectiveness, 0.0)
