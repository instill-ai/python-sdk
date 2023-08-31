"""
@generated by mypy-protobuf.  Do not edit manually!
isort:skip_file
"""
import builtins
import collections.abc
import google.protobuf.descriptor
import google.protobuf.internal.containers
import google.protobuf.message
import sys

if sys.version_info >= (3, 8):
    import typing as typing_extensions
else:
    import typing_extensions

DESCRIPTOR: google.protobuf.descriptor.FileDescriptor

@typing_extensions.final
class ClassificationInput(google.protobuf.message.Message):
    """ClassificationInput represents the input of classification task"""

    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    IMAGE_URL_FIELD_NUMBER: builtins.int
    IMAGE_BASE64_FIELD_NUMBER: builtins.int
    image_url: builtins.str
    """Image type URL"""
    image_base64: builtins.str
    """Image type base64"""
    def __init__(
        self,
        *,
        image_url: builtins.str = ...,
        image_base64: builtins.str = ...,
    ) -> None: ...
    def HasField(self, field_name: typing_extensions.Literal["image_base64", b"image_base64", "image_url", b"image_url", "type", b"type"]) -> builtins.bool: ...
    def ClearField(self, field_name: typing_extensions.Literal["image_base64", b"image_base64", "image_url", b"image_url", "type", b"type"]) -> None: ...
    def WhichOneof(self, oneof_group: typing_extensions.Literal["type", b"type"]) -> typing_extensions.Literal["image_url", "image_base64"] | None: ...

global___ClassificationInput = ClassificationInput

@typing_extensions.final
class ClassificationInputStream(google.protobuf.message.Message):
    """ClassificationInputStream represents the input of classification task when
    using stream method
    """

    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    FILE_LENGTHS_FIELD_NUMBER: builtins.int
    CONTENT_FIELD_NUMBER: builtins.int
    @property
    def file_lengths(self) -> google.protobuf.internal.containers.RepeatedScalarFieldContainer[builtins.int]:
        """The list of file length for each uploaded binary file"""
    content: builtins.bytes
    """Content of images in bytes"""
    def __init__(
        self,
        *,
        file_lengths: collections.abc.Iterable[builtins.int] | None = ...,
        content: builtins.bytes = ...,
    ) -> None: ...
    def ClearField(self, field_name: typing_extensions.Literal["content", b"content", "file_lengths", b"file_lengths"]) -> None: ...

global___ClassificationInputStream = ClassificationInputStream

@typing_extensions.final
class ClassificationOutput(google.protobuf.message.Message):
    """ClassificationOutput represents the output of classification task"""

    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    CATEGORY_FIELD_NUMBER: builtins.int
    SCORE_FIELD_NUMBER: builtins.int
    category: builtins.str
    """Classification category"""
    score: builtins.float
    """Classification score"""
    def __init__(
        self,
        *,
        category: builtins.str = ...,
        score: builtins.float = ...,
    ) -> None: ...
    def ClearField(self, field_name: typing_extensions.Literal["category", b"category", "score", b"score"]) -> None: ...

global___ClassificationOutput = ClassificationOutput
