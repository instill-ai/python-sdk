# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: vdp/controller/v1alpha/controller_service.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from google.api import annotations_pb2 as google_dot_api_dot_annotations__pb2
from google.api import client_pb2 as google_dot_api_dot_client__pb2
from vdp.controller.v1alpha import controller_pb2 as vdp_dot_controller_dot_v1alpha_dot_controller__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n/vdp/controller/v1alpha/controller_service.proto\x12\x16vdp.controller.v1alpha\x1a\x1cgoogle/api/annotations.proto\x1a\x17google/api/client.proto\x1a\'vdp/controller/v1alpha/controller.proto2\xf0\x06\n\x18\x43ontrollerPrivateService\x12\x98\x01\n\x08Liveness\x12\'.vdp.controller.v1alpha.LivenessRequest\x1a(.vdp.controller.v1alpha.LivenessResponse\"9\x82\xd3\xe4\x93\x02\x33\x12\x13/v1alpha/__livenessZ\x1c\x12\x1a/v1alpha/health/controller\x12~\n\tReadiness\x12(.vdp.controller.v1alpha.ReadinessRequest\x1a).vdp.controller.v1alpha.ReadinessResponse\"\x1c\x82\xd3\xe4\x93\x02\x16\x12\x14/v1alpha/__readiness\x12\xb6\x01\n\x0bGetResource\x12*.vdp.controller.v1alpha.GetResourceRequest\x1a+.vdp.controller.v1alpha.GetResourceResponse\"N\xda\x41\x12resource_permalink\x82\xd3\xe4\x93\x02\x33\x12\x31/v1alpha/{resource_permalink=resources/*/types/*}\x12\xbd\x01\n\x0eUpdateResource\x12-.vdp.controller.v1alpha.UpdateResourceRequest\x1a..vdp.controller.v1alpha.UpdateResourceResponse\"L\x82\xd3\xe4\x93\x02\x46\x32:/v1alpha/{resource.resource_permalink=resources/*/types/*}:\x08resource\x12\xbf\x01\n\x0e\x44\x65leteResource\x12-.vdp.controller.v1alpha.DeleteResourceRequest\x1a..vdp.controller.v1alpha.DeleteResourceResponse\"N\xda\x41\x12resource_permalink\x82\xd3\xe4\x93\x02\x33*1/v1alpha/{resource_permalink=resources/*/types/*}B\xfa\x01\n\x1a\x63om.vdp.controller.v1alphaB\x16\x43ontrollerServiceProtoP\x01ZJgithub.com/instill-ai/protogen-go/vdp/controller/v1alpha;controllerv1alpha\xa2\x02\x03VCX\xaa\x02\x16Vdp.Controller.V1alpha\xca\x02\x16Vdp\\Controller\\V1alpha\xe2\x02\"Vdp\\Controller\\V1alpha\\GPBMetadata\xea\x02\x18Vdp::Controller::V1alphab\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'vdp.controller.v1alpha.controller_service_pb2', _globals)
if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  DESCRIPTOR._serialized_options = b'\n\032com.vdp.controller.v1alphaB\026ControllerServiceProtoP\001ZJgithub.com/instill-ai/protogen-go/vdp/controller/v1alpha;controllerv1alpha\242\002\003VCX\252\002\026Vdp.Controller.V1alpha\312\002\026Vdp\\Controller\\V1alpha\342\002\"Vdp\\Controller\\V1alpha\\GPBMetadata\352\002\030Vdp::Controller::V1alpha'
  _CONTROLLERPRIVATESERVICE.methods_by_name['Liveness']._options = None
  _CONTROLLERPRIVATESERVICE.methods_by_name['Liveness']._serialized_options = b'\202\323\344\223\0023\022\023/v1alpha/__livenessZ\034\022\032/v1alpha/health/controller'
  _CONTROLLERPRIVATESERVICE.methods_by_name['Readiness']._options = None
  _CONTROLLERPRIVATESERVICE.methods_by_name['Readiness']._serialized_options = b'\202\323\344\223\002\026\022\024/v1alpha/__readiness'
  _CONTROLLERPRIVATESERVICE.methods_by_name['GetResource']._options = None
  _CONTROLLERPRIVATESERVICE.methods_by_name['GetResource']._serialized_options = b'\332A\022resource_permalink\202\323\344\223\0023\0221/v1alpha/{resource_permalink=resources/*/types/*}'
  _CONTROLLERPRIVATESERVICE.methods_by_name['UpdateResource']._options = None
  _CONTROLLERPRIVATESERVICE.methods_by_name['UpdateResource']._serialized_options = b'\202\323\344\223\002F2:/v1alpha/{resource.resource_permalink=resources/*/types/*}:\010resource'
  _CONTROLLERPRIVATESERVICE.methods_by_name['DeleteResource']._options = None
  _CONTROLLERPRIVATESERVICE.methods_by_name['DeleteResource']._serialized_options = b'\332A\022resource_permalink\202\323\344\223\0023*1/v1alpha/{resource_permalink=resources/*/types/*}'
  _globals['_CONTROLLERPRIVATESERVICE']._serialized_start=172
  _globals['_CONTROLLERPRIVATESERVICE']._serialized_end=1052
# @@protoc_insertion_point(module_scope)
