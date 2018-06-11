# -*- coding: utf-8 -*-
from setuptools import setup

package = 'ezdeploy'
version = '0.1'

setup(name=package,
      version=version,
      description="a simple auto deploy tools",
      url='https://github.com/noca/ezdeploy.git',
      install_requires=[
          'bottle',
          'bottle-sqlalchemy',
          'sqlalchemy',
          'PyYAML',
          'requests',
          'ansible'
      ])
