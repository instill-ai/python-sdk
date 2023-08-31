# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: base/mgmt/v1alpha/mgmt.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from common.healthcheck.v1alpha import healthcheck_pb2 as common_dot_healthcheck_dot_v1alpha_dot_healthcheck__pb2
from google.api import field_behavior_pb2 as google_dot_api_dot_field__behavior__pb2
from google.api import resource_pb2 as google_dot_api_dot_resource__pb2
from google.protobuf import field_mask_pb2 as google_dot_protobuf_dot_field__mask__pb2
from google.protobuf import timestamp_pb2 as google_dot_protobuf_dot_timestamp__pb2
from protoc_gen_openapiv2.options import annotations_pb2 as protoc__gen__openapiv2_dot_options_dot_annotations__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x1c\x62\x61se/mgmt/v1alpha/mgmt.proto\x12\x11\x62\x61se.mgmt.v1alpha\x1a,common/healthcheck/v1alpha/healthcheck.proto\x1a\x1fgoogle/api/field_behavior.proto\x1a\x19google/api/resource.proto\x1a google/protobuf/field_mask.proto\x1a\x1fgoogle/protobuf/timestamp.proto\x1a.protoc-gen-openapiv2/options/annotations.proto\"\x97\x01\n\x0fLivenessRequest\x12k\n\x14health_check_request\x18\x01 \x01(\x0b\x32..common.healthcheck.v1alpha.HealthCheckRequestB\x04\xe2\x41\x01\x01H\x00R\x12healthCheckRequest\x88\x01\x01\x42\x17\n\x15_health_check_request\"w\n\x10LivenessResponse\x12\x63\n\x15health_check_response\x18\x01 \x01(\x0b\x32/.common.healthcheck.v1alpha.HealthCheckResponseR\x13healthCheckResponse\"\x98\x01\n\x10ReadinessRequest\x12k\n\x14health_check_request\x18\x01 \x01(\x0b\x32..common.healthcheck.v1alpha.HealthCheckRequestB\x04\xe2\x41\x01\x01H\x00R\x12healthCheckRequest\x88\x01\x01\x42\x17\n\x15_health_check_request\"x\n\x11ReadinessResponse\x12\x63\n\x15health_check_response\x18\x01 \x01(\x0b\x32/.common.healthcheck.v1alpha.HealthCheckResponseR\x13healthCheckResponse\"\xce\x05\n\x04User\x12\x18\n\x04name\x18\x01 \x01(\tB\x04\xe2\x41\x01\x03R\x04name\x12\x1b\n\x03uid\x18\x02 \x01(\tB\x04\xe2\x41\x01\x05H\x00R\x03uid\x88\x01\x01\x12\x14\n\x02id\x18\x03 \x01(\tB\x04\xe2\x41\x01\x02R\x02id\x12\x36\n\x04type\x18\x04 \x01(\x0e\x32\x1c.base.mgmt.v1alpha.OwnerTypeB\x04\xe2\x41\x01\x03R\x04type\x12\x41\n\x0b\x63reate_time\x18\x05 \x01(\x0b\x32\x1a.google.protobuf.TimestampB\x04\xe2\x41\x01\x03R\ncreateTime\x12\x41\n\x0bupdate_time\x18\x06 \x01(\x0b\x32\x1a.google.protobuf.TimestampB\x04\xe2\x41\x01\x03R\nupdateTime\x12\x1a\n\x05\x65mail\x18\x07 \x01(\tB\x04\xe2\x41\x01\x02R\x05\x65mail\x12%\n\x0b\x63ustomer_id\x18\x08 \x01(\tB\x04\xe2\x41\x01\x03R\ncustomerId\x12(\n\nfirst_name\x18\t \x01(\tB\x04\xe2\x41\x01\x01H\x01R\tfirstName\x88\x01\x01\x12&\n\tlast_name\x18\n \x01(\tB\x04\xe2\x41\x01\x01H\x02R\x08lastName\x88\x01\x01\x12$\n\x08org_name\x18\x0b \x01(\tB\x04\xe2\x41\x01\x01H\x03R\x07orgName\x88\x01\x01\x12\x1d\n\x04role\x18\x0c \x01(\tB\x04\xe2\x41\x01\x01H\x04R\x04role\x88\x01\x01\x12=\n\x17newsletter_subscription\x18\r \x01(\x08\x42\x04\xe2\x41\x01\x02R\x16newsletterSubscription\x12,\n\x0c\x63ookie_token\x18\x0e \x01(\tB\x04\xe2\x41\x01\x01H\x05R\x0b\x63ookieToken\x88\x01\x01:(\xea\x41%\n\x15\x61pi.instill.tech/User\x12\x0cusers/{user}B\x06\n\x04_uidB\r\n\x0b_first_nameB\x0c\n\n_last_nameB\x0b\n\t_org_nameB\x07\n\x05_roleB\x0f\n\r_cookie_token\"\xf5\x01\n\x15ListUsersAdminRequest\x12&\n\tpage_size\x18\x01 \x01(\x03\x42\x04\xe2\x41\x01\x01H\x00R\x08pageSize\x88\x01\x01\x12(\n\npage_token\x18\x02 \x01(\tB\x04\xe2\x41\x01\x01H\x01R\tpageToken\x88\x01\x01\x12\x36\n\x04view\x18\x03 \x01(\x0e\x32\x17.base.mgmt.v1alpha.ViewB\x04\xe2\x41\x01\x01H\x02R\x04view\x88\x01\x01\x12!\n\x06\x66ilter\x18\x04 \x01(\tB\x04\xe2\x41\x01\x01H\x03R\x06\x66ilter\x88\x01\x01\x42\x0c\n\n_page_sizeB\r\n\x0b_page_tokenB\x07\n\x05_viewB\t\n\x07_filter\"\x8e\x01\n\x16ListUsersAdminResponse\x12-\n\x05users\x18\x01 \x03(\x0b\x32\x17.base.mgmt.v1alpha.UserR\x05users\x12&\n\x0fnext_page_token\x18\x02 \x01(\tR\rnextPageToken\x12\x1d\n\ntotal_size\x18\x03 \x01(\x03R\ttotalSize\"K\n\x16\x43reateUserAdminRequest\x12\x31\n\x04user\x18\x01 \x01(\x0b\x32\x17.base.mgmt.v1alpha.UserB\x04\xe2\x41\x01\x02R\x04user\"F\n\x17\x43reateUserAdminResponse\x12+\n\x04user\x18\x01 \x01(\x0b\x32\x17.base.mgmt.v1alpha.UserR\x04user\"\x9c\x01\n\x13GetUserAdminRequest\x12\x44\n\x04name\x18\x01 \x01(\tB0\x92\x41\x0f\xca>\x0c\xfa\x02\tuser.name\xe2\x41\x01\x02\xfa\x41\x17\n\x15\x61pi.instill.tech/UserR\x04name\x12\x36\n\x04view\x18\x02 \x01(\x0e\x32\x17.base.mgmt.v1alpha.ViewB\x04\xe2\x41\x01\x01H\x00R\x04view\x88\x01\x01\x42\x07\n\x05_view\"C\n\x14GetUserAdminResponse\x12+\n\x04user\x18\x01 \x01(\x0b\x32\x17.base.mgmt.v1alpha.UserR\x04user\"\x8e\x01\n\x16UpdateUserAdminRequest\x12\x31\n\x04user\x18\x01 \x01(\x0b\x32\x17.base.mgmt.v1alpha.UserB\x04\xe2\x41\x01\x02R\x04user\x12\x41\n\x0bupdate_mask\x18\x02 \x01(\x0b\x32\x1a.google.protobuf.FieldMaskB\x04\xe2\x41\x01\x02R\nupdateMask\"F\n\x17UpdateUserAdminResponse\x12+\n\x04user\x18\x01 \x01(\x0b\x32\x17.base.mgmt.v1alpha.UserR\x04user\"^\n\x16\x44\x65leteUserAdminRequest\x12\x44\n\x04name\x18\x01 \x01(\tB0\x92\x41\x0f\xca>\x0c\xfa\x02\tuser.name\xe2\x41\x01\x02\xfa\x41\x17\n\x15\x61pi.instill.tech/UserR\x04name\"\x19\n\x17\x44\x65leteUserAdminResponse\"}\n\x16LookUpUserAdminRequest\x12\"\n\tpermalink\x18\x01 \x01(\tB\x04\xe2\x41\x01\x02R\tpermalink\x12\x36\n\x04view\x18\x02 \x01(\x0e\x32\x17.base.mgmt.v1alpha.ViewB\x04\xe2\x41\x01\x01H\x00R\x04view\x88\x01\x01\x42\x07\n\x05_view\"F\n\x17LookUpUserAdminResponse\x12+\n\x04user\x18\x01 \x01(\x0b\x32\x17.base.mgmt.v1alpha.UserR\x04user\"\x1f\n\x1dQueryAuthenticatedUserRequest\"M\n\x1eQueryAuthenticatedUserResponse\x12+\n\x04user\x18\x01 \x01(\x0b\x32\x17.base.mgmt.v1alpha.UserR\x04user\"\x95\x01\n\x1dPatchAuthenticatedUserRequest\x12\x31\n\x04user\x18\x01 \x01(\x0b\x32\x17.base.mgmt.v1alpha.UserB\x04\xe2\x41\x01\x02R\x04user\x12\x41\n\x0bupdate_mask\x18\x02 \x01(\x0b\x32\x1a.google.protobuf.FieldMaskB\x04\xe2\x41\x01\x02R\nupdateMask\"M\n\x1ePatchAuthenticatedUserResponse\x12+\n\x04user\x18\x01 \x01(\x0b\x32\x17.base.mgmt.v1alpha.UserR\x04user\"\\\n\x14\x45xistUsernameRequest\x12\x44\n\x04name\x18\x01 \x01(\tB0\x92\x41\x0f\xca>\x0c\xfa\x02\tuser.name\xe2\x41\x01\x02\xfa\x41\x17\n\x15\x61pi.instill.tech/UserR\x04name\"/\n\x15\x45xistUsernameResponse\x12\x16\n\x06\x65xists\x18\x01 \x01(\x08R\x06\x65xists\"\xdb\x04\n\x08\x41piToken\x12\x18\n\x04name\x18\x01 \x01(\tB\x04\xe2\x41\x01\x03R\x04name\x12\x16\n\x03uid\x18\x02 \x01(\tB\x04\xe2\x41\x01\x03R\x03uid\x12\x14\n\x02id\x18\x03 \x01(\tB\x04\xe2\x41\x01\x05R\x02id\x12\x41\n\x0b\x63reate_time\x18\x04 \x01(\x0b\x32\x1a.google.protobuf.TimestampB\x04\xe2\x41\x01\x03R\ncreateTime\x12\x41\n\x0bupdate_time\x18\x05 \x01(\x0b\x32\x1a.google.protobuf.TimestampB\x04\xe2\x41\x01\x03R\nupdateTime\x12\'\n\x0c\x61\x63\x63\x65ss_token\x18\x07 \x01(\tB\x04\xe2\x41\x01\x03R\x0b\x61\x63\x63\x65ssToken\x12=\n\x05state\x18\x08 \x01(\x0e\x32!.base.mgmt.v1alpha.ApiToken.StateB\x04\xe2\x41\x01\x03R\x05state\x12#\n\ntoken_type\x18\t \x01(\tB\x04\xe2\x41\x01\x03R\ttokenType\x12\x18\n\x03ttl\x18\n \x01(\x03\x42\x04\xe2\x41\x01\x04H\x00R\x03ttl\x12=\n\x0b\x65xpire_time\x18\x0b \x01(\x0b\x32\x1a.google.protobuf.TimestampH\x00R\nexpireTime\"W\n\x05State\x12\x15\n\x11STATE_UNSPECIFIED\x10\x00\x12\x12\n\x0eSTATE_INACTIVE\x10\x01\x12\x10\n\x0cSTATE_ACTIVE\x10\x02\x12\x11\n\rSTATE_EXPIRED\x10\x03:.\xea\x41+\n\x19\x61pi.instill.tech/ApiToken\x12\x0etokens/{token}B\x0c\n\nexpirationJ\x04\x08\x06\x10\x07\"M\n\x12\x43reateTokenRequest\x12\x37\n\x05token\x18\x01 \x01(\x0b\x32\x1b.base.mgmt.v1alpha.ApiTokenB\x04\xe2\x41\x01\x02R\x05token\"H\n\x13\x43reateTokenResponse\x12\x31\n\x05token\x18\x01 \x01(\x0b\x32\x1b.base.mgmt.v1alpha.ApiTokenR\x05token\"\x82\x01\n\x11ListTokensRequest\x12&\n\tpage_size\x18\x01 \x01(\x03\x42\x04\xe2\x41\x01\x01H\x00R\x08pageSize\x88\x01\x01\x12(\n\npage_token\x18\x02 \x01(\tB\x04\xe2\x41\x01\x01H\x01R\tpageToken\x88\x01\x01\x42\x0c\n\n_page_sizeB\r\n\x0b_page_token\"\x90\x01\n\x12ListTokensResponse\x12\x33\n\x06tokens\x18\x01 \x03(\x0b\x32\x1b.base.mgmt.v1alpha.ApiTokenR\x06tokens\x12&\n\x0fnext_page_token\x18\x02 \x01(\tR\rnextPageToken\x12\x1d\n\ntotal_size\x18\x03 \x01(\x03R\ttotalSize\"\\\n\x0fGetTokenRequest\x12I\n\x04name\x18\x01 \x01(\tB5\x92\x41\x10\xca>\r\xfa\x02\ntoken.name\xe2\x41\x01\x02\xfa\x41\x1b\n\x19\x61pi.instill.tech/ApiTokenR\x04name\"E\n\x10GetTokenResponse\x12\x31\n\x05token\x18\x01 \x01(\x0b\x32\x1b.base.mgmt.v1alpha.ApiTokenR\x05token\"_\n\x12\x44\x65leteTokenRequest\x12I\n\x04name\x18\x01 \x01(\tB5\x92\x41\x10\xca>\r\xfa\x02\ntoken.name\xe2\x41\x01\x02\xfa\x41\x1b\n\x19\x61pi.instill.tech/ApiTokenR\x04name\"\x15\n\x13\x44\x65leteTokenResponse*;\n\x04View\x12\x14\n\x10VIEW_UNSPECIFIED\x10\x00\x12\x0e\n\nVIEW_BASIC\x10\x01\x12\r\n\tVIEW_FULL\x10\x02*Y\n\tOwnerType\x12\x1a\n\x16OWNER_TYPE_UNSPECIFIED\x10\x00\x12\x13\n\x0fOWNER_TYPE_USER\x10\x01\x12\x1b\n\x17OWNER_TYPE_ORGANIZATION\x10\x02\x42\xc9\x01\n\x15\x63om.base.mgmt.v1alphaB\tMgmtProtoP\x01Z?github.com/instill-ai/protogen-go/base/mgmt/v1alpha;mgmtv1alpha\xa2\x02\x03\x42MX\xaa\x02\x11\x42\x61se.Mgmt.V1alpha\xca\x02\x11\x42\x61se\\Mgmt\\V1alpha\xe2\x02\x1d\x42\x61se\\Mgmt\\V1alpha\\GPBMetadata\xea\x02\x13\x42\x61se::Mgmt::V1alphab\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'base.mgmt.v1alpha.mgmt_pb2', _globals)
if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  DESCRIPTOR._serialized_options = b'\n\025com.base.mgmt.v1alphaB\tMgmtProtoP\001Z?github.com/instill-ai/protogen-go/base/mgmt/v1alpha;mgmtv1alpha\242\002\003BMX\252\002\021Base.Mgmt.V1alpha\312\002\021Base\\Mgmt\\V1alpha\342\002\035Base\\Mgmt\\V1alpha\\GPBMetadata\352\002\023Base::Mgmt::V1alpha'
  _LIVENESSREQUEST.fields_by_name['health_check_request']._options = None
  _LIVENESSREQUEST.fields_by_name['health_check_request']._serialized_options = b'\342A\001\001'
  _READINESSREQUEST.fields_by_name['health_check_request']._options = None
  _READINESSREQUEST.fields_by_name['health_check_request']._serialized_options = b'\342A\001\001'
  _USER.fields_by_name['name']._options = None
  _USER.fields_by_name['name']._serialized_options = b'\342A\001\003'
  _USER.fields_by_name['uid']._options = None
  _USER.fields_by_name['uid']._serialized_options = b'\342A\001\005'
  _USER.fields_by_name['id']._options = None
  _USER.fields_by_name['id']._serialized_options = b'\342A\001\002'
  _USER.fields_by_name['type']._options = None
  _USER.fields_by_name['type']._serialized_options = b'\342A\001\003'
  _USER.fields_by_name['create_time']._options = None
  _USER.fields_by_name['create_time']._serialized_options = b'\342A\001\003'
  _USER.fields_by_name['update_time']._options = None
  _USER.fields_by_name['update_time']._serialized_options = b'\342A\001\003'
  _USER.fields_by_name['email']._options = None
  _USER.fields_by_name['email']._serialized_options = b'\342A\001\002'
  _USER.fields_by_name['customer_id']._options = None
  _USER.fields_by_name['customer_id']._serialized_options = b'\342A\001\003'
  _USER.fields_by_name['first_name']._options = None
  _USER.fields_by_name['first_name']._serialized_options = b'\342A\001\001'
  _USER.fields_by_name['last_name']._options = None
  _USER.fields_by_name['last_name']._serialized_options = b'\342A\001\001'
  _USER.fields_by_name['org_name']._options = None
  _USER.fields_by_name['org_name']._serialized_options = b'\342A\001\001'
  _USER.fields_by_name['role']._options = None
  _USER.fields_by_name['role']._serialized_options = b'\342A\001\001'
  _USER.fields_by_name['newsletter_subscription']._options = None
  _USER.fields_by_name['newsletter_subscription']._serialized_options = b'\342A\001\002'
  _USER.fields_by_name['cookie_token']._options = None
  _USER.fields_by_name['cookie_token']._serialized_options = b'\342A\001\001'
  _USER._options = None
  _USER._serialized_options = b'\352A%\n\025api.instill.tech/User\022\014users/{user}'
  _LISTUSERSADMINREQUEST.fields_by_name['page_size']._options = None
  _LISTUSERSADMINREQUEST.fields_by_name['page_size']._serialized_options = b'\342A\001\001'
  _LISTUSERSADMINREQUEST.fields_by_name['page_token']._options = None
  _LISTUSERSADMINREQUEST.fields_by_name['page_token']._serialized_options = b'\342A\001\001'
  _LISTUSERSADMINREQUEST.fields_by_name['view']._options = None
  _LISTUSERSADMINREQUEST.fields_by_name['view']._serialized_options = b'\342A\001\001'
  _LISTUSERSADMINREQUEST.fields_by_name['filter']._options = None
  _LISTUSERSADMINREQUEST.fields_by_name['filter']._serialized_options = b'\342A\001\001'
  _CREATEUSERADMINREQUEST.fields_by_name['user']._options = None
  _CREATEUSERADMINREQUEST.fields_by_name['user']._serialized_options = b'\342A\001\002'
  _GETUSERADMINREQUEST.fields_by_name['name']._options = None
  _GETUSERADMINREQUEST.fields_by_name['name']._serialized_options = b'\222A\017\312>\014\372\002\tuser.name\342A\001\002\372A\027\n\025api.instill.tech/User'
  _GETUSERADMINREQUEST.fields_by_name['view']._options = None
  _GETUSERADMINREQUEST.fields_by_name['view']._serialized_options = b'\342A\001\001'
  _UPDATEUSERADMINREQUEST.fields_by_name['user']._options = None
  _UPDATEUSERADMINREQUEST.fields_by_name['user']._serialized_options = b'\342A\001\002'
  _UPDATEUSERADMINREQUEST.fields_by_name['update_mask']._options = None
  _UPDATEUSERADMINREQUEST.fields_by_name['update_mask']._serialized_options = b'\342A\001\002'
  _DELETEUSERADMINREQUEST.fields_by_name['name']._options = None
  _DELETEUSERADMINREQUEST.fields_by_name['name']._serialized_options = b'\222A\017\312>\014\372\002\tuser.name\342A\001\002\372A\027\n\025api.instill.tech/User'
  _LOOKUPUSERADMINREQUEST.fields_by_name['permalink']._options = None
  _LOOKUPUSERADMINREQUEST.fields_by_name['permalink']._serialized_options = b'\342A\001\002'
  _LOOKUPUSERADMINREQUEST.fields_by_name['view']._options = None
  _LOOKUPUSERADMINREQUEST.fields_by_name['view']._serialized_options = b'\342A\001\001'
  _PATCHAUTHENTICATEDUSERREQUEST.fields_by_name['user']._options = None
  _PATCHAUTHENTICATEDUSERREQUEST.fields_by_name['user']._serialized_options = b'\342A\001\002'
  _PATCHAUTHENTICATEDUSERREQUEST.fields_by_name['update_mask']._options = None
  _PATCHAUTHENTICATEDUSERREQUEST.fields_by_name['update_mask']._serialized_options = b'\342A\001\002'
  _EXISTUSERNAMEREQUEST.fields_by_name['name']._options = None
  _EXISTUSERNAMEREQUEST.fields_by_name['name']._serialized_options = b'\222A\017\312>\014\372\002\tuser.name\342A\001\002\372A\027\n\025api.instill.tech/User'
  _APITOKEN.fields_by_name['name']._options = None
  _APITOKEN.fields_by_name['name']._serialized_options = b'\342A\001\003'
  _APITOKEN.fields_by_name['uid']._options = None
  _APITOKEN.fields_by_name['uid']._serialized_options = b'\342A\001\003'
  _APITOKEN.fields_by_name['id']._options = None
  _APITOKEN.fields_by_name['id']._serialized_options = b'\342A\001\005'
  _APITOKEN.fields_by_name['create_time']._options = None
  _APITOKEN.fields_by_name['create_time']._serialized_options = b'\342A\001\003'
  _APITOKEN.fields_by_name['update_time']._options = None
  _APITOKEN.fields_by_name['update_time']._serialized_options = b'\342A\001\003'
  _APITOKEN.fields_by_name['access_token']._options = None
  _APITOKEN.fields_by_name['access_token']._serialized_options = b'\342A\001\003'
  _APITOKEN.fields_by_name['state']._options = None
  _APITOKEN.fields_by_name['state']._serialized_options = b'\342A\001\003'
  _APITOKEN.fields_by_name['token_type']._options = None
  _APITOKEN.fields_by_name['token_type']._serialized_options = b'\342A\001\003'
  _APITOKEN.fields_by_name['ttl']._options = None
  _APITOKEN.fields_by_name['ttl']._serialized_options = b'\342A\001\004'
  _APITOKEN._options = None
  _APITOKEN._serialized_options = b'\352A+\n\031api.instill.tech/ApiToken\022\016tokens/{token}'
  _CREATETOKENREQUEST.fields_by_name['token']._options = None
  _CREATETOKENREQUEST.fields_by_name['token']._serialized_options = b'\342A\001\002'
  _LISTTOKENSREQUEST.fields_by_name['page_size']._options = None
  _LISTTOKENSREQUEST.fields_by_name['page_size']._serialized_options = b'\342A\001\001'
  _LISTTOKENSREQUEST.fields_by_name['page_token']._options = None
  _LISTTOKENSREQUEST.fields_by_name['page_token']._serialized_options = b'\342A\001\001'
  _GETTOKENREQUEST.fields_by_name['name']._options = None
  _GETTOKENREQUEST.fields_by_name['name']._serialized_options = b'\222A\020\312>\r\372\002\ntoken.name\342A\001\002\372A\033\n\031api.instill.tech/ApiToken'
  _DELETETOKENREQUEST.fields_by_name['name']._options = None
  _DELETETOKENREQUEST.fields_by_name['name']._serialized_options = b'\222A\020\312>\r\372\002\ntoken.name\342A\001\002\372A\033\n\031api.instill.tech/ApiToken'
  _globals['_VIEW']._serialized_start=4664
  _globals['_VIEW']._serialized_end=4723
  _globals['_OWNERTYPE']._serialized_start=4725
  _globals['_OWNERTYPE']._serialized_end=4814
  _globals['_LIVENESSREQUEST']._serialized_start=273
  _globals['_LIVENESSREQUEST']._serialized_end=424
  _globals['_LIVENESSRESPONSE']._serialized_start=426
  _globals['_LIVENESSRESPONSE']._serialized_end=545
  _globals['_READINESSREQUEST']._serialized_start=548
  _globals['_READINESSREQUEST']._serialized_end=700
  _globals['_READINESSRESPONSE']._serialized_start=702
  _globals['_READINESSRESPONSE']._serialized_end=822
  _globals['_USER']._serialized_start=825
  _globals['_USER']._serialized_end=1543
  _globals['_LISTUSERSADMINREQUEST']._serialized_start=1546
  _globals['_LISTUSERSADMINREQUEST']._serialized_end=1791
  _globals['_LISTUSERSADMINRESPONSE']._serialized_start=1794
  _globals['_LISTUSERSADMINRESPONSE']._serialized_end=1936
  _globals['_CREATEUSERADMINREQUEST']._serialized_start=1938
  _globals['_CREATEUSERADMINREQUEST']._serialized_end=2013
  _globals['_CREATEUSERADMINRESPONSE']._serialized_start=2015
  _globals['_CREATEUSERADMINRESPONSE']._serialized_end=2085
  _globals['_GETUSERADMINREQUEST']._serialized_start=2088
  _globals['_GETUSERADMINREQUEST']._serialized_end=2244
  _globals['_GETUSERADMINRESPONSE']._serialized_start=2246
  _globals['_GETUSERADMINRESPONSE']._serialized_end=2313
  _globals['_UPDATEUSERADMINREQUEST']._serialized_start=2316
  _globals['_UPDATEUSERADMINREQUEST']._serialized_end=2458
  _globals['_UPDATEUSERADMINRESPONSE']._serialized_start=2460
  _globals['_UPDATEUSERADMINRESPONSE']._serialized_end=2530
  _globals['_DELETEUSERADMINREQUEST']._serialized_start=2532
  _globals['_DELETEUSERADMINREQUEST']._serialized_end=2626
  _globals['_DELETEUSERADMINRESPONSE']._serialized_start=2628
  _globals['_DELETEUSERADMINRESPONSE']._serialized_end=2653
  _globals['_LOOKUPUSERADMINREQUEST']._serialized_start=2655
  _globals['_LOOKUPUSERADMINREQUEST']._serialized_end=2780
  _globals['_LOOKUPUSERADMINRESPONSE']._serialized_start=2782
  _globals['_LOOKUPUSERADMINRESPONSE']._serialized_end=2852
  _globals['_QUERYAUTHENTICATEDUSERREQUEST']._serialized_start=2854
  _globals['_QUERYAUTHENTICATEDUSERREQUEST']._serialized_end=2885
  _globals['_QUERYAUTHENTICATEDUSERRESPONSE']._serialized_start=2887
  _globals['_QUERYAUTHENTICATEDUSERRESPONSE']._serialized_end=2964
  _globals['_PATCHAUTHENTICATEDUSERREQUEST']._serialized_start=2967
  _globals['_PATCHAUTHENTICATEDUSERREQUEST']._serialized_end=3116
  _globals['_PATCHAUTHENTICATEDUSERRESPONSE']._serialized_start=3118
  _globals['_PATCHAUTHENTICATEDUSERRESPONSE']._serialized_end=3195
  _globals['_EXISTUSERNAMEREQUEST']._serialized_start=3197
  _globals['_EXISTUSERNAMEREQUEST']._serialized_end=3289
  _globals['_EXISTUSERNAMERESPONSE']._serialized_start=3291
  _globals['_EXISTUSERNAMERESPONSE']._serialized_end=3338
  _globals['_APITOKEN']._serialized_start=3341
  _globals['_APITOKEN']._serialized_end=3944
  _globals['_APITOKEN_STATE']._serialized_start=3789
  _globals['_APITOKEN_STATE']._serialized_end=3876
  _globals['_CREATETOKENREQUEST']._serialized_start=3946
  _globals['_CREATETOKENREQUEST']._serialized_end=4023
  _globals['_CREATETOKENRESPONSE']._serialized_start=4025
  _globals['_CREATETOKENRESPONSE']._serialized_end=4097
  _globals['_LISTTOKENSREQUEST']._serialized_start=4100
  _globals['_LISTTOKENSREQUEST']._serialized_end=4230
  _globals['_LISTTOKENSRESPONSE']._serialized_start=4233
  _globals['_LISTTOKENSRESPONSE']._serialized_end=4377
  _globals['_GETTOKENREQUEST']._serialized_start=4379
  _globals['_GETTOKENREQUEST']._serialized_end=4471
  _globals['_GETTOKENRESPONSE']._serialized_start=4473
  _globals['_GETTOKENRESPONSE']._serialized_end=4542
  _globals['_DELETETOKENREQUEST']._serialized_start=4544
  _globals['_DELETETOKENREQUEST']._serialized_end=4639
  _globals['_DELETETOKENRESPONSE']._serialized_start=4641
  _globals['_DELETETOKENRESPONSE']._serialized_end=4662
# @@protoc_insertion_point(module_scope)
