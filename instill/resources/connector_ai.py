# pylint: disable=no-member,wrong-import-position,no-name-in-module,arguments-renamed
from typing import Union

from instill.resources import Component
from instill.resources.schema import (
    archetypeai_task_describe_input,
    archetypeai_task_summarize_input,
    archetypeai_task_upload_file_input,
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


class HuggingfaceConnector(Component):
    """Huggingface Connector"""

    def __init__(
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
    ) -> None:
        definition_name = "connector-definitions/hugging-face"
        component_type = "connector"

        component = helper.construct_component_config(
            component_type, definition_name, inp
        )

        super().__init__(name, component)


class InstillModelConnector(Component):
    """Instill Model Connector"""

    def __init__(
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
    ) -> None:
        definition_name = "connector-definitions/instill-model"
        component_type = "connector"

        component = helper.construct_component_config(
            component_type, definition_name, inp
        )

        super().__init__(name, component)


class StabilityAIConnector(Component):
    """Stability AI Connector"""

    def __init__(
        self,
        name: str,
        inp: Union[
            stabilityai_task_image_to_image_input.Input,
            stabilityai_task_text_to_image_input.Input,
        ],
    ) -> None:
        definition_name = "connector-definitions/stability-ai"
        component_type = "connector"

        component = helper.construct_component_config(
            component_type, definition_name, inp
        )

        super().__init__(name, component)


class OpenAIConnector(Component):
    """OpenAI Connector"""

    def __init__(
        self,
        name: str,
        inp: Union[
            openai_task_speech_recognition_input.Input,
            openai_task_text_embeddings_input.Input,
            openai_task_text_to_image_input.Input,
            openai_task_text_generation_input.Input,
            openai_task_text_to_speech_input.Input,
        ],
    ) -> None:
        definition_name = "connector-definitions/openai"
        component_type = "connector"

        component = helper.construct_component_config(
            component_type, definition_name, inp
        )

        super().__init__(name, component)


class ArchetypeAIConnector(Component):
    """ArchetypeAI Connector"""

    def __init__(
        self,
        name: str,
        inp: Union[
            archetypeai_task_upload_file_input.Input,
            archetypeai_task_describe_input.Input,
            archetypeai_task_summarize_input.Input,
        ],
    ) -> None:
        definition_name = "connector-definitions/archetype-ai"
        component_type = "connector"

        component = helper.construct_component_config(
            component_type, definition_name, inp
        )

        super().__init__(name, component)
