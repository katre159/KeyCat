import abc
from models import Button, Shortcut, ShortcutStat


class BaseRepository(object):
    def __init__(self, session):
        self.session = session


class AbstractButtonRepository(BaseRepository):
    @abc.abstractmethod
    def find_all_buttons(self):
        return []

    @abc.abstractmethod
    def save_button(self, button):
        pass

    @abc.abstractmethod
    def find_buttons_by_program(self, program):
        pass


class ButtonRepository(AbstractButtonRepository):
    def find_all_buttons(self):
        return self.session.query(Button).all()

    def save_button(self, button):
        self.session.add(button)
        self.session.commit()

    def find_buttons_by_program(self, program):
        return self.session.query(Button).filter_by(program=program).all()


class AbstractShortcutRepository(BaseRepository):
    @abc.abstractmethod
    def find_shortcut_by_keycode_and_program(self, keycode, program):
        pass


class ShortcutRepository(AbstractShortcutRepository):
    def find_shortcut_by_keycode_and_program(self, keycode, program):
        return self.session.query(Shortcut).join(Shortcut.button) \
            .filter(Button.program == program, Shortcut.keycodes == keycode).first()


class AbstractShortcutStatRepository(BaseRepository):
    @abc.abstractmethod
    def find_shortcut_stat_by_keycode_and_program(self, keycode, program):
        pass

    @abc.abstractmethod
    def save_shortcut_stat(self, shortcut_stat):
        pass


class ShortcutStatRepository(AbstractShortcutStatRepository):
    def find_shortcut_stat_by_keycode_and_program(self, keycode, program):
        return self.session.query(ShortcutStat).join(ShortcutStat.shortcut).join(Shortcut.button) \
            .filter(Button.program == program, Shortcut.keycodes == keycode).first()

    def save_shortcut_stat(self, shortcut_stat):
        self.session.add(shortcut_stat)
        self.session.commit()
