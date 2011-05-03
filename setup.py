#!/usr/bin/env python

from distutils.core import setup

import protojson

setup(
	name='protojson',
	version=protojson.__version__,
	description="Convert any google.protobuf.message.Message to and from " +
		"a format supported by Closure Library's goog.proto2",
	packages=['protojson'],
)
