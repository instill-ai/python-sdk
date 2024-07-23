# pylint: disable=no-member,no-name-in-module, inconsistent-return-statements, unused-import
import base64
import io
import re
from typing import Any, Dict, List, Union

import requests
from google.protobuf import json_format, struct_pb2
from PIL import Image
from starlette.requests import Request

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
from instill.helpers.protobufs.ray_pb2 import CallRequest, CallResponse


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

    # Convert dictionary to struct_pb2.Struct
    struct_pb = struct_pb2.Struct()
    json_format.ParseDict(dict_data, struct_pb)

    return struct_pb


async def parse_task_classification_to_vision_input(
    request: Union[CallRequest, Request],
) -> List[VisionInput]:

    # http test input
    if isinstance(request, Request):
        data: dict = await request.json()

        inp = VisionInput()
        inp.image = url_to_pil_image(data["image_url"])
        return [inp]

    input_list = []
    for task_input in request.task_inputs:
        task_input_dict = json_format.MessageToDict(task_input)["Classification"][
            "Type"
        ]
        inp = VisionInput()
        if ("ImageBase64" in task_input_dict and "ImageUrl" in task_input_dict) or (
            not "ImageBase64" in task_input_dict and not "ImageUrl" in task_input_dict
        ):
            raise InvalidInputException
        if "ImageBase64" in task_input_dict and task_input_dict["ImageBase64"] != "":
            inp.image = base64_to_pil_image(task_input_dict["ImageBase64"])
        elif "ImageUrl" in task_input_dict and task_input_dict["ImageUrl"] != "":
            inp.image = url_to_pil_image(task_input_dict["ImageUrl"])
        else:
            raise InvalidInputException

        input_list.append(inp)

    return input_list


def construct_task_classification_output(
    request: Union[CallRequest, Request],
    categories: List[str],
    scores: List[float],
) -> Union[CallResponse, Dict[str, List]]:
    if not len(categories) == len(scores):
        raise InvalidOutputShapeException

    if isinstance(request, Request):
        return {
            "categories": categories,
            "scores": scores,
        }

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

    return CallResponse(task_outputs=task_outputs)


async def parse_task_detection_to_vision_input(
    request: Union[CallRequest, Request],
) -> List[VisionInput]:

    # http test input
    if isinstance(request, Request):
        data: dict = await request.json()

        inp = VisionInput()
        inp.image = url_to_pil_image(data["image_url"])
        return [inp]

    input_list = []
    for task_input in request.task_inputs:
        task_input_dict = json_format.MessageToDict(task_input)["Detection"]["Type"]
        inp = VisionInput()
        if ("ImageBase64" in task_input_dict and "ImageUrl" in task_input_dict) or (
            not "ImageBase64" in task_input_dict and not "ImageUrl" in task_input_dict
        ):
            raise InvalidInputException
        if "ImageBase64" in task_input_dict and task_input_dict["ImageBase64"] != "":
            inp.image = base64_to_pil_image(task_input_dict["ImageBase64"])
        elif "ImageUrl" in task_input_dict and task_input_dict["ImageUrl"] != "":
            inp.image = url_to_pil_image(task_input_dict["ImageUrl"])
        else:
            raise InvalidInputException

        input_list.append(inp)

    return input_list


def construct_task_detection_output(
    request: Union[CallRequest, Request],
    categories: List[List[str]],
    scores: List[List[float]],
    bounding_boxes: List[List[tuple]],
) -> Union[CallResponse, Dict[str, List]]:
    """Construct trigger output for detection task

    Args:
        categories (List[List[str]]): for each image input, the list of detected object's category
        scores (List[List[float]]): for each image input, the list of detected object's score
        bounding_boxes (List[List[tuple]]): for each image input, the list of detected object's bbox, with the format
        (top, left, width, height)
    """
    if not len(categories) == len(scores) == len(bounding_boxes):
        raise InvalidOutputShapeException

    if isinstance(request, Request):
        return {
            "categories": categories,
            "scores": scores,
            "bounding_boxes": bounding_boxes,
        }

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

    return CallResponse(task_outputs=task_outputs)


async def parse_task_ocr_to_vision_input(
    request: Union[CallRequest, Request],
) -> List[VisionInput]:

    # http test input
    if isinstance(request, Request):
        data: dict = await request.json()

        inp = VisionInput()
        inp.image = url_to_pil_image(data["image_url"])
        return [inp]

    input_list = []
    for task_input in request.task_inputs:
        task_input_dict = json_format.MessageToDict(task_input)["Ocr"]["Type"]
        inp = VisionInput()
        if ("ImageBase64" in task_input_dict and "ImageUrl" in task_input_dict) or (
            not "ImageBase64" in task_input_dict and not "ImageUrl" in task_input_dict
        ):
            raise InvalidInputException
        if "ImageBase64" in task_input_dict and task_input_dict["ImageBase64"] != "":
            inp.image = base64_to_pil_image(task_input_dict["ImageBase64"])
        elif "ImageUrl" in task_input_dict and task_input_dict["ImageUrl"] != "":
            inp.image = url_to_pil_image(task_input_dict["ImageUrl"])
        else:
            raise InvalidInputException

        input_list.append(inp)

    return input_list


def construct_task_ocr_output(
    request: Union[CallRequest, Request],
    texts: List[List[str]],
    scores: List[List[float]],
    bounding_boxes: List[List[tuple]],
) -> Union[CallResponse, Dict[str, List]]:
    """Construct trigger output for ocr task

    Args:
        texts (List[List[str]]): for each image input, the list of detected text
        scores (List[List[float]]): for each image input, the list of detected text's score
        bounding_boxes (List[List[tuple]]): for each image input, the list of detected text's bbox, with the format
        (top, left, width, height)
    """
    if not len(texts) == len(scores) == len(bounding_boxes):
        raise InvalidOutputShapeException

    if isinstance(request, Request):
        return {
            "texts": texts,
            "scores": scores,
            "bounding_boxes": bounding_boxes,
        }

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

    return CallResponse(task_outputs=task_outputs)


async def parse_task_instance_segmentation_to_vision_input(
    request: Union[CallRequest, Request],
) -> List[VisionInput]:

    # http test input
    if isinstance(request, Request):
        data: dict = await request.json()

        inp = VisionInput()
        inp.image = url_to_pil_image(data["image_url"])
        return [inp]

    input_list = []
    for task_input in request.task_inputs:
        task_input_dict = json_format.MessageToDict(task_input)["InstanceSegmentation"][
            "Type"
        ]
        inp = VisionInput()
        if ("ImageBase64" in task_input_dict and "ImageUrl" in task_input_dict) or (
            not "ImageBase64" in task_input_dict and not "ImageUrl" in task_input_dict
        ):
            raise InvalidInputException
        if "ImageBase64" in task_input_dict and task_input_dict["ImageBase64"] != "":
            inp.image = base64_to_pil_image(task_input_dict["ImageBase64"])
        elif "ImageUrl" in task_input_dict and task_input_dict["ImageUrl"] != "":
            inp.image = url_to_pil_image(task_input_dict["ImageUrl"])
        else:
            raise InvalidInputException

        input_list.append(inp)

    return input_list


def construct_task_instance_segmentation_output(
    request: Union[CallRequest, Request],
    rles: List[List[str]],
    categories: List[List[str]],
    scores: List[List[float]],
    bounding_boxes: List[List[tuple]],
) -> Union[CallResponse, Dict[str, List]]:
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

    if isinstance(request, Request):
        return {
            "rles": rles,
            "categories": categories,
            "scores": scores,
            "bounding_boxes": bounding_boxes,
        }

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

    return CallResponse(task_outputs=task_outputs)


async def parse_task_semantic_segmentation_to_vision_input(
    request: Union[CallRequest, Request],
) -> List[VisionInput]:

    # http test input
    if isinstance(request, Request):
        data: dict = await request.json()

        inp = VisionInput()
        inp.image = url_to_pil_image(data["image_url"])
        return [inp]

    input_list = []
    for task_input in request.task_inputs:
        task_input_dict = json_format.MessageToDict(task_input)["SemanticSegmentation"][
            "Type"
        ]
        inp = VisionInput()
        if ("ImageBase64" in task_input_dict and "ImageUrl" in task_input_dict) or (
            not "ImageBase64" in task_input_dict and not "ImageUrl" in task_input_dict
        ):
            raise InvalidInputException
        if "ImageBase64" in task_input_dict and task_input_dict["ImageBase64"] != "":
            inp.image = base64_to_pil_image(task_input_dict["ImageBase64"])
        elif "ImageUrl" in task_input_dict and task_input_dict["ImageUrl"] != "":
            inp.image = url_to_pil_image(task_input_dict["ImageUrl"])
        else:
            raise InvalidInputException

        input_list.append(inp)

    return input_list


def construct_task_semantic_segmentation_output(
    request: Union[CallRequest, Request],
    rles: List[List[str]],
    categories: List[List[str]],
) -> Union[CallResponse, Dict[str, List]]:
    """Construct trigger output for semantic segmentation task

    Args:
        rles (List[List[str]]): for each image input, the list of detected object's rle
        categories (List[List[str]]): for each image input, the list of detected object's category
        (top, left, width, height)
    """
    if not len(rles) == len(categories):
        raise InvalidOutputShapeException

    if isinstance(request, Request):
        return {
            "rles": rles,
            "categories": categories,
        }

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

    return CallResponse(task_outputs=task_outputs)


async def parse_task_keypoint_to_vision_input(
    request: Union[CallRequest, Request],
) -> List[VisionInput]:

    # http test input
    if isinstance(request, Request):
        data: dict = await request.json()

        inp = VisionInput()
        inp.image = url_to_pil_image(data["image_url"])
        return [inp]

    input_list = []
    for task_input in request.task_inputs:
        task_input_dict = json_format.MessageToDict(task_input)["Keypoint"]["Type"]
        inp = VisionInput()
        if ("ImageBase64" in task_input_dict and "ImageUrl" in task_input_dict) or (
            not "ImageBase64" in task_input_dict and not "ImageUrl" in task_input_dict
        ):
            raise InvalidInputException
        if "ImageBase64" in task_input_dict and task_input_dict["ImageBase64"] != "":
            inp.image = base64_to_pil_image(task_input_dict["ImageBase64"])
        elif "ImageUrl" in task_input_dict and task_input_dict["ImageUrl"] != "":
            inp.image = url_to_pil_image(task_input_dict["ImageUrl"])
        else:
            raise InvalidInputException

        input_list.append(inp)

    return input_list


def construct_task_keypoint_output(
    request: Union[CallRequest, Request],
    keypoints: List[List[List[tuple]]],
    scores: List[List[float]],
    bounding_boxes: List[List[tuple]],
) -> Union[CallResponse, Dict[str, List]]:
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

    if isinstance(request, Request):
        return {
            "keypoints": keypoints,
            "scores": scores,
            "bounding_boxes": bounding_boxes,
        }

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

    return CallResponse(task_outputs=task_outputs)


async def parse_task_text_generation_to_conversation_input(
    request: Union[CallRequest, Request],
) -> List[ConversationInput]:

    # http test input
    if isinstance(request, Request):
        data: dict = await request.json()

        inp = ConversationInput()
        inp.conversation = [{"role": "user", "content": data["prompt"]}]
        return [inp]

    input_list = []
    for task_input in request.task_inputs:
        task_input_dict = json_format.MessageToDict(task_input)["TextGeneration"]

        inp = ConversationInput()

        conversation: List[Dict[str, str]] = []

        # system message
        if (
            "system_message" in task_input_dict
            and len(task_input_dict["system_message"]) > 0
        ):
            conversation.append(
                {"role": "system", "content": task_input_dict["system_message"]}
            )

        # conversation history
        if (
            "chat_history" in task_input_dict
            and len(task_input_dict["chat_history"]) > 0
        ):
            for chat_entity in task_input_dict["chat_history"]:
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
                            f"Unknown structure of chat_history: {task_input_dict['chat_history']}"
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
                    and task_input_dict["system_message"] is not None
                    and len(task_input_dict["system_message"]) > 0
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
        prompt = task_input_dict["prompt"]
        if len(conversation) > 0 and conversation[-1]["role"] == PROMPT_ROLES[0]:
            last_conversation = conversation.pop()
            prompt = f"{last_conversation['content']}\n\n{prompt}"

        conversation.append({"role": "user", "content": prompt})

        inp.conversation = conversation

        # max new tokens
        if "max_new_tokens" in task_input_dict:
            inp.max_new_tokens = int(task_input_dict["max_new_tokens"])

        # temperature
        if "temperature" in task_input_dict:
            inp.temperature = task_input_dict["temperature"]

        # top k
        if "top_k" in task_input_dict:
            inp.top_k = int(task_input_dict["top_k"])

        # seed
        if "seed" in task_input_dict:
            inp.seed = int(task_input_dict["seed"])

        input_list.append(inp)

    return input_list


def construct_task_text_generation_output(
    request: Union[CallRequest, Request],
    texts: List[str],
) -> Union[CallResponse, List[str]]:

    if isinstance(request, Request):
        return texts

    task_outputs = []
    for text in texts:
        task_outputs.append(
            protobuf_to_struct(
                modelpb.TaskOutput(
                    text_generation=textgenerationpb.TextGenerationOutput(text=text)
                )
            )
        )

    return CallResponse(task_outputs=task_outputs)


async def parse_task_text_generation_chat_to_conversation_input(
    request: Union[CallRequest, Request],
) -> List[ConversationInput]:

    # http test input
    if isinstance(request, Request):
        data: dict = await request.json()

        inp = ConversationInput()
        inp.conversation = [{"role": "user", "content": data["prompt"]}]
        return [inp]

    input_list = []
    for task_input in request.task_inputs:
        task_input_dict = json_format.MessageToDict(task_input)["TextGenerationChat"]

        inp = ConversationInput()

        conversation: List[Dict[str, str]] = []

        # system message
        if (
            "system_message" in task_input_dict
            and len(task_input_dict["system_message"]) > 0
        ):
            conversation.append(
                {"role": "system", "content": task_input_dict["system_message"]}
            )

        # conversation history
        if (
            "chat_history" in task_input_dict
            and len(task_input_dict["chat_history"]) > 0
        ):
            for chat_entity in task_input_dict["chat_history"]:
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
                            f"Unknown structure of chat_history: {task_input_dict['chat_history']}"
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
                    and task_input_dict["system_message"] is not None
                    and len(task_input_dict["system_message"]) > 0
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
        prompt = task_input_dict["prompt"]
        if len(conversation) > 0 and conversation[-1]["role"] == PROMPT_ROLES[0]:
            last_conversation = conversation.pop()
            prompt = f"{last_conversation['content']}\n\n{prompt}"

        conversation.append({"role": "user", "content": prompt})

        inp.conversation = conversation

        # max new tokens
        if "max_new_tokens" in task_input_dict:
            inp.max_new_tokens = int(task_input_dict["max_new_tokens"])

        # temperature
        if "temperature" in task_input_dict:
            inp.temperature = task_input_dict["temperature"]

        # top k
        if "top_k" in task_input_dict:
            inp.top_k = int(task_input_dict["top_k"])

        # seed
        if "seed" in task_input_dict:
            inp.seed = int(task_input_dict["seed"])

    input_list.append(inp)

    return input_list


def construct_task_text_generation_chat_output(
    request: Union[CallRequest, Request],
    texts: List[str],
) -> Union[CallResponse, List[str]]:

    if isinstance(request, Request):
        return texts

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

    return CallResponse(task_outputs=task_outputs)


async def parse_task_visual_question_answering_to_conversation_multimodal_input(
    request: Union[CallRequest, Request],
) -> List[ConversationMultiModelInput]:

    # http test input
    if isinstance(request, Request):
        data: dict = await request.json()

        test_prompt = data["prompt"]
        image_url = data["image_url"]

        inp = ConversationMultiModelInput()
        inp.conversation = [
            {
                "role": "user",
                "content": {
                    "type": "text",
                    "content": test_prompt,
                },
            }
        ]
        inp.prompt_images = [url_to_pil_image(image_url)]
        return [inp]

    input_list = []
    for task_input in request.task_inputs:
        task_input_dict = json_format.MessageToDict(task_input)[
            "VisualQuestionAnswering"
        ]

        inp = ConversationMultiModelInput()

        conversation: List[Union[Dict[str, Union[str, Dict[str, str]]]]] = []

        # system message
        if (
            "system_message" in task_input_dict
            and len(task_input_dict["system_message"]) > 0
        ):
            conversation.append(
                {"role": "system", "content": task_input_dict["system_message"]}
            )

        # conversation history
        if (
            "chat_history" in task_input_dict
            and len(task_input_dict["chat_history"]) > 0
        ):
            for chat_entity in task_input_dict["chat_history"]:
                chat_dict = json_format.MessageToDict(chat_entity)
                conversation.append(chat_dict)

        # conversation
        prompt = task_input_dict["prompt"]
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
            "prompt_images" in task_input_dict
            and len(task_input_dict["prompt_images"]) > 0
        ):
            for prompt_image in task_input_dict["prompt_images"]:
                if (
                    "PromptImageUrl" in prompt_image["Type"]
                    and "PromptImageBase64" in prompt_image["Type"]
                ) or (
                    "PromptImageUrl" not in prompt_image["Type"]
                    and "PromptImageBase64" not in prompt_image["Type"]
                ):
                    raise InvalidInputException
                if "PromptImageUrl" in prompt_image["Type"]:
                    prompt_image_list.append(
                        url_to_pil_image(prompt_image["Type"]["PromptImageUrl"])
                    )
                elif "PromptImageBase64" in prompt_image["Type"]:
                    prompt_image_list.append(
                        base64_to_pil_image(prompt_image["Type"]["PromptImageBase64"])
                    )
            inp.prompt_images = prompt_image_list

        # max new tokens
        if "max_new_tokens" in task_input_dict:
            inp.max_new_tokens = int(task_input_dict["max_new_tokens"])

        # temperature
        if "temperature" in task_input_dict:
            inp.temperature = task_input_dict["temperature"]

        # top k
        if "top_k" in task_input_dict:
            inp.top_k = int(task_input_dict["top_k"])

        # seed
        if "seed" in task_input_dict:
            inp.seed = int(task_input_dict["seed"])

        input_list.append(inp)

    return input_list


def construct_task_visual_question_answering_output(
    request: Union[CallRequest, Request],
    texts: List[str],
) -> Union[CallResponse, List[str]]:

    if isinstance(request, Request):
        return texts

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

    return CallResponse(task_outputs=task_outputs)


async def parse_task_text_to_image_input(
    request: Union[CallRequest, Request],
) -> List[TextToImageInput]:

    # http test input
    if isinstance(request, Request):
        data: dict = await request.json()

        inp = TextToImageInput()
        inp.prompt = data["prompt"]

        return [inp]

    input_list = []
    for task_input in request.task_inputs:
        task_input_dict = json_format.MessageToDict(task_input)["TextToImage"]

        inp = TextToImageInput()

        # prompt
        inp.prompt = task_input_dict["prompt"]

        # steps
        if "steps" in task_input_dict:
            inp.steps = int(task_input_dict["steps"])

        # cfg_scale
        if "cfg_scale" in task_input_dict:
            inp.cfg_scale = task_input_dict["cfg_scale"]

        # samples
        if "samples" in task_input_dict:
            inp.samples = int(task_input_dict["samples"])

        # seed
        if "seed" in task_input_dict:
            inp.seed = int(task_input_dict["seed"])

        input_list.append(inp)

    return input_list


def construct_task_text_to_image_output(
    request: Union[CallRequest, Request],
    images: List[List[str]],
) -> Union[CallResponse, List[List[str]]]:
    """Construct trigger output for keypoint task

    Args:
        images (List[List[str]]): for each input prompt, the generated images with the length of `samples`
    """

    if isinstance(request, Request):
        return images

    task_outputs = []
    for imgs in images:
        task_outputs.append(
            protobuf_to_struct(
                modelpb.TaskOutput(
                    text_to_image=texttoimagepb.TextToImageOutput(images=imgs)
                )
            )
        )

    return CallResponse(task_outputs=task_outputs)


async def parse_task_image_to_image_input(
    request: Union[CallRequest, Request],
) -> List[ImageToImageInput]:

    # http test input
    if isinstance(request, Request):
        data: dict = await request.json()

        test_prompt = data["prompt"]
        test_image_url = data["image_url"]

        inp = ImageToImageInput()
        inp.prompt = test_prompt
        inp.prompt_image = url_to_pil_image(test_image_url)

        return [inp]

    input_list = []
    for task_input in request.task_inputs:
        task_input_dict = json_format.MessageToDict(task_input)["ImageToImage"]

        inp = ImageToImageInput()

        # prompt
        inp.prompt = task_input_dict["prompt"]

        # prompt images
        if (
            "PromptImageUrl" in task_input_dict["Type"]
            and "PromptImageBase64" in task_input_dict["Type"]
        ) or (
            "PromptImageUrl" not in task_input_dict["Type"]
            and "PromptImageBase64" not in task_input_dict["Type"]
        ):
            raise InvalidInputException
        if "PromptImageUrl" in task_input_dict["Type"]:
            inp.prompt_image = url_to_pil_image(
                task_input_dict["Type"]["PromptImageUrl"]
            )
        elif "PromptImageBase64" in task_input_dict["Type"]:
            inp.prompt_image = base64_to_pil_image(
                task_input_dict["Type"]["PromptImageBase64"]
            )

        # steps
        if "steps" in task_input_dict:
            inp.steps = int(task_input_dict["steps"])

        # cfg_scale
        if "cfg_scale" in task_input_dict:
            inp.cfg_scale = task_input_dict["cfg_scale"]

        # samples
        if "samples" in task_input_dict:
            inp.samples = int(task_input_dict["samples"])

        # seed
        if "seed" in task_input_dict:
            inp.seed = int(task_input_dict["seed"])

        input_list.append(inp)

    return input_list


def construct_task_image_to_image_output(
    request: Union[CallRequest, Request],
    images: List[List[str]],
) -> Union[CallResponse, List[List[str]]]:
    """Construct trigger output for keypoint task

    Args:
        images (List[List[str]]): for each input prompt, the generated images with the length of `samples`
    """

    if isinstance(request, Request):
        return images

    task_outputs = []
    for imgs in images:
        task_outputs.append(
            protobuf_to_struct(
                modelpb.TaskOutput(
                    image_to_image=imagetoimagepb.ImageToImageOutput(images=imgs)
                )
            )
        )

    return CallResponse(task_outputs=task_outputs)
