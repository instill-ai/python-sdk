# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: user_defined.proto
# Protobuf Python Version: 4.25.1
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from google.protobuf import struct_pb2 as google_dot_protobuf_dot_struct__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x12user_defined.proto\x12\x11model.ray.v1alpha\x1a\x1cgoogle/protobuf/struct.proto\";\n\x0b\x43\x61llRequest\x12,\n\x0btask_inputs\x18\x01 \x03(\x0b\x32\x17.google.protobuf.Struct\"=\n\x0c\x43\x61llResponse\x12-\n\x0ctask_outputs\x18\x01 \x03(\x0b\x32\x17.google.protobuf.Struct2d\n\x15RayUserDefinedService\x12K\n\x08__call__\x12\x1e.model.ray.v1alpha.CallRequest\x1a\x1f.model.ray.v1alpha.CallResponseb\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'user_defined_pb2', _globals)
if _descriptor._USE_C_DESCRIPTORS == False:
  DESCRIPTOR._options = None
  _globals['_CALLREQUEST']._serialized_start=71
  _globals['_CALLREQUEST']._serialized_end=130
  _globals['_CALLRESPONSE']._serialized_start=132
  _globals['_CALLRESPONSE']._serialized_end=193
  _globals['_RAYUSERDEFINEDSERVICE']._serialized_start=195
  _globals['_RAYUSERDEFINEDSERVICE']._serialized_end=295
# @@protoc_insertion_point(module_scope)
