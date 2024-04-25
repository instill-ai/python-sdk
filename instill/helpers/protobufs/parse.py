from dataclasses import dataclass
from typing import List

from instill.helpers.protobufs.ray_pb2 import (
    ModelMetadataRequest,
    ModelMetadataResponse,
    RayServiceCallRequest,
    RayServiceCallResponse,
    InferTensor,
)

from instill.helpers.const import DataType


@dataclass
class Metadata:
    name: str
    datatype: str
    shape: list


def construct_metadata_response(
    req: ModelMetadataRequest,
    inputs: List[Metadata],
    outputs: List[Metadata],
) -> ModelMetadataResponse:
    resp = ModelMetadataResponse(
        name=req.name,
        versions=req.version,
        framework="python",
        inputs=[],
        outputs=[],
    )

    for i in inputs:
        resp.inputs.append(
            ModelMetadataResponse.TensorMetadata(
                name=i.name,
                datatype=i.datatype,
                shape=i.shape,
            )
        )

    for o in outputs:
        resp.outputs.append(
            ModelMetadataResponse.TensorMetadata(
                name=o.name,
                datatype=o.datatype,
                shape=o.shape,
            )
        )

    return resp


def construct_infer_response(
    req: RayServiceCallRequest,
    outputs: List[Metadata],
    raw_outputs: List[bytes],
) -> RayServiceCallResponse:
    resp = RayServiceCallResponse(
        model_name=req.model_name,
        model_version=req.model_version,
        outputs=[],
        raw_output_contents=[],
    )

    for o in outputs:
        resp.outputs.append(
            InferTensor(
                name=o.name,
                datatype=o.datatype,
                shape=o.shape,
            )
        )

    resp.raw_output_contents.extend(raw_outputs)

    return resp


def construct_text_generation_metadata_response(
    req: ModelMetadataRequest,
) -> ModelMetadataResponse:
    return construct_metadata_response(
        req=req,
        inputs=[
            Metadata(
                name="prompt",
                datatype=str(DataType.TYPE_STRING.name),
                shape=[1],
            ),
            Metadata(
                name="prompt_images",
                datatype=str(DataType.TYPE_STRING.name),
                shape=[1],
            ),
            Metadata(
                name="chat_history",
                datatype=str(DataType.TYPE_STRING.name),
                shape=[1],
            ),
            Metadata(
                name="system_message",
                datatype=str(DataType.TYPE_STRING.name),
                shape=[1],
            ),
            Metadata(
                name="max_new_tokens",
                datatype=str(DataType.TYPE_UINT32.name),
                shape=[1],
            ),
            Metadata(
                name="temperature",
                datatype=str(DataType.TYPE_FP32.name),
                shape=[1],
            ),
            Metadata(
                name="top_k",
                datatype=str(DataType.TYPE_UINT32.name),
                shape=[1],
            ),
            Metadata(
                name="random_seed",
                datatype=str(DataType.TYPE_UINT64.name),
                shape=[1],
            ),
            Metadata(
                name="extra_params",
                datatype=str(DataType.TYPE_STRING.name),
                shape=[1],
            ),
        ],
        outputs=[
            Metadata(
                name="text",
                datatype=str(DataType.TYPE_STRING.name),
                shape=[-1, -1],
            ),
        ],
    )


def construct_text_generation_infer_response(
    req: RayServiceCallRequest,
    shape: list,
    raw_outputs: List[bytes],
):
    return construct_infer_response(
        req=req,
        outputs=[
            Metadata(
                name="text",
                datatype=str(DataType.TYPE_STRING.name),
                shape=shape,
            )
        ],
        raw_outputs=raw_outputs,
    )


def construct_text_generation_chat_metadata_response(
    req: ModelMetadataRequest,
) -> ModelMetadataResponse:
    return construct_metadata_response(
        req=req,
        inputs=[
            Metadata(
                name="prompt",
                datatype=str(DataType.TYPE_STRING.name),
                shape=[1],
            ),
            Metadata(
                name="prompt_images",
                datatype=str(DataType.TYPE_STRING.name),
                shape=[1],
            ),
            Metadata(
                name="chat_history",
                datatype=str(DataType.TYPE_STRING.name),
                shape=[1],
            ),
            Metadata(
                name="system_message",
                datatype=str(DataType.TYPE_STRING.name),
                shape=[1],
            ),
            Metadata(
                name="max_new_tokens",
                datatype=str(DataType.TYPE_UINT32.name),
                shape=[1],
            ),
            Metadata(
                name="temperature",
                datatype=str(DataType.TYPE_FP32.name),
                shape=[1],
            ),
            Metadata(
                name="top_k",
                datatype=str(DataType.TYPE_UINT32.name),
                shape=[1],
            ),
            Metadata(
                name="random_seed",
                datatype=str(DataType.TYPE_UINT64.name),
                shape=[1],
            ),
            Metadata(
                name="extra_params",
                datatype=str(DataType.TYPE_STRING.name),
                shape=[1],
            ),
        ],
        outputs=[
            Metadata(
                name="text",
                datatype=str(DataType.TYPE_STRING.name),
                shape=[-1, -1],
            ),
        ],
    )


def construct_text_generation_chat_infer_response(
    req: RayServiceCallRequest,
    shape: list,
    raw_outputs: List[bytes],
):
    return construct_infer_response(
        req=req,
        outputs=[
            Metadata(
                name="text",
                datatype=str(DataType.TYPE_STRING.name),
                shape=shape,
            )
        ],
        raw_outputs=raw_outputs,
    )


def construct_text_to_image_metadata_response(
    req: ModelMetadataRequest,
):
    return construct_metadata_response(
        req=req,
        inputs=[
            Metadata(
                name="prompt",
                datatype=str(DataType.TYPE_STRING.name),
                shape=[1],
            ),
            Metadata(
                name="negative_prompt",
                datatype=str(DataType.TYPE_STRING.name),
                shape=[1],
            ),
            Metadata(
                name="prompt_image",
                datatype=str(DataType.TYPE_STRING.name),
                shape=[1],
            ),
            Metadata(
                name="samples",
                datatype=str(DataType.TYPE_INT32.name),
                shape=[1],
            ),
            Metadata(
                name="scheduler",
                datatype=str(DataType.TYPE_STRING.name),
                shape=[1],
            ),
            Metadata(
                name="steps",
                datatype=str(DataType.TYPE_INT32.name),
                shape=[1],
            ),
            Metadata(
                name="guidance_scale",
                datatype=str(DataType.TYPE_FP32.name),
                shape=[1],
            ),
            Metadata(
                name="seed",
                datatype=str(DataType.TYPE_INT64.name),
                shape=[1],
            ),
            Metadata(
                name="extra_params",
                datatype=str(DataType.TYPE_STRING.name),
                shape=[1],
            ),
        ],
        outputs=[
            Metadata(
                name="images",
                datatype=str(DataType.TYPE_FP32.name),
                shape=[-1, -1, -1, -1],
            ),
        ],
    )


def construct_text_to_image_infer_response(
    req: RayServiceCallRequest,
    shape: list,
    raw_outputs: List[bytes],
):
    return construct_infer_response(
        req=req,
        outputs=[
            Metadata(
                name="images",
                datatype=str(DataType.TYPE_FP32.name),
                shape=shape,
            )
        ],
        raw_outputs=raw_outputs,
    )


def construct_image_to_image_metadata_response(
    req: ModelMetadataRequest,
):
    return construct_metadata_response(
        req=req,
        inputs=[
            Metadata(
                name="prompt",
                datatype=str(DataType.TYPE_STRING.name),
                shape=[1],
            ),
            Metadata(
                name="negative_prompt",
                datatype=str(DataType.TYPE_STRING.name),
                shape=[1],
            ),
            Metadata(
                name="prompt_image",
                datatype=str(DataType.TYPE_STRING.name),
                shape=[1],
            ),
            Metadata(
                name="samples",
                datatype=str(DataType.TYPE_INT32.name),
                shape=[1],
            ),
            Metadata(
                name="scheduler",
                datatype=str(DataType.TYPE_STRING.name),
                shape=[1],
            ),
            Metadata(
                name="steps",
                datatype=str(DataType.TYPE_INT32.name),
                shape=[1],
            ),
            Metadata(
                name="guidance_scale",
                datatype=str(DataType.TYPE_FP32.name),
                shape=[1],
            ),
            Metadata(
                name="seed",
                datatype=str(DataType.TYPE_INT64.name),
                shape=[1],
            ),
            Metadata(
                name="extra_params",
                datatype=str(DataType.TYPE_STRING.name),
                shape=[1],
            ),
        ],
        outputs=[
            Metadata(
                name="images",
                datatype=str(DataType.TYPE_FP32.name),
                shape=[-1, -1, -1, -1],
            ),
        ],
    )


def construct_image_to_image_infer_response(
    req: RayServiceCallRequest,
    shape: list,
    raw_outputs: List[bytes],
):
    return construct_infer_response(
        req=req,
        outputs=[
            Metadata(
                name="images",
                datatype=str(DataType.TYPE_FP32.name),
                shape=shape,
            )
        ],
        raw_outputs=raw_outputs,
    )


def construct_visual_question_answering_metadata_response(
    req: ModelMetadataRequest,
):
    return construct_metadata_response(
        req=req,
        inputs=[
            Metadata(
                name="prompt",
                datatype=str(DataType.TYPE_STRING.name),
                shape=[1],
            ),
            Metadata(
                name="prompt_images",
                datatype=str(DataType.TYPE_STRING.name),
                shape=[1],
            ),
            Metadata(
                name="chat_history",
                datatype=str(DataType.TYPE_STRING.name),
                shape=[1],
            ),
            Metadata(
                name="system_message",
                datatype=str(DataType.TYPE_STRING.name),
                shape=[1],
            ),
            Metadata(
                name="max_new_tokens",
                datatype=str(DataType.TYPE_UINT32.name),
                shape=[1],
            ),
            Metadata(
                name="temperature",
                datatype=str(DataType.TYPE_FP32.name),
                shape=[1],
            ),
            Metadata(
                name="top_k",
                datatype=str(DataType.TYPE_UINT32.name),
                shape=[1],
            ),
            Metadata(
                name="random_seed",
                datatype=str(DataType.TYPE_UINT64.name),
                shape=[1],
            ),
            Metadata(
                name="extra_params",
                datatype=str(DataType.TYPE_STRING.name),
                shape=[1],
            ),
        ],
        outputs=[
            Metadata(
                name="text",
                datatype=str(DataType.TYPE_STRING.name),
                shape=[-1, -1],
            ),
        ],
    )


def construct_visual_question_answering_infer_response(
    req: RayServiceCallRequest,
    shape: list,
    raw_outputs: List[bytes],
):
    return construct_infer_response(
        req=req,
        outputs=[
            Metadata(
                name="text",
                datatype=str(DataType.TYPE_STRING.name),
                shape=shape,
            )
        ],
        raw_outputs=raw_outputs,
    )
