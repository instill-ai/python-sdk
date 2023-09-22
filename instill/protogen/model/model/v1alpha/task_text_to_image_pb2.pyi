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
import typing

if sys.version_info >= (3, 8):
    import typing as typing_extensions
else:
    import typing_extensions

DESCRIPTOR: google.protobuf.descriptor.FileDescriptor

@typing_extensions.final
class TextToImageInput(google.protobuf.message.Message):
    """TextToImageInput represents the input of text to image task"""

    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    PROMPT_FIELD_NUMBER: builtins.int
    STEPS_FIELD_NUMBER: builtins.int
    CFG_SCALE_FIELD_NUMBER: builtins.int
    SEED_FIELD_NUMBER: builtins.int
    SAMPLES_FIELD_NUMBER: builtins.int
    prompt: builtins.str
    """The prompt text"""
    steps: builtins.int
    """The steps, default is 5"""
    cfg_scale: builtins.float
    """The guidance scale, default is 7.5"""
    seed: builtins.int
    """The seed, default is 0"""
    samples: builtins.int
    """The number of generated samples, default is 1"""
    def __init__(
        self,
        *,
        prompt: builtins.str = ...,
        steps: builtins.int | None = ...,
        cfg_scale: builtins.float | None = ...,
        seed: builtins.int | None = ...,
        samples: builtins.int | None = ...,
    ) -> None: ...
    def HasField(self, field_name: typing_extensions.Literal["_cfg_scale", b"_cfg_scale", "_samples", b"_samples", "_seed", b"_seed", "_steps", b"_steps", "cfg_scale", b"cfg_scale", "samples", b"samples", "seed", b"seed", "steps", b"steps"]) -> builtins.bool: ...
    def ClearField(self, field_name: typing_extensions.Literal["_cfg_scale", b"_cfg_scale", "_samples", b"_samples", "_seed", b"_seed", "_steps", b"_steps", "cfg_scale", b"cfg_scale", "prompt", b"prompt", "samples", b"samples", "seed", b"seed", "steps", b"steps"]) -> None: ...
    @typing.overload
    def WhichOneof(self, oneof_group: typing_extensions.Literal["_cfg_scale", b"_cfg_scale"]) -> typing_extensions.Literal["cfg_scale"] | None: ...
    @typing.overload
    def WhichOneof(self, oneof_group: typing_extensions.Literal["_samples", b"_samples"]) -> typing_extensions.Literal["samples"] | None: ...
    @typing.overload
    def WhichOneof(self, oneof_group: typing_extensions.Literal["_seed", b"_seed"]) -> typing_extensions.Literal["seed"] | None: ...
    @typing.overload
    def WhichOneof(self, oneof_group: typing_extensions.Literal["_steps", b"_steps"]) -> typing_extensions.Literal["steps"] | None: ...

global___TextToImageInput = TextToImageInput

@typing_extensions.final
class TextToImageOutput(google.protobuf.message.Message):
    """TextToImageOutput represents the output of text to image task"""

    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    IMAGES_FIELD_NUMBER: builtins.int
    @property
    def images(self) -> google.protobuf.internal.containers.RepeatedScalarFieldContainer[builtins.str]:
        """List of generated images"""
    def __init__(
        self,
        *,
        images: collections.abc.Iterable[builtins.str] | None = ...,
    ) -> None: ...
    def ClearField(self, field_name: typing_extensions.Literal["images", b"images"]) -> None: ...

global___TextToImageOutput = TextToImageOutput
