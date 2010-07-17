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


"""
Protocol Buffer 2 Serializer which serializes messages into PB-Lite
("JsPbLite") format.

PB-Lite format is an array where each index corresponds to the associated tag
number. For example, a message like so:

	message Foo {
		optional int bar = 1;
		optional int baz = 2;
		optional int bop = 4;
	}

would be represented as such:

	[None, (bar data), (baz data), (nothing), (bop data)]

Note that since the array index is used to represent the tag number, sparsely
populated messages with tag numbers that are not continuous (and/or are very
large) will have many (empty) spots and thus, are inefficient.
"""


from google.protobuf.descriptor.FieldDescriptor import \
	TYPE_BOOL, TYPE_MESSAGE, TYPE_GROUP, LABEL_REPEATED

from google.protobuf.message import Message


class PbLiteSerializer(object):
	"""
	A port of Closure Library's goog.proto2.PbLiteSerializer, but without
	the laziness.
	"""
	__slots__ = ('fillerValue',)

	def __init__(self, fillerValue=None):
		"""
		C{fillerValue} is the object to use for unpopulated indices.  The
		default is C{None}.
		"""
		self.fillerValue = fillerValue


	def getSerializedValue(self, field, value):
		if field.type == TYPE_BOOL:
			# Booleans are serialized in numeric form.
			return value and 1 or 0

		elif field.type in (TYPE_MESSAGE, TYPE_GROUP):
			assert isinstance(value, Message)
			return self.serialize(value)

		else:
			return value


	def serialize(message):
		"""
		C{message} is a L{google.protobuf.message.Message}.

		Returns a C{list}, the serialized form of C{message}.
		"""
		maxFieldNumber = max([f.number for f in message.DESCRIPTOR.fields])
		serialized = [self.fillerValue] * maxFieldNumber

		for tag, field in message.DESCRIPTOR.fields_by_number:
			value = getattr(message, field.name)
			if field.label == LABEL_REPEATED:
				serializedChild = []
				for child in getattr(message, field.name):
					serializedChild.append(self.getSerializedValue(field, child))
				serialized[tag] = serializedChild
			else:
				serialized[tag] = self.getSerializedValue(field, value)

		return serialized
