import abc
from models import Button, Shortcut, ShortcutStat, ButtonStat


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
    def delete(self, button):
        pass

    @abc.abstractmethod
    def find_buttons_by_program(self, program):
        pass


class ButtonRepository(AbstractButtonRepository):
    def find_all_buttons(self):
        return self.session.query(Button).all()

    def save_button(self, button):
        self.session.merge(button)
        self.session.commit()

    def delete(self, button):
        self.session.delete(button)
        self.session.commit()

    def find_buttons_by_program(self, program):
        return self.session.query(Button).filter_by(program=program).all()


class AbstractShortcutRepository(BaseRepository):
    @abc.abstractmethod
    def find_shortcut_by_keycode_and_program(self, keycode, program):
        pass


class ShortcutRepository(AbstractShortcutRepository):
    def find_shortcut_by_keycode_and_program(self, keycode, program):
        return self.session.query(Shortcut).join(Shortcut.button).filter(
            Button.program == program, Shortcut.keycodes == keycode).first()


class AbstractShortcutStatRepository(BaseRepository):
    @abc.abstractmethod
    def find_shortcut_stat_by_keycode_and_program(self, keycode, program):
        pass

    @abc.abstractmethod
    def delete_button_shortcut_stats(self, button):
        pass

    @abc.abstractmethod
    def save(self, shortcut_stat):
        pass


class ShortcutStatRepository(AbstractShortcutStatRepository):
    def find_shortcut_stat_by_keycode_and_program(self, keycode, program):
        return self.session.query(ShortcutStat).join(ShortcutStat.shortcut).join(Shortcut.button).filter(
            Button.program == program, Shortcut.keycodes == keycode).first()

    def delete_button_shortcut_stats(self, button):
        self.session.query(ShortcutStat).filter(ShortcutStat.shortcut.has(button=button)).delete(
            synchronize_session=False)
        self.session.commit()

    def save(self, shortcut_stat):
        self.session.add(shortcut_stat)
        self.session.commit()


class AbstractButtonStatRepository(BaseRepository):
    @abc.abstractmethod
    def find_button_stat_by_button(self, button):
        pass

    @abc.abstractmethod
    def delete_button_stats(self, button):
        pass

    @abc.abstractmethod
    def save(self, button_stat):
        pass


class ButtonStatRepository(AbstractButtonStatRepository):

    def find_button_stat_by_button(self, button):
        return self.session.query(ButtonStat).filter(ButtonStat.button == button).first()

    def delete_button_stats(self, button):
        self.session.query(ButtonStat).filter(ButtonStat.button == button).delete(
            synchronize_session=False)
        self.session.commit()

    def save(self, button_stat):
        self.session.add(button_stat)
        self.session.commit()
