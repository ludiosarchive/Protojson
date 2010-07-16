#!/usr/bin/env python

from distutils.core import setup

import protojson

setup(
	name='protojson',
	version=protojson.__version__,
	description="Converts google.protobuf.message.Message <-> JSON, " +
		"where JSON is a format supported by Closure Library's goog.proto2",
	packages=['protojson'],
)
