import abc
from models import ProgramButton
import os
from picture_util import *
from PIL.PngImagePlugin import PngImageFile


class AbstractButtonRepository(object):
    @abc.abstractmethod
    def find_all_buttons(self):
        return []


class HardCodedButtonReposotory(AbstractButtonRepository):
    def __init__(self):
        self.directory = os.path.dirname(os.path.abspath(__file__))
        button_template = PngImageFile(os.path.join(self.directory, 'data/new_tab_template_chrome.png'))
        button_template = convert_picture_to_grayscale(button_template)
        button_template = convert_picture_to_numpy_array(button_template)
        button_templates = [button_template]
        button_key_coeds = [[]]
        button = ProgramButton(button_templates, button_key_coeds)
        self.buttons = [button]

    def find_all_buttons(self):
        return self.buttons
