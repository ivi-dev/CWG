#!/usr/local/bin/python3

from distutils.core import setup

setup(name='CWG',
      version='1.0',
      description='A casual word guessing game.',
      author='Iliyan Videv',
      author_email='videviliyan@gmail.com',
      url='https://github.com/ivi-dev/CWG/',
      packages=['src'],
      package_data={'': ['data/*.*']},
      )
