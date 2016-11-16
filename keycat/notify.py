import subprocess


class Notify:

    @staticmethod
    def show_notification(message):
        subprocess.Popen(['notify-send', message, '-t', '3000'])
        return
