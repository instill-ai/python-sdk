from dataclasses import dataclass
from typing import List

from instill.helpers.protobufs.ray_pb2 import (
    ModelMetadataRequest,
    ModelMetadataResponse,
    RayServiceCallRequest,
    RayServiceCallResponse,
    InferTensor,
)


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
