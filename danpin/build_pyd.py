# -*- coding: utf-8 -*-
from distutils.core import setup
from Cython.Build import cythonize
setup(
  name = 'oneKeyCopy',
  ext_modules = cythonize(["register.py"])
)
