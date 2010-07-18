#!/usr/bin/env python
#
# Copyright 2010 The Protojson Authors. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#	  http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS-IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import os
import sys
import unittest


def getSuite():
	suite = unittest.TestLoader().loadTestsFromNames([
		'protojson.test_pbliteserializer.PbLiteSerializeTests',
		'protojson.test_pbliteserializer.PbLiteDeserializeWrongObjectTests',
	])
	return suite


def main():
	runner = unittest.TextTestRunner()
	suite = getSuite()
	runner.run(suite)


def _parent(path):
	return os.path.dirname(path)


if __name__ == '__main__':
	packageParentDir = _parent(_parent(os.path.abspath(__file__)))
	sys.path.insert(0, packageParentDir)
	print "sys.path[0] is now", repr(sys.path[0])
	print
	print "Note that unittest swallows import-time exceptions.  If you see below"
	print "\"AttributeError: 'module' object has no attribute 'test_pbliteserializer'\","
	print "make sure that google.protobuf is in your PYTHONPATH."
	print "=" * 78
	main()
