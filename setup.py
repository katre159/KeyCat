from setuptools import setup, find_packages
from keycat import _VERSION
from setuptools.command.install import install
import os
from os.path import expanduser


class OverrideInstall(install):
    def run(self):
        mode = 0o777
        install.run(self)

        for filepath in self.get_outputs():
            if "data/" in filepath:
                os.chmod(os.path.dirname(filepath), mode)
                os.chmod(filepath, mode)
                
destination = os.path.join(expanduser("~"), '.local', 'share', 'applications')
icon_destination = os.path.join(expanduser("~"), '.local', 'share', 'icons', 'hicolor', '256x256', 'apps')
icon_small_destination = os.path.join(expanduser("~"), '.local', 'share', 'icons', 'hicolor', '22x22', 'apps')

setup(
    name='KeyCat',
    version=_VERSION,
    packages=find_packages(),
    package_data={'': ['*.db', '*.png', '*.json']},
    url='https://github.com/KatreMetsvahi/KeyCat',
    download_url='https://github.com/KatreMetsvahi/KeyCat/tarball/' + _VERSION,
    license='',
    author='',
    author_email='',
    description='KeyCat',
    test_suite="tests",
    install_requires=[
        'Pillow>=3.4.2',
        'pyscreenshot>=0.4.2',
        'PyUserInput>=0.1.11',
        'screeninfo>=0.2.1',
        'python-xlib>=0.17',
        'SQLAlchemy>=1.1.3'
    ],
    data_files=[
        (destination, ['keycat.desktop']),
        (icon_destination, ['keycat.png']),
        (icon_small_destination, ['keycat-small.png'])
    ],
    entry_points={
        'console_scripts': [
            'keycat=keycat.__main__:main',
        ],
    },
    tests_require=['mock'],
    cmdclass={'install': OverrideInstall}
)
