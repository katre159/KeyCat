class EventReceiver(object):
    @staticmethod
    def receive_mouse_event(event):
        print("MouseEvent: x = %s, y = %s, screenshot = %s" % (event.click_x, event.click_y, event.screenshot))
        event.screenshot.save("screenshot_x_" + str(event.click_x) + "_y_" + str(event.click_y) + ".png", "PNG")

    @staticmethod
    def receive_keyboard_state_change_event(event):
        print("Keys pressed : %s" % event.pressed_keys)
