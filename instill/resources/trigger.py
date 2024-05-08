# pylint: disable=no-member,wrong-import-position
from typing import List
from dataclasses import dataclass

import instill.protogen.vdp.pipeline.v1beta.pipeline_pb2 as pipeline_pb


@dataclass
class TriggerByRequestRequestFields:
    key: str
    title: str
    description: str
    format: str


@dataclass
class TriggerByRequestResponseFields:
    key: str
    title: str
    description: str
    value: str


class Trigger:
    def __init__(
        self,
        request_fields: List[TriggerByRequestRequestFields],
        response_fields: List[TriggerByRequestResponseFields],
    ) -> None:
        t = pipeline_pb.TriggerByRequest
        req = {}
        for f in request_fields:
            req[f.key] = pipeline_pb.TriggerByRequest.RequestField(
                title=f.title,
                description=f.description,
                instill_format=f.format,
            )
        resp = {}
        for f in response_fields:
            resp[f.key] = pipeline_pb.TriggerByRequest.ResponseField(
                title=f.title,
                description=f.description,
                value=f.value,
            )
        t.request_fields = req
        t.response_fields = resp

        self.t = t

    def get_trigger(self) -> pipeline_pb.Trigger:
        return self.t
