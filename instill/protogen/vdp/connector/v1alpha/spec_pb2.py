# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: vdp/connector/v1alpha/spec.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from google.api import field_behavior_pb2 as google_dot_api_dot_field__behavior__pb2
from google.protobuf import struct_pb2 as google_dot_protobuf_dot_struct__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n vdp/connector/v1alpha/spec.proto\x12\x15vdp.connector.v1alpha\x1a\x1fgoogle/api/field_behavior.proto\x1a\x1cgoogle/protobuf/struct.proto\"\x8a\x02\n\x04Spec\x12T\n\x16resource_specification\x18\x02 \x01(\x0b\x32\x17.google.protobuf.StructB\x04\xe2\x41\x01\x02R\x15resourceSpecification\x12V\n\x17\x63omponent_specification\x18\x03 \x01(\x0b\x32\x17.google.protobuf.StructB\x04\xe2\x41\x01\x02R\x16\x63omponentSpecification\x12T\n\x16openapi_specifications\x18\x04 \x01(\x0b\x32\x17.google.protobuf.StructB\x04\xe2\x41\x01\x02R\x15openapiSpecificationsB\xe6\x01\n\x19\x63om.vdp.connector.v1alphaB\tSpecProtoP\x01ZHgithub.com/instill-ai/protogen-go/vdp/connector/v1alpha;connectorv1alpha\xa2\x02\x03VCX\xaa\x02\x15Vdp.Connector.V1alpha\xca\x02\x15Vdp\\Connector\\V1alpha\xe2\x02!Vdp\\Connector\\V1alpha\\GPBMetadata\xea\x02\x17Vdp::Connector::V1alphab\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'vdp.connector.v1alpha.spec_pb2', _globals)
if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  DESCRIPTOR._serialized_options = b'\n\031com.vdp.connector.v1alphaB\tSpecProtoP\001ZHgithub.com/instill-ai/protogen-go/vdp/connector/v1alpha;connectorv1alpha\242\002\003VCX\252\002\025Vdp.Connector.V1alpha\312\002\025Vdp\\Connector\\V1alpha\342\002!Vdp\\Connector\\V1alpha\\GPBMetadata\352\002\027Vdp::Connector::V1alpha'
  _SPEC.fields_by_name['resource_specification']._options = None
  _SPEC.fields_by_name['resource_specification']._serialized_options = b'\342A\001\002'
  _SPEC.fields_by_name['component_specification']._options = None
  _SPEC.fields_by_name['component_specification']._serialized_options = b'\342A\001\002'
  _SPEC.fields_by_name['openapi_specifications']._options = None
  _SPEC.fields_by_name['openapi_specifications']._serialized_options = b'\342A\001\002'
  _globals['_SPEC']._serialized_start=123
  _globals['_SPEC']._serialized_end=389
# @@protoc_insertion_point(module_scope)
