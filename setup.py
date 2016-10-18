from setuptools import setup
#import distutils
import py2exe
import os

setup(
    name = "Meringue",
    version = "1.0",
    author = "John Carter",
    author_email = "jcarter2010@comcast.net",
    description = "Raspberry Pi/Linux/Windows/OS X text editor",
    license = "BSD",
    url = "https://github.com/JCarter2010/Merengue",
    packages=['meringue'],
    package_data = {'meringue.data': ['*']},
    entry_points={ 'gui_scripts': [ 'meringue=meringue.meringue:main' ] },
    data_files=[ ('share/icons', ['data/icon.gif']), ('share/applications', ['data/meringue.desktop']) ],
)
