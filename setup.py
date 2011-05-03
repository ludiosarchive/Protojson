#!/usr/bin/env python

from distutils.core import setup

import protojson

setup(
	name='protojson',
	version=protojson.__version__,
	description="Convert any google.protobuf.message.Message to and from " +
		"a format supported by Closure Library's goog.proto2",
	url="https://github.com/ludios/Protojson",
	author="Ivan Kozik",
	author_email="ivan@ludios.org",
	classifiers=[
		'Programming Language :: Python :: 2',
		'Development Status :: 5 - Production/Stable',
		'Operating System :: OS Independent',
		'Intended Audience :: Developers',
		'License :: OSI Approved :: MIT License',
	],
	packages=['protojson'],
)
