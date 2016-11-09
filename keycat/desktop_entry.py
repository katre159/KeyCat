import os.path
from shutil import copyfile


def create_desktop_entry():
    destination = '/usr/share/applications/keycat.desktop'
    filename = 'keycat.desktop'

    if not os.path.isfile(destination):
        copyfile(filename, destination)
