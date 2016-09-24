from setuptools import setup
import os

setup(
    name = "Merengue",
    version = "1.0",
    author = "John Carter",
    author_email = "jcarter2010@comcast.net",
    description = "Raspberry Pi/Linux text editor",
    license = "BSD",
    url = "https://github.com/JCarter2010/Merengue",
    packages=['merengue'],
    package_data = {'merengue.data': ['*']},
    entry_points={ 'gui_scripts': [ 'merengue=merengue.merengue:main' ] },
    data_files=[ ('share/icons', ['data/icon.gif']), ('share/applications', ['data/merengue.desktop']) ],
)
