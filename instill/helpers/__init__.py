# pylint: disable=no-name-in-module
from instill.helpers.protobufs.ray_pb2 import CallRequest, CallResponse
from instill.helpers.ray_io import (
    construct_task_chat_output,
    construct_task_classification_output,
    construct_task_detection_output,
    construct_task_instance_segmentation_output,
    construct_task_keypoint_output,
    construct_task_ocr_output,
    construct_task_semantic_segmentation_output,
    parse_task_chat_to_chat_input,
    parse_task_chat_to_multimodal_chat_input,
    parse_task_classification_to_vision_input,
    parse_task_detection_to_vision_input,
    parse_task_instance_segmentation_to_vision_input,
    parse_task_keypoint_to_vision_input,
    parse_task_ocr_to_vision_input,
    parse_task_semantic_segmentation_to_vision_input,
)
