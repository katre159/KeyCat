from setuptools import setup
from keycat import _VERSION

setup(
    name='KeyCat',
    version=_VERSION,
    packages=['keycat'],
    url='https://github.com/KatreMetsvahi/KeyCat',
    download_url='https://github.com/KatreMetsvahi/KeyCat/tarball/' + _VERSION,
    license='',
    author='',
    author_email='',
    description='KeyCat',
    test_suite="tests",
    include_package_data=True,
    install_requires=[
        'Pillow',
        'pyscreenshot',
        'PyUserInput',
        'screeninfo',
        'python-xlib',
        'SQLAlchemy'
    ],
    entry_points={
        'console_scripts': [
            'keycat=keycat.__main__:main',
        ],
    },
    tests_require=['mock']
)
