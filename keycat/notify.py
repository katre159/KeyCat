import subprocess


class Notify:

    @staticmethod
    def show_notification(message):
        subprocess.Popen(['notify-send', message])
        return
