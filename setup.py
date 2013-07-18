#!/usr/bin/python

"""
Setup script for the mallard project.

kieran.renfrew.campbell@cern.ch

"""

from setuptools import setup

mallard_version = 0.1

setup(name="mallard",
      version=mallard_version,
      description="DAQ for CRIS@ISOLDE",
      author="CERN",
      author_email="kieran.renfrew.campbell@cern.ch",
      packages=['mallard'],
      zip_safe=False,
      install_requires=[
          'wx',
          'PyDAQmx',
          'numpy'
          ]
      )


