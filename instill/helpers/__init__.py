# pylint: disable=no-name-in-module
from instill.helpers.ray_config import InstillDeployable, instill_deployment
from instill.helpers.ray_io import (
    construct_custom_output,
    construct_task_chat_output,
    construct_task_classification_output,
    construct_task_completion_output,
    construct_task_detection_output,
    construct_task_embedding_output,
    construct_task_instance_segmentation_output,
    construct_task_keypoint_output,
    construct_task_ocr_output,
    construct_task_semantic_segmentation_output,
    construct_task_text_to_image_output,
    parse_custom_input,
    parse_task_chat_to_chat_input,
    parse_task_chat_to_multimodal_chat_input,
    parse_task_classification_to_vision_input,
    parse_task_completion_to_completion_input,
    parse_task_detection_to_vision_input,
    parse_task_embedding_to_image_embedding_input,
    parse_task_embedding_to_multimodal_embedding_input,
    parse_task_embedding_to_text_embedding_input,
    parse_task_instance_segmentation_to_vision_input,
    parse_task_keypoint_to_vision_input,
    parse_task_ocr_to_vision_input,
    parse_task_semantic_segmentation_to_vision_input,
    parse_task_text_to_image_input,
)
