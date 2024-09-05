from google.protobuf import struct_pb2 as _struct_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class CallRequest(_message.Message):
    __slots__ = ("task_inputs",)
    TASK_INPUTS_FIELD_NUMBER: _ClassVar[int]
    task_inputs: _containers.RepeatedCompositeFieldContainer[_struct_pb2.Struct]
    def __init__(self, task_inputs: _Optional[_Iterable[_Union[_struct_pb2.Struct, _Mapping]]] = ...) -> None: ...

class CallResponse(_message.Message):
    __slots__ = ("task_outputs",)
    TASK_OUTPUTS_FIELD_NUMBER: _ClassVar[int]
    task_outputs: _containers.RepeatedCompositeFieldContainer[_struct_pb2.Struct]
    def __init__(self, task_outputs: _Optional[_Iterable[_Union[_struct_pb2.Struct, _Mapping]]] = ...) -> None: ...
