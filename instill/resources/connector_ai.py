# pylint: disable=no-member,wrong-import-position,no-name-in-module,arguments-renamed
import json
from typing import Union

import jsonschema

from instill.clients import InstillClient
from instill.protogen.vdp.pipeline.v1beta.pipeline_pb2 import Component
from instill.resources import const
from instill.resources.connector import Connector
from instill.resources.schema import (
    helper,
    huggingface_task_audio_classification_input,
    huggingface_task_conversational_input,
    huggingface_task_fill_mask_input,
    huggingface_task_image_classification_input,
    huggingface_task_image_segmentation_input,
    huggingface_task_image_to_text_input,
    huggingface_task_object_detection_input,
    huggingface_task_question_answering_input,
    huggingface_task_sentence_similarity_input,
    huggingface_task_speech_recognition_input,
    huggingface_task_summarization_input,
    huggingface_task_table_question_answering_input,
    huggingface_task_text_classification_input,
    huggingface_task_text_generation_input,
    huggingface_task_text_to_image_input,
    huggingface_task_token_classification_input,
    huggingface_task_translation_input,
    huggingface_task_zero_shot_classification_input,
    instill_task_classification_input,
    instill_task_detection_input,
    instill_task_image_to_image_input,
    instill_task_instance_segmentation_input,
    instill_task_keypoint_input,
    instill_task_ocr_input,
    instill_task_semantic_segmentation_input,
    instill_task_text_generation_input,
    instill_task_text_to_image_input,
    instill_task_visual_question_answering_input,
    openai_task_speech_recognition_input,
    openai_task_text_embeddings_input,
    openai_task_text_generation_input,
    openai_task_text_to_image_input,
    openai_task_text_to_speech_input,
    stabilityai_task_image_to_image_input,
    stabilityai_task_text_to_image_input,
)
from instill.resources.schema.huggingface import HuggingFaceConnectorSpec
from instill.resources.schema.instill import (
    InstillModelConnector as InstillModelConnectorConfig,
)
from instill.resources.schema.openai import OpenAIConnectorResource
from instill.resources.schema.stabilityai import StabilityAIConnectorResource


class HuggingfaceConnector(Connector):
    """Huggingface Connector"""

    with open(
        f"{const.SPEC_PATH}/huggingface_definitions.json", "r", encoding="utf8"
    ) as f:
        definitions_jsonschema = json.loads(f.read())

    def __init__(
        self,
        client: InstillClient,
        name: str,
        config: HuggingFaceConnectorSpec,
    ) -> None:
        definition = "connector-definitions/hugging-face"

        config_dict = helper.pop_default_and_to_dict(config)
        jsonschema.validate(config_dict, StabilityAIConnector.definitions_jsonschema)
        super().__init__(client, name, definition, config_dict)

    def create_component(
        self,
        name: str,
        inp: Union[
            huggingface_task_audio_classification_input.Input,
            huggingface_task_conversational_input.Input,
            huggingface_task_fill_mask_input.Input,
            huggingface_task_image_classification_input.Input,
            huggingface_task_image_segmentation_input.Input,
            huggingface_task_object_detection_input.Input,
            huggingface_task_image_to_text_input.Input,
            huggingface_task_question_answering_input.Input,
            huggingface_task_sentence_similarity_input.Input,
            huggingface_task_speech_recognition_input.Input,
            huggingface_task_summarization_input.Input,
            huggingface_task_table_question_answering_input.Input,
            huggingface_task_text_generation_input.Input,
            huggingface_task_text_classification_input.Input,
            huggingface_task_text_to_image_input.Input,
            huggingface_task_translation_input.Input,
            huggingface_task_zero_shot_classification_input.Input,
            huggingface_task_token_classification_input.Input,
        ],
    ) -> Component:
        config = helper.construct_component_config(inp)
        return super()._create_component(name, config)


class InstillModelConnector(Connector):
    """Instill Model Connector"""

    with open(f"{const.SPEC_PATH}/instill_definitions.json", "r", encoding="utf8") as f:
        definitions_jsonschema = json.loads(f.read())

    def __init__(
        self,
        client: InstillClient,
        config: InstillModelConnectorConfig,
        name: str = "model-connector",
    ) -> None:
        definition = "connector-definitions/instill-model"

        config_dict = helper.pop_default_and_to_dict(config)
        jsonschema.validate(config_dict, InstillModelConnector.definitions_jsonschema)
        super().__init__(client, name, definition, config_dict)

    def create_component(
        self,
        name: str,
        inp: Union[
            instill_task_classification_input.Input,
            instill_task_detection_input.Input,
            instill_task_instance_segmentation_input.Input,
            instill_task_semantic_segmentation_input.Input,
            instill_task_keypoint_input.Input,
            instill_task_ocr_input.Input,
            instill_task_image_to_image_input.Input,
            instill_task_text_generation_input.Input,
            instill_task_text_to_image_input.Input,
            instill_task_visual_question_answering_input.Input,
        ],
    ) -> Component:
        config = helper.construct_component_config(inp)
        return super()._create_component(name, config)


class StabilityAIConnector(Connector):
    """Stability AI Connector"""

    with open(
        f"{const.SPEC_PATH}/stabilityai_definitions.json", "r", encoding="utf8"
    ) as f:
        definitions_jsonschema = json.loads(f.read())

    def __init__(
        self,
        client: InstillClient,
        name: str,
        config: StabilityAIConnectorResource,
    ) -> None:
        definition = "connector-definitions/stability-ai"

        config_dict = helper.pop_default_and_to_dict(config)
        jsonschema.validate(config_dict, StabilityAIConnector.definitions_jsonschema)
        super().__init__(client, name, definition, config_dict)

    def create_component(
        self,
        name: str,
        inp: Union[
            stabilityai_task_image_to_image_input.Input,
            stabilityai_task_text_to_image_input.Input,
        ],
    ) -> Component:
        config = helper.construct_component_config(inp)
        return super()._create_component(name, config)


class OpenAIConnector(Connector):
    """OpenAI Connector"""

    with open(f"{const.SPEC_PATH}/openai_definitions.json", "r", encoding="utf8") as f:
        definitions_jsonschema = json.loads(f.read())

    def __init__(
        self,
        client: InstillClient,
        name: str,
        config: OpenAIConnectorResource,
    ) -> None:
        definition = "connector-definitions/openai"

        config_dict = helper.pop_default_and_to_dict(config)
        jsonschema.validate(config_dict, OpenAIConnector.definitions_jsonschema)
        super().__init__(client, name, definition, config_dict)

    def create_component(
        self,
        name: str,
        inp: Union[
            openai_task_speech_recognition_input.Input,
            openai_task_text_embeddings_input.Input,
            openai_task_text_to_image_input.Input,
            openai_task_text_generation_input.Input,
            openai_task_text_to_speech_input.Input,
        ],
    ) -> Component:
        config = helper.construct_component_config(inp)
        return super()._create_component(name, config)
