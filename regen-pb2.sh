#!/bin/sh -e

# This script uses `protoc` from the open-source protobuf to
# regenerate the protojson/alltypes_pb2.py file.

protoc -I=protojson --python_out=protojson protojson/alltypes.proto
