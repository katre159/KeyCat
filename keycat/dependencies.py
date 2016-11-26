from mouse_events import FixedSizeScreenshotEventCreator
from events import EventReceiver
from screen import ScreenshotTaker, ScreenManager
from repository import ButtonRepository, ShortcutRepository, ShortcutStatRepository, ButtonStatRepository
from button_matcher import ButtonMatcher
from template_matcher import CCOEFFNORMEDTemplateMatcher
from database import *
from program_identifier import *
from statistic import StatisticCollector

session = get_database_scoped_session()
button_repository = ButtonRepository(session)
shortcut_repository = ShortcutRepository(session)
shortcut_stat_repository = ShortcutStatRepository(session)
button_stat_repository = ButtonStatRepository(session)
statistic_collector = StatisticCollector(shortcut_stat_repository, button_stat_repository)
program_identifier = ProgramIdentifier()
button_matcher = ButtonMatcher(CCOEFFNORMEDTemplateMatcher(), button_repository)
event_receiver = EventReceiver(button_matcher, shortcut_repository, statistic_collector)

mouse_event_creator = FixedSizeScreenshotEventCreator(ScreenshotTaker(), ScreenManager(), program_identifier,
                                                      700, 100)
