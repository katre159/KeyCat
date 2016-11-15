import abc
from keycat.models import Button


class AbstractButtonRepository(object):
    def __init__(self, session):
        self.session = session

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



