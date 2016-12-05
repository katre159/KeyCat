#!/usr/bin/env bash

apt-get install libnotify-bin
apt-get install python-opencv
apt-get install python-pip
apt-get install python-gobject
apt-get install imagemagick

python setup.py develop
