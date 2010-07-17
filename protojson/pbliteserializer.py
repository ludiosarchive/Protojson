from google.protobuf.descriptor.FieldDescriptor import \
	TYPE_BOOL, TYPE_MESSAGE, TYPE_GROUP, LABEL_REPEATED

from google.protobuf.message import Message


class PbLiteSerializer(object):
	"""
	A port of Closure Library's goog.proto2.PbLiteSerializer, but without
	the laziness.
	"""
	__slots__ = ()

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
		# The google.protobuf.descriptor documentation is not very clear
		# about how `fields` is sorted, so sort it ourselves. 
		sortedFields = [(f.number, f) for f in message.DESCRIPTOR.fields]
		sortedFields.sort()

		serialized = []

		lastFieldNumber = -1
		for fieldNumber, field in sortedFields:
			numEmptiesToAppend = lastFieldNumber + 1 - fieldNumber
			assert numEmptiesToAppend >= 0, numEmptiesToAppend
			if numEmptiesToAppend:
				for _ in xrange(numEmptiesToAppend):
					serialized.push(None)

			value = getattr(message, field.name)
			if field.label == LABEL_REPEATED:
				serializedChild = []
				for child in getattr(message, field.name):
					serializedChild.append(self.getSerializedValue(field, child))
				serialized.append(serializedChild)
			else:
				serialized.append(self.getSerializedValue(field, value))
			lastFieldNumber = fieldNumber

		return serialized
