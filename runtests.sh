#!/bin/sh -e

# If this doesn't work, or if you want to obtain coverage
# information, install Twisted and run `trial --coverage protojson`

time python -W all protojson/run_tests.py
time pypy   -W all protojson/run_tests.py
