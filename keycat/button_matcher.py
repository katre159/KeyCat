from collections import namedtuple


class Click(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y


class ButtonMatcher(object):
    def __init__(self, template_matcher, button_repository):
        self.template_matcher = template_matcher
        self.button_repository = button_repository

    def find_button_on_clicked_position(self, click, picture, program):
        buttons = self.button_repository.find_buttons_by_program(program)
        for button in buttons:
            template_position = self._get_matched_template_position_on_picture(button, picture)
            if template_position is not None and self._is_click_inside_template(click, template_position):
                return button

        return None

    def _get_matched_template_position_on_picture(self, button, picture):
        TemplatePosition = namedtuple('TemplatePosition', 'template x y')
        for template in button.templates:
            position = self.template_matcher.get_template_location(template.get_template_as_numpy_array(), picture)
            if position is not None:
                return TemplatePosition(template, position[0], position[1])

        return None

    def _is_click_inside_template(self, click, template_position):
        template_height = template_position.template.height
        template_width = template_position.template.width
        return click.x >= template_position.x and click.x <= template_position.x + template_width \
               and click.y >= template_position.y and click.y <= template_position.y + template_height
