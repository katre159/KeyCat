import os
from os.path import expanduser
import shutil


def create_desktop_entry():
    destination = os.path.join(expanduser("~"), '.local', 'share', 'applications')
    target = os.path.join('..', 'keycat.desktop')

    shutil.copy(target, destination)
