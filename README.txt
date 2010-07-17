Description
========

Protojson contains pbliteserializer, a Protocol Buffers 2
encoder/decoder compatible with Closure Library's
goog.proto2.PbLiteSerializer.

In the future, this package might contain an encoder/decoder
compatible with Closure Library's goog.proto2.ObjectSerializer.

See also protojson.pbliteserializer's docstring.


Requirements
==========

-	Python 2.4+ (tested only with 2.7, though).

-	Google's protobuf Python module:
	https://code.google.com/p/protobuf/
	(see python/ in their source tree)



Q&A
===

Why does this special serialization format exist in the first place?

Normally, protobuf Messages are encoded (and decoded from)
bytes, but JavaScript environments have an easier time handling
Arrays of objects.  The PbLite format encodes Messages to Arrays
(or `list`s in Python).


Why is this called "Protojson"? I don't see any JSON.

You're right, pbliteserializer doesn't do any actual JSON encoding/decoding.
This matches the behavior of the JavaScript version.  You'll need
`simplejson` (or the built-in `json` module) to send and receive
PbLite Arrays over the wire.

Note: if you want to send protobuf `bytes` to a client where bytes are
not UTF-8, you may need to change the encoding= passed to simplejson.dumps:

>>> simplejson.dumps(["\xff"])
[...] UnicodeDecodeError: 'utf8' codec can't decode byte 0xff in position 0: invalid start byte

>>> simplejson.dumps(["\xff"], encoding='latin-1')
'["\\u00ff"]'



Likely bugs
========

Not everything in pbliteserializer is tested.  You may discover problems with:

-	Protocol Buffers Extensions (completely untested).

-	Groups and Messages nested in untested ways.



Code style notes
============

This package mostly follows the Divmod Coding Standard:
	http://divmod.org/trac/wiki/CodingStandard
except:
-	Use hard tabs for indentation.
-	Use hard tabs only at the beginning of a line.
-	Prefer to have lines <= 80 characters, but always less than 100.
-	In docstrings, use epytext, but don't use @param, @type, etc.
	Few people know how to maintain those annotations.

If you add tests, make sure to update run_tests.py!
