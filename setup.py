from setuptools import setup

setup(
    name='KeyCat',
    version='0.0.1',
    packages=['keycat'],
    url='',
    license='',
    author='',
    author_email='',
    description='',
    test_suite="tests",
    include_package_data=True,
    install_requires=[
        'Pillow',
        'pyscreenshot',
        'PyUserInput',
        'screeninfo',
        'python-xlib'
      ],
    tests_require = ['mock']
)
