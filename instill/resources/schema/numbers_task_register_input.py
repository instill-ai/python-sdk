# generated by datamodel-codegen:
#   filename:  numbers_task_register_input.json

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import List, Optional


class DigitalSourceType(Enum):
    trainedAlgorithmicMedia = 'trainedAlgorithmicMedia'
    trainedAlgorithmicData = 'trainedAlgorithmicData'
    digitalCapture = 'digitalCapture'
    digitalArt = 'digitalArt'
    algorithmicMedia = 'algorithmicMedia'


@dataclass
class License:
    document: Optional[str] = None
    name: Optional[str] = None


class MiningPreference(Enum):
    dataMining = 'dataMining'
    aiInference = 'aiInference'
    notAllowed = 'notAllowed'
    aiGenerativeTraining = 'aiGenerativeTraining'
    aiGenerativeTrainingWithAuthorship = 'aiGenerativeTrainingWithAuthorship'
    aiTraining = 'aiTraining'
    aiTrainingWithAuthorship = 'aiTrainingWithAuthorship'


@dataclass
class Input:
    images: List[str]
    headline: Optional[str] = None
    caption: Optional[str] = None
    asset_creator: Optional[str] = None
    digital_source_type: Optional[DigitalSourceType] = (
        DigitalSourceType.trainedAlgorithmicMedia
    )
    generated_by: Optional[str] = None
    license: Optional[License] = None
    mining_preference: Optional[MiningPreference] = MiningPreference.notAllowed
