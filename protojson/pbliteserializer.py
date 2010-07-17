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


from google.protobuf.descriptor import FieldDescriptor
from google.protobuf.message import Message

TYPE_BOOL = FieldDescriptor.TYPE_BOOL
TYPE_MESSAGE = FieldDescriptor.TYPE_MESSAGE
TYPE_GROUP = FieldDescriptor.TYPE_GROUP
LABEL_REPEATED = FieldDescriptor.LABEL_REPEATED


def _isRepeated(field):
	return field.label == LABEL_REPEATED


def _isMessageOrGroup(field):
	return field.type in (TYPE_MESSAGE, TYPE_GROUP)


class PbDecodeError(Exception):
	pass


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
		"""
		Returns the serialized form of the given value for the given field
		if the field is a Message or Group and returns the value unchanged
		otherwise (except serialize BOOLs as ints).
		"""
		if field.type == TYPE_BOOL:
			# Booleans are serialized in numeric form.
			return value and 1 or 0

		elif _isMessageOrGroup(field):
			assert isinstance(value, Message)
			return self.serialize(value)

		else:
			return value


	def serialize(self, message):
		"""
		C{message} is a L{google.protobuf.message.Message}.

		Returns a C{list}, the serialized form of C{message}.
		"""
		maxFieldNumber = max([f.number for f in message.DESCRIPTOR.fields])
		serialized = [self.fillerValue] * (maxFieldNumber + 1)

		for tag, field in message.DESCRIPTOR.fields_by_number.iteritems():
			value = getattr(message, field.name)
			if _isRepeated(field):
				serializedChild = []
				for child in getattr(message, field.name):
					serializedChild.append(self.getSerializedValue(field, child))
				serialized[tag] = serializedChild
			else:
				serialized[tag] = self.getSerializedValue(field, value)

		return serialized


	def _getIterator(self, obj):
		try:
			return obj.__iter__()
		except (TypeError, AttributeError):
			raise PbDecodeError("Expected a list but found a %r" % (type(obj),))


	def _deserializeMessageField(self, message, field, subdata):
		if _isRepeated(field):
			if not _isMessageOrGroup(field):
				if field.type != TYPE_BOOL:
					getattr(message, field.name).extend(subdata)
				else:
					getattr(message, field.name).extend([v == 1 for v in subdata])
			else:
				iterator = self._getIterator(subdata)
				for subsubdata in iterator:
					submessage = getattr(message, field.name).add()
					self._deserializeMessage(submessage, subsubdata)
		else:
			if not _isMessageOrGroup(field):
				if field.type != TYPE_BOOL:
					##print repr(message), str(message), repr(subdata)
					setattr(message, field.name, subdata)
				else:
					setattr(message, field.name, subdata == 1)
			else:
				# See "Singular Fields",
				# https://code.google.com/apis/protocolbuffers/docs/reference/python-generated.html#fields
				submessage = getattr(message, field.name)
				self._deserializeMessage(submessage, subdata)


	def _deserializeMessage(self, message, data):
		for tag, field in message.DESCRIPTOR.fields_by_number.iteritems():
			subdata = data[tag]
			##print "tag, field, subdata", repr(tag), repr(field), repr(subdata)
			self._deserializeMessageField(message, field, subdata)


	def deserialize(self, message, data):
		"""
		C{message} is a L{google.protobuf.message.Message}.  It will be
			mutated, not returned.  Existing values will be cleared.
		C{data} is a L{list}.  Unneeded values are ignored.
		"""
		message.Clear()
		self._deserializeMessage(message, data)
