# generated by datamodel-codegen:
#   filename:  pinecone_definitions.json
#   timestamp: 2024-01-04T21:52:04+00:00

from __future__ import annotations

from dataclasses import dataclass


@dataclass
class PineconeConnectorSpec:
    api_key: str
    url: str
