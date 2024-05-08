# pylint: disable=no-member,wrong-import-position
from dataclasses import dataclass
from typing import List

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

        req = {}
        for req_f in request_fields:
            req[req_f.key] = pipeline_pb.TriggerByRequest.RequestField(
                title=req_f.title,
                description=req_f.description,
                instill_format=req_f.format,
            )
        resp = {}
        for resp_f in response_fields:
            resp[resp_f.key] = pipeline_pb.TriggerByRequest.ResponseField(
                title=resp_f.title,
                description=resp_f.description,
                value=resp_f.value,
            )

        t = pipeline_pb.Trigger(
            trigger_by_request=pipeline_pb.TriggerByRequest(
                request_fields=req,
                response_fields=resp,
            )
        )

        self.t = t

    def get_trigger(self) -> pipeline_pb.Trigger:
        return self.t
