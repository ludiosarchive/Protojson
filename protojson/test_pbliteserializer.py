# Copyright 2010 The Protojson Authors. All Rights Reserved.
# Copyright 2008 The Closure Library Authors. All Rights Reserved.
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
		message = alltypes_pb2.TestAllTypes()
		serializer = pbliteserializer.PbLiteSerializer()
		ser = serializer.serialize(message)

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
			[ # 16
				None, None, None, None, None, None, None, None, None,
				None, None, None, None, None, None, None, None, 0],
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


	def test_serialization(self):
		"""
		This is a port of Closure Library's closure/goog/proto2/pbserializer_test.html
		testSerializationAndDeserialization.
		"""
		message = alltypes_pb2.TestAllTypes()
		
		# Set the fields.
		# Singular.
		message.optional_int32 = 101
		message.optional_int64 = 102
		message.optional_uint32 = 103
		message.optional_uint64 = 104
		message.optional_sint32 = 105
		message.optional_sint64 = 106
		message.optional_fixed32 = 107
		message.optional_fixed64 = 108
		message.optional_sfixed32 = 109
		message.optional_sfixed64 = 110
		message.optional_float = 111.5
		message.optional_double = 112.5
		message.optional_bool = True
		message.optional_string = 'test'
		message.optional_bytes = 'abcd'

		# Note: setting OptionGroup.a is wrong and leads to disaster.
		message.optionalgroup.a = 111

		message.optional_nested_message.b = 112

		message.optional_nested_enum  = alltypes_pb2.TestAllTypes.FOO

		# Repeated.
		message.repeated_int32.append(201)
		message.repeated_int32.append(202)

		# Skip a few repeated fields so we can test how null array values are
		# handled.
		message.repeated_string.append('foo')
		message.repeated_string.append('bar')

		# Serialize.
		serializer = pbliteserializer.PbLiteSerializer()
		pblite = serializer.serialize(message)

		self.assertTrue(isinstance(pblite, list))

		# Assert that everything serialized properly.
		self.assertEqual(101, pblite[1])
		self.assertEqual(102, pblite[2])
		self.assertEqual(103, pblite[3])
		self.assertEqual(104, pblite[4])
		self.assertEqual(105, pblite[5])
		self.assertEqual(106, pblite[6])
		self.assertEqual(107, pblite[7])
		self.assertEqual(108, pblite[8])
		self.assertEqual(109, pblite[9])
		self.assertEqual(110, pblite[10])
		self.assertEqual(111.5, pblite[11])
		self.assertEqual(112.5, pblite[12])
		self.assertEqual(1, pblite[13]) # True is serialized as 1
		self.assertEqual('test', pblite[14])
		self.assertEqual('abcd', pblite[15])

		self.assertEqual(111, pblite[16][17])
		self.assertEqual(112, pblite[18][1])

		self.assertEqual(None, pblite[19])
		self.assertEqual(None, pblite[20])

		self.assertEqual(alltypes_pb2.TestAllTypes.FOO, pblite[21])

		self.assertEqual(201, pblite[31][0])
		self.assertEqual(202, pblite[31][1])
		self.assertEqual('foo', pblite[44][0])
		self.assertEqual('bar', pblite[44][1])

		messageDecoded = alltypes_pb2.TestAllTypes()
		serializer.deserialize(messageDecoded, pblite)
		##print "\n\n", message
		##print "\n\n", messageDecoded
		self.assertEqual(messageDecoded, message)
