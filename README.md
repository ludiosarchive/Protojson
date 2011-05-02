Protojson overview
==================

Protojson contains `pbliteserializer`, a Protocol Buffers 2
encoder/decoder compatible with Closure Library's
`goog.proto2.PbLiteSerializer`.

In the future, this package might contain an encoder/decoder
compatible with Closure Library's `goog.proto2.ObjectSerializer`.

See also `protojson.pbliteserializer`'s docstring.


Requirements
============

*	Python 2.4+ (but tested only on CPython 2.6.5, CPython 2.7,
	pypy 1.3, pypy 1.4).

*	Google's protobuf Python module:
	https://code.google.com/p/protobuf/
	(see python/ in their source tree)


Installation
============
`python setup.py install`

This installs the module `protojson`.


Sample use
==========

**Deserialization:**

```
import simplejson
from protojson.pbliteserializer import PbLiteSerializer
from protojson.error import PbDecodeError

serializer = PbLiteSerializer()

def decode_json_from_client(jsonStr):
	"""Returns a populated protobuf Message"""

	body = simplejson.loads(jsonStr)
	try:
		msg = SomeProtobufMessage()
		serializer.deserialize(msg, body)
		# msg is now populated with fields from body.
	except PbDecodeError:
		log.err()
		raise
	return msg
```

**Serialization:**

```
import simplejson
from protojson.pbliteserializer import PbLiteSerializer
from protojson.error import PbDecodeError

serializer = PbLiteSerializer()

simplejson.dumps(serializer.serialize(
	SomeProtobufMessage(field1=val1, field2=val2)
```


FAQ
===

**Why does this special serialization format exist in the first place?**

Normally, protobuf Messages are encoded (and decoded from)
bytes, but JavaScript environments have an easier time handling
Arrays of objects.  The PbLite format encodes Messages to Arrays
(or `list`s in Python).


**Why is this called "Protojson"? I don't see any JSON.**

You're right, pbliteserializer doesn't do any actual JSON encoding/decoding.
This matches the behavior of the JavaScript version.  You'll need
`simplejson` (or the built-in `json` module) to send and receive
PbLite lists over the wire.

Note: if you want to send protobuf `bytes` to a client where bytes are
not UTF-8, you may need to change the encoding= passed to simplejson.dumps:

```
>>> simplejson.dumps(["\xff"])
[...] UnicodeDecodeError: 'utf8' codec can't decode byte 0xff in position 0: invalid start byte

>>> simplejson.dumps(["\xff"], encoding='latin-1')
'["\\u00ff"]'
```


Likely bugs
===========

Not everything in `pbliteserializer` is tested.  You might discover problems
with:

*	Protocol Buffers Extensions (completely untested).

*	Groups and Messages nested in untested ways.


Code style notes
================

This package mostly follows the Divmod Coding Standard
<http://replay.web.archive.org/http://divmod.org/trac/wiki/CodingStandard> with a few exceptions:

*	Use hard tabs for indentation.

*	Use hard tabs only at the beginning of a line.

*	Prefer to have lines <= 80 characters, but always less than 100.

If you add tests, make sure to update `protojson/run_tests.py`!
