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


class ButtonRepository(AbstractButtonRepository):
    def find_all_buttons(self):
        return self.session.query(Button).all()

    def save_button(self, button):
        self.session.add(button)
        self.session.commit()



