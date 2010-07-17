# Copyright 2010 The Protojson Authors. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS-IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


from unittest import TestCase
from protojson import pbliteserializer, alltypes_pb2


class PbLiteSerializeTests(TestCase):
	"""
	Tests for L{pbliteserializer.PbLiteSerializer.serialize}.
	"""
	def test_defaults(self):
		tat = alltypes_pb2.TestAllTypes()
		serializer = pbliteserializer.PbLiteSerializer()
		ser = serializer.serialize(tat)

		self.assertEqual([
			None, # 0
			0, # 1
			1, # 2
			0, # and so on
			0,
			0,
			0,
			0,
			0,
			0,
			0,
			1.5,
			0,
			0,
			u'',
			'moo',
			[None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, 0], # 16
			None, # 17
			[None, 0],
			None,
			None,
			1,
			None,
			None,
			None,
			None,
			None,
			None,
			None,
			None,
			None,
			[], # 31
			[],
			[],
			[],
			[],
			[],
			[],
			[],
			[],
			[],
			[],
			[],
			[],
			[],
			[],
			[], # 46
			None, # 47
			[], # 48
			[], # 49
		], ser)
