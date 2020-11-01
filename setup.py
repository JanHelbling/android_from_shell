#!/usr/bin/python3
# -*- coding: utf-8 -*-

from distutils.core import setup

setup(name='android_from_shell.py',
      version='0.1',
      description='Create AndroidApps from SHELL without GUI.',
      license='GPL3+',
      author='Jan Helbling',
      author_email='jh@jan-helbling.ch',
      url='https://github.com/JanHelbling/android_from_shell.git',
      platforms=['linux','freebsd','netbsd','unixware7' , 'openbsd' , 'windows'],
      scripts=['bin/android_from_shell.py'],
)
