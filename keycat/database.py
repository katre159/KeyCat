import os
from PIL.PngImagePlugin import PngImageFile
from models import Button, Base, Template, Shortcut
from picture_util import *
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
import json


def setup_database(engine):
    base = Base
    if not (engine.dialect.has_table(engine, "shortcut_stat") and engine.dialect.has_table(engine, "button_stat")):
        base.metadata.drop_all(engine)
        base.metadata.create_all(engine)


def get_database_scoped_session():
    directory = os.path.dirname(os.path.abspath(__file__))
    engine = create_engine('sqlite:///' + os.path.join(directory, 'data/database.db'))
    setup_database(engine)
    session_factory = sessionmaker(bind=engine)
    return scoped_session(session_factory)


def load_buttons_from_config(directory, config_file):
    def load_template_from_file(file_path):

        button_template = PngImageFile(file_path)
        button_template = convert_picture_to_grayscale(button_template)
        button_template = convert_picture_to_numpy_array(button_template)
        return button_template

    def get_templates(template_files):
        result = []

        for template_file_path in template_files:
            template_numpy_array = load_template_from_file(os.path.join(directory, template_file_path))
            template = Template(template_numpy_array.tobytes(), template_numpy_array.shape[0],
                                template_numpy_array.shape[1])
            result.append(template)

        return result

    def get_shortcuts(shortcut_list):
        result = []

        for shortcut_values in shortcut_list:
            shortcut = Shortcut(",".join(map(str, shortcut_values)))
            result.append(shortcut)

        return result

    buttons = []

    with open(os.path.join(directory, config_file)) as data_file:
        data = json.load(data_file)

    for button in data["buttons"]:
        templates = get_templates(button["templates"])
        shortcuts = get_shortcuts(button["shortcuts"])
        buttons.append(Button(button["id"], button["program"], button["name"], templates, shortcuts))

    return buttons


def merge_shortcuts(shortcut, existing_shortcut):
    shortcut.id = existing_shortcut.id
    return shortcut


def merge_shortcuts_with_existing(shortcuts, existing_shortcuts):
    merged_shortcuts = []
    for shortcut in shortcuts:
        if shortcut in existing_shortcuts:
            merged_shortcuts.append(merge_shortcuts(shortcut, existing_shortcuts[existing_shortcuts.index(shortcut)]))
        else:
            merged_shortcuts.append(shortcut)
    return merged_shortcuts


def merge_buttons(button, existing_button):
    button.shortcuts = merge_shortcuts_with_existing(button.shortcuts, existing_button.shortcuts)
    return button


def merge_buttons_with_existing(buttons, existing_buttons):
    merged_buttons = []

    for button in buttons:
        if button in existing_buttons:
            merged_buttons.append(merge_buttons(button, existing_buttons[existing_buttons.index(button)]))
            existing_buttons.remove(button)
        else:
            merged_buttons.append(button)
    return (merged_buttons, existing_buttons)


def load_data_to_database(button_repository, shortcut_stat_repository, button_stat_repository):

    def delete_removed_buttons(buttons_for_deletion):
        for button in buttons_for_deletion:
            shortcut_stat_repository.delete_button_shortcut_stats(button)
            button_stat_repository.delete_button_stats(button)
            button_repository.delete(button)

    directory = os.path.dirname(os.path.abspath(__file__))
    buttons = load_buttons_from_config(directory, 'data/buttons_config.json')
    existing_buttons = button_repository.find_all_buttons()
    merged_buttons, buttons_for_deletion = merge_buttons_with_existing(buttons, existing_buttons)
    [button_repository.save_button(button) for button in merged_buttons]
    delete_removed_buttons(buttons_for_deletion)

