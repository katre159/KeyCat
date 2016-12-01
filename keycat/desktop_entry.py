import os
from os.path import expanduser
import shutil


def create_desktop_entry():
    destination = os.path.join(expanduser("~"), '.local', 'share', 'applications')
    filename = 'keycat.desktop'

    shutil.copy(filename, destination)
