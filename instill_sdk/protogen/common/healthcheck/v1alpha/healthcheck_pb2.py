# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: common/healthcheck/v1alpha/healthcheck.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from google.api import field_behavior_pb2 as google_dot_api_dot_field__behavior__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n,common/healthcheck/v1alpha/healthcheck.proto\x12\x1a\x63ommon.healthcheck.v1alpha\x1a\x1fgoogle/api/field_behavior.proto\"E\n\x12HealthCheckRequest\x12#\n\x07service\x18\x01 \x01(\tB\x04\xe2\x41\x01\x01H\x00R\x07service\x88\x01\x01\x42\n\n\x08_service\"\xd9\x01\n\x13HealthCheckResponse\x12U\n\x06status\x18\x01 \x01(\x0e\x32=.common.healthcheck.v1alpha.HealthCheckResponse.ServingStatusR\x06status\"k\n\rServingStatus\x12\x1e\n\x1aSERVING_STATUS_UNSPECIFIED\x10\x00\x12\x1a\n\x16SERVING_STATUS_SERVING\x10\x01\x12\x1e\n\x1aSERVING_STATUS_NOT_SERVING\x10\x02\x42\x8d\x02\n\x1e\x63om.common.healthcheck.v1alphaB\x10HealthcheckProtoP\x01ZOgithub.com/instill-ai/protogen-go/common/healthcheck/v1alpha;healthcheckv1alpha\xa2\x02\x03\x43HX\xaa\x02\x1a\x43ommon.Healthcheck.V1alpha\xca\x02\x1a\x43ommon\\Healthcheck\\V1alpha\xe2\x02&Common\\Healthcheck\\V1alpha\\GPBMetadata\xea\x02\x1c\x43ommon::Healthcheck::V1alphab\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'common.healthcheck.v1alpha.healthcheck_pb2', _globals)
if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  DESCRIPTOR._serialized_options = b'\n\036com.common.healthcheck.v1alphaB\020HealthcheckProtoP\001ZOgithub.com/instill-ai/protogen-go/common/healthcheck/v1alpha;healthcheckv1alpha\242\002\003CHX\252\002\032Common.Healthcheck.V1alpha\312\002\032Common\\Healthcheck\\V1alpha\342\002&Common\\Healthcheck\\V1alpha\\GPBMetadata\352\002\034Common::Healthcheck::V1alpha'
  _HEALTHCHECKREQUEST.fields_by_name['service']._options = None
  _HEALTHCHECKREQUEST.fields_by_name['service']._serialized_options = b'\342A\001\001'
  _globals['_HEALTHCHECKREQUEST']._serialized_start=109
  _globals['_HEALTHCHECKREQUEST']._serialized_end=178
  _globals['_HEALTHCHECKRESPONSE']._serialized_start=181
  _globals['_HEALTHCHECKRESPONSE']._serialized_end=398
  _globals['_HEALTHCHECKRESPONSE_SERVINGSTATUS']._serialized_start=291
  _globals['_HEALTHCHECKRESPONSE_SERVINGSTATUS']._serialized_end=398
# @@protoc_insertion_point(module_scope)
