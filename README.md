# KeyCat

## Overview
KeyCat is a program that works in the background, analyzing the user's keyboard and mouse actions. When KeyCat detects a mouse action that can also be performed with a keyboard, it shows a notification in the corner of the screen. A keyboard shortcut that can be used to achieve the same result is displayed in that notification. The notification will fade away on its own in order not to disrupt the normal workflow of the user. Over time the user will start remembering more shortcuts and become more proficient in using their keyboard.

KeyCat holds a list of program specific shortcuts, which can also be customized according to users' needs.

Users can also view statistics on their keyboard and mouse usage, which will give them an overview of their progress and encourage further improvements.

Although these kind of programs already exist, there are currently no programs like this for Linux, which is what we are going to change. Examples of currently existing programs: KeyRocket (Windows), AltMOUSE (Windows), Hotkey EVE (Mac), KeyCue (Mac).

## Installation
To install keycat run [install.sh](install.sh) script in terminal:
~~~
sudo sh install.sh
~~~

## Running
Run in terminal:
~~~
keycat
~~~
To close type Ctrl+z

## Contributing to the project
To set up the build environment for keycat follow these steps:
### Cloning
To clone this repository run
~~~
git clone <url>
~~~

### Updating
To pull the changes in this repository run
~~~
git pull
~~~

### Build from source code
To build project run in terminal
~~~
sudo apt-get install libnotify-bin python-opencv python-pip
sudo pip install Pillow pyscreenshot PyUserInput screeninfo python-xlib SQLAlchemy
~~~

### Run using source code
~~~~
python keycat
~~~~

### Close program
~~~~
ctrl + z
~~~~

### Running tests
~~~~
python setup.py test
~~~~
