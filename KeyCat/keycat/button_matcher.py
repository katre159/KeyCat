from collections import namedtuple


class ButtonMatcher(object):
    def __init__(self, template_matcher, button_repository):
        self.template_matcher = template_matcher
        self.button_repository = button_repository

    def find_button_on_clicked_position(self, click_x, click_y, picture):

        buttons = self.button_repository.find_all_buttons()
        for button in buttons:
            template_position = self.__get_matched_template_position_on_picture(button, picture)
            if template_position is not None and self.__is_click_inside_template(click_x, click_y, template_position):
                return button

        return None

    def __get_matched_template_position_on_picture(self, button, picture):
        TemplatePosition = namedtuple('TemplatePosition', 'template x y')
        for template in button.templates:
            position = self.template_matcher.get_template_location(template, picture)
            if position is not None:
                return TemplatePosition(template, position[0], position[1])

        return None

    def __is_click_inside_template(self, click_x, click_y, template_position):
        template_height = template_position.template.shape[0]
        template_width = template_position.template.shape[1]
        return click_x >= template_position.x and click_x <= template_position.x + template_width \
               and click_y >= template_position.y and click_y <= template_position.y + template_height
