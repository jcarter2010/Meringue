from setuptools import setup

setup(
    name='merengue',
    entry_points={
        'console_scripts': ['merengue = merengue.merengue:main']},
    version='1.0.0',
    author='John Carter',
    author_email='jcarter2010@comcast.net',
    packages=['merengue'],
    package_dir={'merengue': 'merengue'},
    description='Merengue text editor for Linux/Windows/Raspbian.')
