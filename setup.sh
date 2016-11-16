#!/usr/bin/env bash

apt-get install libnotify-bin
apt-get install python-opencv
apt-get install python-pip

python setup.py install

# Fallback
pip install Pillow
pip install pyscreenshot
pip install PyUserInput
pip install screeninfo
pip install python-xlib
pip install SQLAlchemy