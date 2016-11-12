from Xlib.display import Display
from Xlib import X
import os


class Error(Exception):
    """Base class for exceptions in this module."""
    pass


class NoTopWindowFoundError(Error):
    def __init__(self, message):
        self.message = message


class CantGetPIDOfWindowError(Error):
    def __init__(self, message):
        self.message = message


class ProgramIdentifier(object):
    def __init__(self):
        self.display = Display()
        self.pid_atom = self.display.get_atom("_NET_WM_PID")

    def get_active_program(self):
        pid = self._get_top_window_pid()
        realpath = self._get_pid_realpath(pid)
        return self._get_program_name_from_path(realpath)

    def _get_pid_realpath(self, pid):
        return os.path.realpath('/proc/' + str(pid) + '/exe')

    def _get_program_name_from_path(self, path):
        return path.split("/")[-1]

    def _get_top_window_pid(self):
        top_window = self._get_top_window()
        if top_window is not None:
            pid = self._get_window_pid(top_window)
            if pid is None:
                raise CantGetPIDOfWindowError("")
            return pid
        else:
            raise NoTopWindowFoundError("")

    def _get_top_window(self):
        focused_window = self.display.get_input_focus().focus
        if focused_window is not None and focused_window != X.NONE and focused_window != X.PointerRoot:
            parent = focused_window

            while (True):
                if self.pid_atom in parent.list_properties():
                    break
                query_result = parent.query_tree()
                root = query_result.root
                parent = query_result.parent

                if root.id == parent.id:
                    break

            return parent

        return None

    def _get_window_pid(self, window):
        if self.pid_atom in window.list_properties():
            value = window.get_full_property(self.pid_atom, X.AnyPropertyType).value
            if value is not None and len(value) == 1:
                return value[0]

        return None
