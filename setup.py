from setuptools import setup

setup(
    name='merengue',
    install_requires=['paramiko'],
    entry_points={
        'qui_scripts': ['merengue = merengue.__main__:main']},
    version='1.0.4',
    author='John Carter',
    author_email='jcarter2010@comcast.net',
    packages=['merengue'],
    package_dir={'merengue': 'merengue'},
    description='Merengue text editor for Linux/Windows/Raspbian.')
