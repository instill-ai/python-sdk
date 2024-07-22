# pylint: disable=no-member,no-name-in-module, inconsistent-return-statements, unused-import
import base64
import io
import re
from typing import Any, Dict, List, Union

import requests
from google.protobuf import json_format, struct_pb2
from PIL import Image

import instill.protogen.model.model.v1alpha.common_pb2 as commonpb
import instill.protogen.model.model.v1alpha.model_pb2 as modelpb
import instill.protogen.model.model.v1alpha.task_classification_pb2 as classificationpb
import instill.protogen.model.model.v1alpha.task_detection_pb2 as detectionpb
import instill.protogen.model.model.v1alpha.task_image_to_image_pb2 as imagetoimagepb
import instill.protogen.model.model.v1alpha.task_instance_segmentation_pb2 as instancesegmentationpb
import instill.protogen.model.model.v1alpha.task_keypoint_pb2 as keypointpb
import instill.protogen.model.model.v1alpha.task_ocr_pb2 as ocrpb
import instill.protogen.model.model.v1alpha.task_semantic_segmentation_pb2 as semanticsegmentationpb
import instill.protogen.model.model.v1alpha.task_text_generation_chat_pb2 as textgenerationchatpb
import instill.protogen.model.model.v1alpha.task_text_generation_pb2 as textgenerationpb
import instill.protogen.model.model.v1alpha.task_text_to_image_pb2 as texttoimagepb
import instill.protogen.model.model.v1alpha.task_visual_question_answering_pb2 as visualquestionansweringpb
from instill.helpers.const import (
    PROMPT_ROLES,
    ConversationInput,
    ConversationMultiModelInput,
    ImageToImageInput,
    TextToImageInput,
    VisionInput,
)
from instill.helpers.errors import InvalidInputException, InvalidOutputShapeException
from instill.helpers.protobufs.ray_pb2 import TriggerRequest, TriggerResponse


def base64_to_pil_image(base64_str):
    return Image.open(
        io.BytesIO(
            base64.b64decode(
                re.sub(
                    "^data:image/.+;base64,",
                    "",
                    base64_str,
                )
            )
        )
    )


def url_to_pil_image(url):
    resp = requests.get(url, timeout=10)
    resp.raise_for_status()
    return Image.open(io.BytesIO(resp.content))


def snake_to_lower_camel(name):
    """Convert snake_case to lowerCamelCase."""
    components = name.split("_")
    return components[0] + "".join(x.title() for x in components[1:])


def protobuf_to_struct(pb_msg):
    """Convert Protobuf message to Struct"""
    dict_data = json_format.MessageToDict(pb_msg)

    lower_camel_dict: Dict[str, Dict[str, Any]] = {}
    # task layer
    for k, v in dict_data.items():
        lower_camel_dict[k[0].lower() + k[1:]] = {}
        # field layer
        for kk, vv in v.items():
            lower_camel_dict[k[0].lower() + k[1:]][snake_to_lower_camel(kk)] = vv

    # Convert dictionary to struct_pb2.Struct
    struct_pb = struct_pb2.Struct()
    json_format.ParseDict(lower_camel_dict, struct_pb)

    return struct_pb


def struct_to_protobuf(struct_pb, pb_message_type):
    """Convert Struct to Protobuf message"""
    dict_data = json_format.MessageToDict(struct_pb)

    lower_camel_dict: Dict[str, Dict[str, Any]] = {}
    # task layer
    for k, v in dict_data.items():
        lower_camel_dict[k[0].lower() + k[1:]] = {}
        # field layer
        for kk, vv in v.items():
            lower_camel_dict[k[0].lower() + k[1:]][snake_to_lower_camel(kk)] = vv

    # Parse dictionary to Protobuf message
    pb_msg = pb_message_type()
    json_format.ParseDict(lower_camel_dict, pb_msg)

    return pb_msg


def struct_to_dict(struct_obj):
    """Convert Protobuf Struct to dictionary"""
    if isinstance(struct_obj, struct_pb2.Struct):
        return {k: struct_to_dict(v) for k, v in struct_obj.fields.items()}
    if isinstance(struct_obj, struct_pb2.ListValue):
        return [struct_to_dict(v) for v in struct_obj.values]
    if isinstance(struct_obj, struct_pb2.Value):
        kind = struct_obj.WhichOneof("kind")
        if kind == "null_value":
            return None
        if kind == "number_value":
            return struct_obj.number_value
        if kind == "string_value":
            return struct_obj.string_value
        if kind == "bool_value":
            return struct_obj.bool_value
        if kind == "struct_value":
            return struct_to_dict(struct_obj.struct_value)
        if kind == "list_value":
            return struct_to_dict(struct_obj.list_value)
    else:
        return struct_obj


def parse_task_classification_to_vision_input(
    request: TriggerRequest,
) -> List[VisionInput]:
    input_list = []
    for task_input in request.task_inputs:
        task_input_pb = struct_to_protobuf(task_input, modelpb.TaskInput)

        classification_pb: classificationpb.ClassificationInput = (
            task_input_pb.classification
        )

        inp = VisionInput()
        if (
            classification_pb.image_base64 != "" and classification_pb.image_url != ""
        ) or (
            classification_pb.image_base64 == "" and classification_pb.image_url == ""
        ):
            raise InvalidInputException
        if classification_pb.image_base64 != "":
            inp.image = base64_to_pil_image(classification_pb.image_base64)
        elif classification_pb.image_url != "":
            inp.image = url_to_pil_image(classification_pb.image_url)

        input_list.append(inp)

    return input_list


def construct_task_classification_output(
    categories: List[str],
    scores: List[float],
) -> TriggerResponse:
    if not len(categories) == len(scores):
        raise InvalidOutputShapeException

    task_outputs = []
    for category, score in zip(categories, scores):

        task_outputs.append(
            protobuf_to_struct(
                modelpb.TaskOutput(
                    classification=classificationpb.ClassificationOutput(
                        category=category, score=score
                    )
                )
            )
        )

    return TriggerResponse(task_outputs=task_outputs)


def parse_task_detection_to_vision_input(
    request: TriggerRequest,
) -> List[VisionInput]:
    input_list = []
    for task_input in request.task_inputs:
        task_input_pb = struct_to_protobuf(task_input, modelpb.TaskInput)

        detection_pb: detectionpb.DetectionInput = task_input_pb.detection

        inp = VisionInput()
        if (detection_pb.image_base64 != "" and detection_pb.image_url != "") or (
            detection_pb.image_base64 == "" and detection_pb.image_url == ""
        ):
            raise InvalidInputException
        if detection_pb.image_base64 != "":
            inp.image = base64_to_pil_image(detection_pb.image_base64)
        elif detection_pb.image_url != "":
            inp.image = url_to_pil_image(detection_pb.image_url)

        input_list.append(inp)

    return input_list


def construct_task_detection_output(
    categories: List[List[str]],
    scores: List[List[float]],
    bounding_boxes: List[List[tuple]],
) -> TriggerResponse:
    """Construct trigger output for detection task

    Args:
        categories (List[List[str]]): for each image input, the list of detected object's category
        scores (List[List[float]]): for each image input, the list of detected object's score
        bounding_boxes (List[List[tuple]]): for each image input, the list of detected object's bbox, with the format
        (top, left, width, height)
    """
    if not len(categories) == len(scores) == len(bounding_boxes):
        raise InvalidOutputShapeException

    task_outputs = []
    for category, score, bbox in zip(categories, scores, bounding_boxes):
        objects = []
        for cat, sc, bb in zip(category, score, bbox):
            objects.append(
                detectionpb.DetectionObject(
                    category=cat,
                    score=sc,
                    bounding_box=commonpb.BoundingBox(
                        top=bb[0],
                        left=bb[1],
                        width=bb[2],
                        height=bb[3],
                    ),
                )
            )
        task_outputs.append(
            protobuf_to_struct(
                modelpb.TaskOutput(
                    detection=detectionpb.DetectionOutput(objects=objects)
                )
            )
        )

    return TriggerResponse(task_outputs=task_outputs)


def parse_task_ocr_to_vision_input(
    request: TriggerRequest,
) -> List[VisionInput]:
    input_list = []
    for task_input in request.task_inputs:
        task_input_pb = struct_to_protobuf(task_input, modelpb.TaskInput)

        ocr_pb: ocrpb.OcrInput = task_input_pb.ocr

        inp = VisionInput()
        if (ocr_pb.image_base64 != "" and ocr_pb.image_url != "") or (
            ocr_pb.image_base64 == "" and ocr_pb.image_url == ""
        ):
            raise InvalidInputException
        if ocr_pb.image_base64 != "":
            inp.image = base64_to_pil_image(ocr_pb.image_base64)
        elif ocr_pb.image_url != "":
            inp.image = url_to_pil_image(ocr_pb.image_url)

        input_list.append(inp)

    return input_list


def construct_task_ocr_output(
    texts: List[List[str]],
    scores: List[List[float]],
    bounding_boxes: List[List[tuple]],
) -> TriggerResponse:
    """Construct trigger output for ocr task

    Args:
        texts (List[List[str]]): for each image input, the list of detected text
        scores (List[List[float]]): for each image input, the list of detected text's score
        bounding_boxes (List[List[tuple]]): for each image input, the list of detected text's bbox, with the format
        (top, left, width, height)
    """
    if not len(texts) == len(scores) == len(bounding_boxes):
        raise InvalidOutputShapeException

    task_outputs = []
    for text, score, bbox in zip(texts, scores, bounding_boxes):
        objects = []
        for txt, sc, bb in zip(text, score, bbox):
            objects.append(
                ocrpb.OcrObject(
                    text=txt,
                    score=sc,
                    bounding_box=commonpb.BoundingBox(
                        top=bb[0],
                        left=bb[1],
                        width=bb[2],
                        height=bb[3],
                    ),
                )
            )
        task_outputs.append(
            protobuf_to_struct(modelpb.TaskOutput(ocr=ocrpb.OcrOutput(objects=objects)))
        )

    return TriggerResponse(task_outputs=task_outputs)


def parse_task_instance_segmentation_to_vision_input(
    request: TriggerRequest,
) -> List[VisionInput]:
    input_list = []
    for task_input in request.task_inputs:
        task_input_pb = struct_to_protobuf(task_input, modelpb.TaskInput)

        instance_segmentation_pb: instancesegmentationpb.InstanceSegmentationInput = (
            task_input_pb.instance_segmentation
        )

        inp = VisionInput()
        if (
            instance_segmentation_pb.image_base64 != ""
            and instance_segmentation_pb.image_url != ""
        ) or (
            instance_segmentation_pb.image_base64 == ""
            and instance_segmentation_pb.image_url == ""
        ):
            raise InvalidInputException
        if instance_segmentation_pb.image_base64 != "":
            inp.image = base64_to_pil_image(
                instance_segmentation_pb.image_base64,
            )
        elif instance_segmentation_pb.image_url != "":
            inp.image = url_to_pil_image(instance_segmentation_pb.image_url)

        input_list.append(inp)

    return input_list


def construct_task_instance_segmentation_output(
    rles: List[List[str]],
    categories: List[List[str]],
    scores: List[List[float]],
    bounding_boxes: List[List[tuple]],
) -> TriggerResponse:
    """Construct trigger output for instance segmentation task

    Args:
        rles (List[List[str]]): for each image input, the list of detected object's rle
        categories (List[List[str]]): for each image input, the list of detected object's category
        scores (List[List[float]]): for each image input, the list of detected text's score
        bounding_boxes (List[List[tuple]]): for each image input, the list of detected text's bbox, with the format
        (top, left, width, height)
    """
    if not len(rles) == len(categories) == len(scores) == len(bounding_boxes):
        raise InvalidOutputShapeException

    task_outputs = []
    for rle, category, score, bbox in zip(rles, categories, scores, bounding_boxes):
        objects = []
        for r, cat, sc, bb in zip(rle, category, score, bbox):
            objects.append(
                instancesegmentationpb.InstanceSegmentationObject(
                    rle=r,
                    category=cat,
                    score=sc,
                    bounding_box=commonpb.BoundingBox(
                        top=bb[0],
                        left=bb[1],
                        width=bb[2],
                        height=bb[3],
                    ),
                )
            )
        task_outputs.append(
            protobuf_to_struct(
                modelpb.TaskOutput(
                    instance_segmentation=instancesegmentationpb.InstanceSegmentationOutput(
                        objects=objects
                    )
                )
            )
        )

    return TriggerResponse(task_outputs=task_outputs)


def parse_task_semantic_segmentation_to_vision_input(
    request: TriggerRequest,
) -> List[VisionInput]:
    input_list = []
    for task_input in request.task_inputs:
        task_input_pb = struct_to_protobuf(task_input, modelpb.TaskInput)

        semantic_segmentation_pb: semanticsegmentationpb.SemanticSegmentationInput = (
            task_input_pb.semantic_segmentation
        )

        inp = VisionInput()
        if (
            semantic_segmentation_pb.image_base64 != ""
            and semantic_segmentation_pb.image_url != ""
        ) or (
            semantic_segmentation_pb.image_base64 == ""
            and semantic_segmentation_pb.image_url == ""
        ):
            raise InvalidInputException
        if semantic_segmentation_pb.image_base64 != "":
            inp.image = base64_to_pil_image(
                semantic_segmentation_pb.image_base64,
            )
        elif semantic_segmentation_pb.image_url != "":
            inp.image = url_to_pil_image(semantic_segmentation_pb.image_url)

        input_list.append(inp)

    return input_list


def construct_task_semantic_segmentation_output(
    rles: List[List[str]],
    categories: List[List[str]],
) -> TriggerResponse:
    """Construct trigger output for semantic segmentation task

    Args:
        rles (List[List[str]]): for each image input, the list of detected object's rle
        categories (List[List[str]]): for each image input, the list of detected object's category
        (top, left, width, height)
    """
    if not len(rles) == len(categories):
        raise InvalidOutputShapeException

    task_outputs = []
    for rle, category in zip(rles, categories):
        objects = []
        for r, cat in zip(rle, category):
            objects.append(
                semanticsegmentationpb.SemanticSegmentationStuff(
                    rle=r,
                    category=cat,
                )
            )
        task_outputs.append(
            protobuf_to_struct(
                modelpb.TaskOutput(
                    instance_segmentation=semanticsegmentationpb.SemanticSegmentationOutput(
                        stuffs=objects
                    )
                )
            )
        )

    return TriggerResponse(task_outputs=task_outputs)


def parse_task_keypoint_to_vision_input(
    request: TriggerRequest,
) -> List[VisionInput]:
    input_list = []
    for task_input in request.task_inputs:
        task_input_pb = struct_to_protobuf(task_input, modelpb.TaskInput)

        keypoint_pb: keypointpb.KeypointInput = task_input_pb.keypoint

        inp = VisionInput()
        if (keypoint_pb.image_base64 != "" and keypoint_pb.image_url != "") or (
            keypoint_pb.image_base64 == "" and keypoint_pb.image_url == ""
        ):
            raise InvalidInputException
        if keypoint_pb.image_base64 != "":
            inp.image = base64_to_pil_image(keypoint_pb.image_base64)
        elif keypoint_pb.image_url != "":
            inp.image = url_to_pil_image(keypoint_pb.image_url)

        input_list.append(inp)

    return input_list


def construct_task_keypoint_output(
    keypoints: List[List[List[tuple]]],
    scores: List[List[float]],
    bounding_boxes: List[List[tuple]],
) -> TriggerResponse:
    """Construct trigger output for keypoint task

    Args:
        keypoints (List[List[List[str]]]): for each image input, the list of detected object's keypoints,
        with the format (x_coordinate, y_coordinate, visibility)
        scores (List[List[float]]): for each image input, the list of detected object's score
        bounding_boxes (List[List[tuple]]): for each image input, the list of detected object's bbox, with the format
        (top, left, width, height)
    """
    if not len(keypoints) == len(scores) == len(bounding_boxes):
        raise InvalidOutputShapeException

    task_outputs = []
    for keypoint, score, bbox in zip(keypoints, scores, bounding_boxes):
        objects = []
        for kps, sc, bb in zip(keypoint, score, bbox):
            point_list = []
            for kp in kps:
                point_list.append(
                    keypointpb.Keypoint(
                        x=kp[0],
                        y=kp[1],
                        v=kp[2],
                    )
                )
            objects.append(
                keypointpb.KeypointObject(
                    keypoints=point_list,
                    score=sc,
                    bounding_box=commonpb.BoundingBox(
                        top=bb[0],
                        left=bb[1],
                        width=bb[2],
                        height=bb[3],
                    ),
                )
            )
        task_outputs.append(
            protobuf_to_struct(
                modelpb.TaskOutput(keypoint=keypointpb.KeypointOutput(objects=objects))
            )
        )

    return TriggerResponse(task_outputs=task_outputs)


def parse_task_text_generation_to_conversation_input(
    request: TriggerRequest,
) -> List[ConversationInput]:

    input_list = []

    for task_input in request.task_inputs:
        task_input_pb = struct_to_protobuf(task_input, modelpb.TaskInput)

        text_generation_pb: textgenerationpb.TextGenerationInput = (
            task_input_pb.text_generation
        )

        inp = ConversationInput()

        conversation: List[Dict[str, str]] = []

        # system message
        if (
            text_generation_pb.system_message is not None
            and len(text_generation_pb.system_message) > 0
        ):
            conversation.append(
                {"role": "system", "content": text_generation_pb.system_message}
            )

        # conversation history
        if (
            text_generation_pb.chat_history is not None
            and len(text_generation_pb.chat_history) > 0
        ):
            for chat_entity in text_generation_pb.chat_history:
                chat_message = None
                if len(chat_entity["content"]) > 1:
                    raise ValueError(
                        "Multiple text message detected"
                        " in a single chat history entity"
                    )

                if chat_entity["content"][0]["type"] == "text":
                    if "Content" in chat_entity["content"][0]:
                        chat_message = chat_entity["content"][0]["Content"]["Text"]
                    elif "Text" in chat_entity["content"][0]:
                        chat_message = chat_entity["content"][0]["Text"]
                    elif "text" in chat_entity["content"][0]:
                        chat_message = chat_entity["content"][0]["text"]
                    else:
                        raise ValueError(
                            f"Unknown structure of chat_history: {text_generation_pb.chat_history}"
                        )
                else:
                    raise ValueError(
                        "Unsupported chat_hisotry message type"
                        ", expected 'text'"
                        f" but get {chat_entity['content'][0]['type']}"
                    )

                if chat_entity["role"] not in PROMPT_ROLES:
                    raise ValueError(
                        f"Role `{chat_entity['role']}` is not in supported"
                        f"role list ({','.join(PROMPT_ROLES)})"
                    )
                if (
                    chat_entity["role"] == PROMPT_ROLES[-1]
                    and text_generation_pb.system_message is not None
                    and len(text_generation_pb.system_message) > 0
                ):
                    continue
                if chat_message is None:
                    raise ValueError(
                        f"No message found in chat_history. {chat_message}"
                    )

                if len(conversation) == 1 and chat_entity["role"] != PROMPT_ROLES[0]:
                    conversation.append({"role": "user", "content": " "})

                if (
                    len(conversation) > 0
                    and conversation[-1]["role"] == chat_entity["role"]
                ):
                    last_conversation = conversation.pop()
                    chat_message = f"{last_conversation['content']}\n\n{chat_message}"

                conversation.append(
                    {"role": chat_entity["role"], "content": chat_message}
                )

        # conversation
        prompt = text_generation_pb.prompt
        if len(conversation) > 0 and conversation[-1]["role"] == PROMPT_ROLES[0]:
            last_conversation = conversation.pop()
            prompt = f"{last_conversation['content']}\n\n{prompt}"

        conversation.append({"role": "user", "content": prompt})

        inp.conversation = conversation

        # max new tokens
        if text_generation_pb.max_new_tokens is not None:
            inp.max_new_tokens = text_generation_pb.max_new_tokens

        # temperature
        if text_generation_pb.temperature is not None:
            inp.temperature = text_generation_pb.temperature

        # top k
        if text_generation_pb.top_k is not None:
            inp.top_k = text_generation_pb.top_k

        # seed
        if text_generation_pb.seed is not None:
            inp.seed = text_generation_pb.seed

        input_list.append(inp)

    return input_list


def construct_task_text_generation_output(texts: List[str]) -> TriggerResponse:
    task_outputs = []

    for text in texts:
        task_outputs.append(
            protobuf_to_struct(
                modelpb.TaskOutput(
                    text_generation=textgenerationpb.TextGenerationOutput(text=text)
                )
            )
        )

    return TriggerResponse(task_outputs=task_outputs)


def parse_task_text_generation_chat_to_conversation_input(
    request: TriggerRequest,
) -> List[ConversationInput]:

    input_list = []

    for task_input in request.task_inputs:
        task_input_pb = struct_to_protobuf(task_input, modelpb.TaskInput)

        text_generation_chat_pb: textgenerationchatpb.TextGenerationChatInput = (
            task_input_pb.text_generation_chat
        )

        inp = ConversationInput()

        conversation = []

        # system message
        if (
            text_generation_chat_pb.system_message is not None
            and len(text_generation_chat_pb.system_message) > 0
        ):
            conversation.append(
                {
                    "role": "system",
                    "content": text_generation_chat_pb.system_message,
                }
            )

        # conversation history
        if (
            text_generation_chat_pb.chat_history is not None
            and len(text_generation_chat_pb.chat_history) > 0
        ):
            for chat_entity in text_generation_chat_pb.chat_history:
                chat_message = None
                if len(chat_entity["content"]) > 1:
                    raise ValueError(
                        "Multiple text message detected"
                        " in a single chat history entity"
                    )

                if chat_entity["content"][0]["type"] == "text":
                    if "Content" in chat_entity["content"][0]:
                        chat_message = chat_entity["content"][0]["Content"]["Text"]
                    elif "Text" in chat_entity["content"][0]:
                        chat_message = chat_entity["content"][0]["Text"]
                    elif "text" in chat_entity["content"][0]:
                        chat_message = chat_entity["content"][0]["text"]
                    else:
                        raise ValueError(
                            f"Unknown structure of chat_history: {text_generation_chat_pb.chat_history}"
                        )
                else:
                    raise ValueError(
                        "Unsupported chat_hisotry message type"
                        ", expected 'text'"
                        f" but get {chat_entity['content'][0]['type']}"
                    )

                if chat_entity["role"] not in PROMPT_ROLES:
                    raise ValueError(
                        f"Role `{chat_entity['role']}` is not in supported"
                        f"role list ({','.join(PROMPT_ROLES)})"
                    )
                if (
                    chat_entity["role"] == PROMPT_ROLES[-1]
                    and text_generation_chat_pb.system_message is not None
                    and len(text_generation_chat_pb.system_message) > 0
                ):
                    continue
                if chat_message is None:
                    raise ValueError(
                        f"No message found in chat_history. {chat_message}"
                    )

                if len(conversation) == 1 and chat_entity["role"] != PROMPT_ROLES[0]:
                    conversation.append({"role": "user", "content": " "})

                if (
                    len(conversation) > 0
                    and conversation[-1]["role"] == chat_entity["role"]
                ):
                    last_conversation = conversation.pop()
                    chat_message = f"{last_conversation['content']}\n\n{chat_message}"

                conversation.append(
                    {"role": chat_entity["role"], "content": chat_message}
                )

        # conversation
        prompt = text_generation_chat_pb.prompt
        if len(conversation) > 0 and conversation[-1]["role"] == PROMPT_ROLES[0]:
            last_conversation = conversation.pop()
            prompt = f"{last_conversation['content']}\n\n{prompt}"

        conversation.append({"role": "user", "content": prompt})

        inp.conversation = conversation

        # max new tokens
        if text_generation_chat_pb.max_new_tokens is not None:
            inp.max_new_tokens = text_generation_chat_pb.max_new_tokens

        # temperature
        if text_generation_chat_pb.temperature is not None:
            inp.temperature = text_generation_chat_pb.temperature

        # top k
        if text_generation_chat_pb.top_k is not None:
            inp.top_k = text_generation_chat_pb.top_k

        # seed
        if text_generation_chat_pb.seed is not None:
            inp.seed = text_generation_chat_pb.seed

        input_list.append(inp)

    return input_list


def construct_task_text_generation_chat_output(texts: List[str]) -> TriggerResponse:
    task_outputs = []

    for text in texts:
        task_outputs.append(
            protobuf_to_struct(
                modelpb.TaskOutput(
                    text_generation_chat=textgenerationchatpb.TextGenerationChatOutput(
                        text=text
                    )
                )
            )
        )

    return TriggerResponse(task_outputs=task_outputs)


def parse_task_visual_question_answering_to_conversation_multimodal_input(
    request: TriggerRequest,
) -> List[ConversationMultiModelInput]:

    input_list = []

    for task_input in request.task_inputs:
        task_input_pb = struct_to_protobuf(task_input, modelpb.TaskInput)

        visual_question_answering_pb: (
            visualquestionansweringpb.VisualQuestionAnsweringInput
        ) = task_input_pb.visual_question_answering

        inp = ConversationMultiModelInput()

        conversation: List[Union[Dict[str, Union[str, Dict[str, str]]]]] = []

        # system message
        if (
            visual_question_answering_pb.system_message is not None
            and len(visual_question_answering_pb.system_message) > 0
        ):
            conversation.append(
                {
                    "role": "system",
                    "content": {
                        "type": "text",
                        "content": visual_question_answering_pb.system_message,
                    },
                }
            )

        # conversation history
        if (
            visual_question_answering_pb.chat_history is not None
            and len(visual_question_answering_pb.chat_history) > 0
        ):
            for chat_entity in visual_question_answering_pb.chat_history:
                chat_dict = json_format.MessageToDict(chat_entity)
                conversation.append(chat_dict)

        # conversation
        prompt = visual_question_answering_pb.prompt
        if len(conversation) > 0 and conversation[-1]["role"] == PROMPT_ROLES[0]:
            last_conversation = conversation.pop()
            prompt = f"{last_conversation['content']['content']}\n\n{prompt}"  # type: ignore

        conversation.append(
            {
                "role": "user",
                "content": {
                    "type": "text",
                    "content": prompt,
                },
            }
        )

        inp.conversation = conversation

        # prompt images
        prompt_image_list = []
        if (
            visual_question_answering_pb.prompt_images is not None
            and len(visual_question_answering_pb.prompt_images) > 0
        ):
            for prompt_image in visual_question_answering_pb.prompt_images:
                if (
                    prompt_image.prompt_image_base64 != ""
                    and prompt_image.prompt_image_url != ""
                ) or (
                    prompt_image.prompt_image_base64 == ""
                    and prompt_image.prompt_image_url == ""
                ):
                    raise InvalidInputException
                if prompt_image.prompt_image_base64 != "":
                    prompt_image_list.append(
                        base64_to_pil_image(prompt_image.prompt_image_base64)
                    )
                elif prompt_image.prompt_image_url != "":
                    prompt_image_list.append(
                        url_to_pil_image(prompt_image.prompt_image_url)
                    )
            inp.prompt_images = prompt_image_list

        # max new tokens
        if visual_question_answering_pb.max_new_tokens is not None:
            inp.max_new_tokens = visual_question_answering_pb.max_new_tokens

        # temperature
        if visual_question_answering_pb.temperature is not None:
            inp.temperature = visual_question_answering_pb.temperature

        # top k
        if visual_question_answering_pb.top_k is not None:
            inp.top_k = visual_question_answering_pb.top_k

        # seed
        if visual_question_answering_pb.seed is not None:
            inp.seed = visual_question_answering_pb.seed

        input_list.append(inp)

    return input_list


def construct_task_visual_question_answering_output(
    texts: List[str],
) -> TriggerResponse:
    task_outputs = []

    for text in texts:
        task_outputs.append(
            protobuf_to_struct(
                modelpb.TaskOutput(
                    visual_question_answering=visualquestionansweringpb.VisualQuestionAnsweringOutput(
                        text=text
                    )
                )
            )
        )

    return TriggerResponse(task_outputs=task_outputs)


def parse_task_text_to_image_input(
    request: TriggerRequest,
) -> List[TextToImageInput]:

    input_list = []

    for task_input in request.task_inputs:
        task_input_pb = struct_to_protobuf(task_input, modelpb.TaskInput)

        text_to_image_pb: texttoimagepb.TextToImageInput = task_input_pb.text_to_image

        inp = TextToImageInput()

        # prompt
        inp.prompt = text_to_image_pb.prompt

        # steps
        if text_to_image_pb.steps is not None:
            inp.steps = text_to_image_pb.steps

        # temperature
        if text_to_image_pb.cfg_scale is not None:
            inp.cfg_scale = text_to_image_pb.cfg_scale

        # top k
        if text_to_image_pb.samples is not None:
            inp.samples = text_to_image_pb.samples

        # seed
        if text_to_image_pb.seed is not None:
            inp.seed = text_to_image_pb.seed

        input_list.append(inp)

    return input_list


def construct_task_text_to_image_output(
    images: List[List[str]],
) -> TriggerResponse:
    """Construct trigger output for keypoint task

    Args:
        images (List[List[str]]): for each input prompt, the generated images with the length of `samples`
    """
    task_outputs = []

    for imgs in images:
        task_outputs.append(
            protobuf_to_struct(
                modelpb.TaskOutput(
                    text_to_image=texttoimagepb.TextToImageOutput(images=imgs)
                )
            )
        )

    return TriggerResponse(task_outputs=task_outputs)


def parse_task_image_to_image_input(
    request: TriggerRequest,
) -> List[ImageToImageInput]:

    input_list = []

    for task_input in request.task_inputs:
        task_input_pb = struct_to_protobuf(task_input, modelpb.TaskInput)

        image_to_image_pb: imagetoimagepb.ImageToImageInput = (
            task_input_pb.text_to_image
        )

        inp = ImageToImageInput()

        # prompt
        inp.prompt = image_to_image_pb.prompt

        # prompt images
        if (
            image_to_image_pb.prompt_image_base64 != ""
            and image_to_image_pb.prompt_image_url != ""
        ) or (
            image_to_image_pb.prompt_image_base64 == ""
            and image_to_image_pb.prompt_image_url == ""
        ):
            raise InvalidInputException
        if image_to_image_pb.prompt_image_base64 != "":
            inp.prompt_image = base64_to_pil_image(
                image_to_image_pb.prompt_image_base64
            )
        elif image_to_image_pb.prompt_image_url != "":
            inp.prompt_image = url_to_pil_image(image_to_image_pb.prompt_image_url)

        # steps
        if image_to_image_pb.steps is not None:
            inp.steps = image_to_image_pb.steps

        # temperature
        if image_to_image_pb.cfg_scale is not None:
            inp.cfg_scale = image_to_image_pb.cfg_scale

        # top k
        if image_to_image_pb.samples is not None:
            inp.samples = image_to_image_pb.samples

        # seed
        if image_to_image_pb.seed is not None:
            inp.seed = image_to_image_pb.seed

        input_list.append(inp)

    return input_list


def construct_task_image_to_image_output(
    images: List[List[str]],
) -> TriggerResponse:
    """Construct trigger output for keypoint task

    Args:
        images (List[List[str]]): for each input prompt, the generated images with the length of `samples`
    """
    task_outputs = []

    for imgs in images:
        task_outputs.append(
            protobuf_to_struct(
                modelpb.TaskOutput(
                    image_to_image=imagetoimagepb.ImageToImageOutput(images=imgs)
                )
            )
        )

    return TriggerResponse(task_outputs=task_outputs)
