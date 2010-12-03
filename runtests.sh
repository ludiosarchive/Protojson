#!/bin/sh -e

# If this doesn't work, or if you want to obtain coverage
# information, install Twisted and run `trial --coverage protojson`

MYPY_CONSTANT_BINDER_AUTOENABLE=0 time python     -W all protojson/run_tests.py
MYPY_CONSTANT_BINDER_AUTOENABLE=1 time python     -W all protojson/run_tests.py
MYPY_CONSTANT_BINDER_AUTOENABLE=0 time python -O  -W all protojson/run_tests.py
MYPY_CONSTANT_BINDER_AUTOENABLE=1 time python -O  -W all protojson/run_tests.py
MYPY_CONSTANT_BINDER_AUTOENABLE=0 time python -OO -W all protojson/run_tests.py
MYPY_CONSTANT_BINDER_AUTOENABLE=1 time python -OO -W all protojson/run_tests.py

MYPY_CONSTANT_BINDER_AUTOENABLE=0 time pypy       -W all protojson/run_tests.py
MYPY_CONSTANT_BINDER_AUTOENABLE=1 time pypy       -W all protojson/run_tests.py
