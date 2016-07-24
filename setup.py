from distutils.core import setup
import sys
import os

setup(name='merengue',
      description='A Raspberry Pi text editor',
      version='1.0',
      py_modules=['merengue'],
      )

path = os.path.abspath(__file__)

#sys.path.insert(0, path)
os.system('PATH=$PATH:' + path)
