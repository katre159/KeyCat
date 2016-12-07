import os
from os.path import expanduser
import shutil


def create_desktop_entry():
    destination = os.path.join(expanduser("~"), '.local', 'share', 'applications')
    dir = os.path.dirname(__file__)
    target = os.path.join(dir, '..', 'keycat.desktop')

    shutil.copy(target, destination)
