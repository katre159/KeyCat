import os
from PIL.PngImagePlugin import PngImageFile
from keycat.models import Button, Base, Template
from keycat.picture_util import *
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker


def setup_database(engine):
    base = Base
    base.metadata.drop_all(engine)
    base.metadata.create_all(engine)


def get_database_scoped_session():
    engine = create_engine('sqlite:///database.db')
    setup_database(engine)
    session_factory = sessionmaker(bind=engine)
    return scoped_session(session_factory)


def load_data(button_repository):
    directory = os.path.dirname(os.path.abspath(__file__))
    button_template = PngImageFile(os.path.join(directory, 'data/new_tab_template_chrome.png'))
    button_template = convert_picture_to_grayscale(button_template)
    button_template = convert_picture_to_numpy_array(button_template).tobytes()

    template = Template(button_template, 24, 324)

    button_templates = [template]

    button = Button(button_templates)
    button_repository.save_button(button)
