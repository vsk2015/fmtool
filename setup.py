#!/usr/bin/env python
'''
Setup for fmcheck
'''
from setuptools import setup, find_packages

setup(name='fmcheck',
      version='1.0',
      description='CLI for performing comparison between network and SDN controller state',
      license='MIT',
      author='Lumina NetDev',
      url='https://github.com/luminanetworks/fmcheck',
      packages=find_packages(exclude=['tests']),
      install_requires=[
        'docopt==0.6.2','pyyaml','requests','pexpect','coloredlogs'
      ],
      keywords='lumina luminanetworks netdev flowmanager flow manager cli fmcheck',
      classifiers=[
          'Development Status :: 5 - Production/Stable',
          'Intended Audience :: Developers',
          'Intended Audience :: Telecommunications Industry',
          'License :: OSI Approved :: Apache Software License',
          'Operating System :: OS Independent',
          'Programming Language :: Python',
          'Programming Language :: Python :: 2.7',
          'Topic :: Software Development :: Libraries',
          'Topic :: Software Development :: Libraries :: Python Modules',
          'Topic :: System :: Networking'
      ],
      entry_points={
          'console_scripts': [
              'lscli = fmcheck.cli:main'
          ]
      })
