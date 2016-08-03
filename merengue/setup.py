from setuptools import setup

setup(
    name='merengue',
    entry_points={
        'console_scripts': ['merengue = merengue:main']},
    version='1.0.0',
    author='John Carter',
    author_email='jcarter2010@comcast.net',
    packages=['merengue'],
    description='Merengue text editor for Linux/Windows/Raspbian.')
