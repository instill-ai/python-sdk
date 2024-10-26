# pylint: disable=no-member,no-name-in-module, inconsistent-return-statements, unused-import
import base64
import io
import re
from typing import Dict, List, Union

import numpy as np
import requests
from google.protobuf import json_format, struct_pb2
from PIL import Image
from starlette.requests import Request

from instill.helpers.const import (
    HEADERS,
    IMAGE_INPUT_TYPE_BASE64,
    IMAGE_INPUT_TYPE_URL,
    PROMPT_ROLES,
    ChatInput,
    ChatMultiModalInput,
    CompletionInput,
    ImageEmbeddingInput,
    MultimodalEmbeddingInput,
    TextEmbeddingInput,
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
    resp = requests.get(url, headers=HEADERS, timeout=10)
    resp.raise_for_status()
    return Image.open(io.BytesIO(resp.content))


def snake_to_lower_camel(name):
    """Convert snake_case to lowerCamelCase."""
    components = name.split("_")
    return components[0] + "".join(x.title() for x in components[1:])


def dict_to_struct(dict_data):
    """Convert Dict to Struct"""
    struct_pb = struct_pb2.Struct()
    json_format.ParseDict(dict_data, struct_pb)

    return struct_pb


async def _parse_vision_task_to_vision_input(
    request: Union[CallRequest, Request],
) -> List[VisionInput]:

    def extract_data(data: dict) -> VisionInput:
        image_type = data["type"]

        inp = VisionInput()
        if image_type == IMAGE_INPUT_TYPE_URL:
            inp.image = url_to_pil_image(data[image_type])
        elif image_type == IMAGE_INPUT_TYPE_BASE64:
            inp.image = base64_to_pil_image(data[image_type])
        else:
            raise InvalidInputException("input image type not supported")

        return inp

    # http test input
    if isinstance(request, Request):
        data: dict = await request.json()

        if "type" not in data:
            data["type"] = IMAGE_INPUT_TYPE_URL

        return [extract_data(data)]

    input_list = []
    for task_input in request.task_inputs:
        task_input_dict = json_format.MessageToDict(task_input)

        data = task_input_dict["data"]

        input_list.append(extract_data(data))

    return input_list


async def parse_task_classification_to_vision_input(
    request: Union[CallRequest, Request],
) -> List[VisionInput]:

    return await _parse_vision_task_to_vision_input(request)


def construct_task_classification_output(
    request: Union[CallRequest, Request],
    categories: List[str],
    scores: List[float],
) -> Union[CallResponse, List]:
    if not len(categories) == len(scores):
        raise InvalidOutputShapeException

    task_outputs = []
    for category, score in zip(categories, scores):
        data = {"category": str(category), "score": float(score)}

        if isinstance(request, Request):
            task_outputs.append({"data": data})
        else:
            task_outputs.append(dict_to_struct({"data": data}))

    if isinstance(request, Request):
        return task_outputs

    return CallResponse(task_outputs=task_outputs)


async def parse_task_detection_to_vision_input(
    request: Union[CallRequest, Request],
) -> List[VisionInput]:

    return await _parse_vision_task_to_vision_input(request)


def construct_task_detection_output(
    request: Union[CallRequest, Request],
    categories: List[List[str]],
    scores: List[List[float]],
    bounding_boxes: List[List[tuple]],
) -> Union[CallResponse, List]:
    """Construct trigger output for detection task

    Args:
        categories (List[List[str]]): for each image input, the list of detected object's category
        scores (List[List[float]]): for each image input, the list of detected object's score
        bounding_boxes (List[List[tuple]]): for each image input, the list of detected object's bbox, with the format
        (top left x, top left y, width, height)
    """
    if not len(categories) == len(scores) == len(bounding_boxes):
        raise InvalidOutputShapeException

    task_outputs = []
    for category, score, bbox in zip(categories, scores, bounding_boxes):
        data = {}
        objects = []
        for cat, sc, bb in zip(category, score, bbox):
            bb_dict = {
                "top": float(bb[1]),
                "left": float(bb[0]),
                "width": float(bb[2]),
                "height": float(bb[3]),
            }
            objects.append(
                {"category": str(cat), "score": float(sc), "bounding-box": bb_dict}
            )

        data["objects"] = objects

        if isinstance(request, Request):
            task_outputs.append({"data": data})
        else:
            task_outputs.append(dict_to_struct({"data": data}))

    if isinstance(request, Request):
        return task_outputs

    return CallResponse(task_outputs=task_outputs)


async def parse_task_ocr_to_vision_input(
    request: Union[CallRequest, Request],
) -> List[VisionInput]:

    return await _parse_vision_task_to_vision_input(request)


def construct_task_ocr_output(
    request: Union[CallRequest, Request],
    texts: List[List[str]],
    scores: List[List[float]],
    bounding_boxes: List[List[tuple]],
) -> Union[CallResponse, List]:
    """Construct trigger output for ocr task

    Args:
        texts (List[List[str]]): for each image input, the list of detected text
        scores (List[List[float]]): for each image input, the list of detected text's score
        bounding_boxes (List[List[tuple]]): for each image input, the list of detected text's bbox, with the format
        (top left x, top left y, width, height)
    """
    if not len(texts) == len(scores) == len(bounding_boxes):
        raise InvalidOutputShapeException

    task_outputs = []
    for text, score, bbox in zip(texts, scores, bounding_boxes):
        data = {}
        objects = []
        for txt, sc, bb in zip(text, score, bbox):
            bb_dict = {
                "top": float(bb[1]),
                "left": float(bb[0]),
                "width": float(bb[2]),
                "height": float(bb[3]),
            }
            objects.append(
                {"text": str(txt), "score": float(sc), "bounding-box": bb_dict}
            )

        data["objects"] = objects

        if isinstance(request, Request):
            task_outputs.append({"data": data})
        else:
            task_outputs.append(dict_to_struct({"data": data}))

    if isinstance(request, Request):
        return task_outputs

    return CallResponse(task_outputs=task_outputs)


async def parse_task_instance_segmentation_to_vision_input(
    request: Union[CallRequest, Request],
) -> List[VisionInput]:

    return await _parse_vision_task_to_vision_input(request)


def construct_task_instance_segmentation_output(
    request: Union[CallRequest, Request],
    rles: List[List[str]],
    categories: List[List[str]],
    scores: List[List[float]],
    bounding_boxes: List[List[tuple]],
) -> Union[CallResponse, List]:
    """Construct trigger output for instance segmentation task

    Args:
        rles (List[List[str]]): for each image input, the list of detected object's rle
        categories (List[List[str]]): for each image input, the list of detected object's category
        scores (List[List[float]]): for each image input, the list of detected text's score
        bounding_boxes (List[List[tuple]]): for each image input, the list of detected text's bbox, with the format
        (top left x, top left y, width, height)
    """
    if not len(rles) == len(categories) == len(scores) == len(bounding_boxes):
        raise InvalidOutputShapeException

    task_outputs = []
    for rle, category, score, bbox in zip(rles, categories, scores, bounding_boxes):
        data = {}
        objects = []
        for r, cat, sc, bb in zip(rle, category, score, bbox):
            bb_dict = {
                "top": float(bb[1]),
                "left": float(bb[0]),
                "width": float(bb[2]),
                "height": float(bb[3]),
            }
            objects.append(
                {
                    "rle": str(r),
                    "category": str(cat),
                    "score": float(sc),
                    "bounding-box": bb_dict,
                }
            )

        data["objects"] = objects

        if isinstance(request, Request):
            task_outputs.append({"data": data})
        else:
            task_outputs.append(dict_to_struct({"data": data}))

    if isinstance(request, Request):
        return task_outputs

    return CallResponse(task_outputs=task_outputs)


async def parse_task_semantic_segmentation_to_vision_input(
    request: Union[CallRequest, Request],
) -> List[VisionInput]:

    return await _parse_vision_task_to_vision_input(request)


def construct_task_semantic_segmentation_output(
    request: Union[CallRequest, Request],
    rles: List[List[str]],
    categories: List[List[str]],
) -> Union[CallResponse, List]:
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
        data = {}
        objects = []
        for r, cat in zip(rle, category):
            objects.append({"rle": str(r), "category": str(cat)})

        data["stuffs"] = objects

        if isinstance(request, Request):
            task_outputs.append({"data": data})
        else:
            task_outputs.append(dict_to_struct({"data": data}))

    if isinstance(request, Request):
        return task_outputs

    return CallResponse(task_outputs=task_outputs)


async def parse_task_keypoint_to_vision_input(
    request: Union[CallRequest, Request],
) -> List[VisionInput]:

    return await _parse_vision_task_to_vision_input(request)


def construct_task_keypoint_output(
    request: Union[CallRequest, Request],
    keypoints: List[List[List[tuple]]],
    scores: List[List[float]],
    bounding_boxes: List[List[tuple]],
) -> Union[CallResponse, List]:
    """Construct trigger output for keypoint task

    Args:
        keypoints (List[List[List[str]]]): for each image input, the list of detected object's keypoints,
        with the format (x_coordinate, y_coordinate, visibility)
        scores (List[List[float]]): for each image input, the list of detected object's score
        bounding_boxes (List[List[tuple]]): for each image input, the list of detected object's bbox, with the format
        (top left x, top left y, width, height)
    """

    if not len(keypoints) == len(scores) == len(bounding_boxes):
        raise InvalidOutputShapeException

    task_outputs = []
    for keypoint, score, bbox in zip(keypoints, scores, bounding_boxes):
        data = {}
        objects = []
        for kps, sc, bb in zip(keypoint, score, bbox):
            point_list = []
            for kp in kps:
                point_list.append({"x": kp[0], "y": kp[1], "v": kp[2]})

            bb_dict = {
                "top": float(bb[1]),
                "left": float(bb[0]),
                "width": float(bb[2]),
                "height": float(bb[3]),
            }
            objects.append(
                {"keypoints": point_list, "score": float(sc), "bounding-box": bb_dict}
            )

        data["objects"] = objects

        if isinstance(request, Request):
            task_outputs.append({"data": data})
        else:
            task_outputs.append(dict_to_struct({"data": data}))

    if isinstance(request, Request):
        return task_outputs

    return CallResponse(task_outputs=task_outputs)


async def parse_task_completion_to_completion_input(
    request: Union[CallRequest, Request],
) -> List[CompletionInput]:

    # http test input
    if isinstance(request, Request):
        test_data: dict = await request.json()

        inp = CompletionInput()
        inp.prompt = test_data["prompt"]
        return [inp]

    input_list = []
    for task_input in request.task_inputs:
        task_input_dict = json_format.MessageToDict(task_input)

        data = task_input_dict["data"]
        parameter = (
            task_input_dict["parameter"] if "parameter" in task_input_dict else {}
        )

        inp = CompletionInput()

        inp.prompt = data["prompt"]

        # system message
        if "system-message" in data:
            inp.system_message = data["system-message"]
        else:
            inp.system_message = (
                "You are a helpful, respectful and honest assistant. "
                "Always answer as helpfully as possible, while being safe.  "
                "Your answers should not include any harmful, unethical, racist, "
                "sexist, toxic, dangerous, or illegal content. Please ensure that "
                "your responses are socially unbiased and positive in nature. "
                "If a question does not make any sense, or is not factually coherent, "
                "explain why instead of answering something not correct. If you don't "
                "know the answer to a question, please don't share false information."
            )

        # max tokens
        if "max-tokens" in parameter:
            inp.max_tokens = int(parameter["max-tokens"])

        # temperature
        if "temperature" in parameter:
            inp.temperature = parameter["temperature"]

        # number of generated outputs
        if "n" in parameter:
            inp.n = int(parameter["n"])

        # top p
        if "top-p" in parameter:
            inp.top_p = int(parameter["top-p"])

        # seed
        if "seed" in parameter:
            inp.seed = int(parameter["seed"])

        # stream
        if "stream" in parameter:
            inp.seed = int(parameter["stream"])

        input_list.append(inp)

    return input_list


def construct_task_completion_output(
    request: Union[CallRequest, Request],
    finish_reasons: List[List[str]],
    indexes: List[List[int]],
    created_timestamps: List[List[int]],
    contents: List[List[str]],
    completion_tokens: Union[List[int], None] = None,
    prompt_tokens: Union[List[int], None] = None,
    total_tokens: Union[List[int], None] = None,
) -> Union[CallResponse, List]:

    if (
        not len(finish_reasons)
        == len(indexes)
        == len(created_timestamps)
        == len(contents)
    ):
        raise InvalidOutputShapeException
    if len(contents) > 0 and not (
        len(finish_reasons[0])
        == len(indexes[0])
        == len(created_timestamps[0])
        == len(contents[0])
    ):
        raise InvalidOutputShapeException

    if completion_tokens is None or prompt_tokens is None or total_tokens is None:
        print("one or more of token usage number not set, ignore all ")
    else:
        if not len(completion_tokens) == len(prompt_tokens) == len(total_tokens):
            raise InvalidOutputShapeException

    task_outputs = []
    # data
    for finish_reason_list, index_list, created_timestamp_list, content_list in zip(
        finish_reasons, indexes, created_timestamps, contents
    ):
        data = {}
        choices = []
        for (
            finish_reason,
            index,
            created_timestamp,
            content,
        ) in zip(finish_reason_list, index_list, created_timestamp_list, content_list):
            choices.append(
                {
                    "finish-reason": finish_reason,
                    "index": index,
                    "content": content,
                    "created": created_timestamp,
                }
            )
        data["choices"] = choices
        task_outputs.append({"data": data})

    # metadata
    if (
        completion_tokens is not None
        and prompt_tokens is not None
        and total_tokens is not None
    ):
        for i, (completion_token, prompt_token, total_token) in enumerate(
            zip(completion_tokens, prompt_tokens, total_tokens)
        ):
            metadata = {
                "usage": {
                    "completion-tokens": completion_token,
                    "prompt-tokens": prompt_token,
                    "total-tokens": total_token,
                }
            }
            task_outputs[i]["metadata"] = metadata  # type: ignore

    if isinstance(request, Request):
        return task_outputs

    for i, o in enumerate(task_outputs):
        task_outputs[i] = dict_to_struct(o)

    return CallResponse(task_outputs=task_outputs)


async def parse_task_chat_to_chat_input(
    request: Union[CallRequest, Request],
) -> List[ChatInput]:

    # http test input
    if isinstance(request, Request):
        test_data: dict = await request.json()

        inp = ChatInput()
        inp.messages = [{"role": "user", "content": test_data["prompt"]}]
        return [inp]

    input_list = []
    for task_input in request.task_inputs:
        task_input_dict = json_format.MessageToDict(task_input)

        data = task_input_dict["data"]
        parameter = (
            task_input_dict["parameter"] if "parameter" in task_input_dict else {}
        )

        inp = ChatInput()

        messages: List[Dict[str, str]] = []

        # messages
        if len(data["messages"]) > 0:
            for chat_entity in data["messages"]:
                chat_message = None
                if len(chat_entity["content"]) > 1:
                    raise ValueError(
                        "Multiple text message detected"
                        " in a single chat history entity"
                    )

                if "text" in chat_entity["content"][0]:
                    chat_message = chat_entity["content"][0]["text"]
                else:
                    raise ValueError(
                        "Unsupported chat_hisotry message type"
                        ", expected 'text'"
                        f" but get {chat_entity['content'][0]}"
                    )

                if chat_entity["role"] not in PROMPT_ROLES:
                    raise ValueError(
                        f"Role `{chat_entity['role']}` is not in supported"
                        f"role list ({','.join(PROMPT_ROLES)})"
                    )
                if chat_message is None:
                    raise ValueError(
                        f"No message found in chat_history. {chat_message}"
                    )

                if (
                    len(messages) > 0
                    and messages[-1]["role"] != PROMPT_ROLES[0]
                    and chat_entity["role"] != PROMPT_ROLES[0]
                ):
                    messages.append({"role": "user", "content": " "})

                if len(messages) > 0 and messages[-1]["role"] == chat_entity["role"]:
                    last_conversation = messages.pop()
                    chat_message = f"{last_conversation['content']}\n\n{chat_message}"

                messages.append({"role": chat_entity["role"], "content": chat_message})

            if messages[0]["role"] != PROMPT_ROLES[-1]:
                messages.insert(
                    0,
                    {
                        "role": PROMPT_ROLES[-1],
                        "content": (
                            "You are a helpful, respectful and honest assistant. "
                            "Always answer as helpfully as possible, while being safe.  "
                            "Your answers should not include any harmful, unethical, racist, "
                            "sexist, toxic, dangerous, or illegal content. Please ensure that "
                            "your responses are socially unbiased and positive in nature. "
                            "If a question does not make any sense, or is not factually coherent, "
                            "explain why instead of answering something not correct. If you don't "
                            "know the answer to a question, please don't share false information."
                        ),
                    },
                )

        inp.messages = messages

        # max tokens
        if "max-tokens" in parameter:
            inp.max_tokens = int(parameter["max-tokens"])

        # temperature
        if "temperature" in parameter:
            inp.temperature = parameter["temperature"]

        # number of generated outputs
        if "n" in parameter:
            inp.n = int(parameter["n"])

        # top p
        if "top-p" in parameter:
            inp.top_p = int(parameter["top-p"])

        # seed
        if "seed" in parameter:
            inp.seed = int(parameter["seed"])

        # stream
        if "stream" in parameter:
            inp.seed = int(parameter["stream"])

        input_list.append(inp)

    return input_list


def construct_task_chat_output(
    request: Union[CallRequest, Request],
    finish_reasons: List[List[str]],
    indexes: List[List[int]],
    created_timestamps: List[List[int]],
    messages: List[List[dict]],
    completion_tokens: Union[List[int], None] = None,
    prompt_tokens: Union[List[int], None] = None,
    total_tokens: Union[List[int], None] = None,
) -> Union[CallResponse, List]:

    if (
        not len(finish_reasons)
        == len(indexes)
        == len(created_timestamps)
        == len(messages)
    ):
        raise InvalidOutputShapeException
    if len(messages) > 0 and not (
        len(finish_reasons[0])
        == len(indexes[0])
        == len(created_timestamps[0])
        == len(messages[0])
    ):
        raise InvalidOutputShapeException

    if completion_tokens is None or prompt_tokens is None or total_tokens is None:
        print("one or more of token usage number not set, ignore all ")
    else:
        if not len(completion_tokens) == len(prompt_tokens) == len(total_tokens):
            raise InvalidOutputShapeException

    task_outputs = []
    # data
    for finish_reason_list, index_list, created_timestamp_list, message_list in zip(
        finish_reasons, indexes, created_timestamps, messages
    ):
        data = {}
        choices = []
        for (
            finish_reason,
            index,
            created_timestamp,
            message,
        ) in zip(finish_reason_list, index_list, created_timestamp_list, message_list):
            choices.append(
                {
                    "finish-reason": finish_reason,
                    "index": index,
                    "message": message,
                    "created": created_timestamp,
                }
            )
        data["choices"] = choices
        task_outputs.append({"data": data})

    # metadata
    if (
        completion_tokens is not None
        and prompt_tokens is not None
        and total_tokens is not None
    ):
        for i, (completion_token, prompt_token, total_token) in enumerate(
            zip(completion_tokens, prompt_tokens, total_tokens)
        ):
            metadata = {
                "usage": {
                    "completion-tokens": completion_token,
                    "prompt-tokens": prompt_token,
                    "total-tokens": total_token,
                }
            }
            task_outputs[i]["metadata"] = metadata  # type: ignore

    if isinstance(request, Request):
        return task_outputs

    for i, o in enumerate(task_outputs):
        task_outputs[i] = dict_to_struct(o)

    return CallResponse(task_outputs=task_outputs)


async def parse_task_chat_to_multimodal_chat_input(
    request: Union[CallRequest, Request],
) -> List[ChatMultiModalInput]:

    # http test input
    if isinstance(request, Request):
        test_data: dict = await request.json()

        test_prompt = test_data["prompt"]
        image_url = test_data["image-url"]

        inp = ChatMultiModalInput()
        inp.messages = [
            {
                "role": "user",
                "content": test_prompt,
            }
        ]
        inp.prompt_images = [[url_to_pil_image(image_url)]]
        return [inp]

    input_list = []
    for task_input in request.task_inputs:
        task_input_dict = json_format.MessageToDict(task_input)

        data = task_input_dict["data"]
        parameter = (
            task_input_dict["parameter"] if "parameter" in task_input_dict else {}
        )

        inp = ChatMultiModalInput()

        # messages and prompt images
        messages: List[Dict[str, str]] = []
        images: List[List[Image.Image]] = []
        for i, message in enumerate(data["messages"]):
            role = message["role"]
            content = message["content"]

            imgs = []
            if role == PROMPT_ROLES[0]:
                for c in content:
                    if c["type"] == "text":
                        if len(messages) > i:
                            raise InvalidInputException(
                                "can only have single text from user in each round"
                            )
                        messages.insert(i, {"role": role, "content": c["text"]})
                    elif c["type"] == "image-url":
                        imgs.append(url_to_pil_image(c["image-url"]))
                    elif c["type"] == "image-base64":
                        imgs.append(base64_to_pil_image(c["image-base64"]))
                    else:
                        raise InvalidInputException("input content type not supported")
            elif role == PROMPT_ROLES[1]:
                messages.append({"role": role, "content": content[0]["text"]})
            elif role == PROMPT_ROLES[-1] and messages[0]["role"] != PROMPT_ROLES[-1]:
                messages.insert(0, {"role": role, "content": content[0]["text"]})

            images.append(imgs)

        if messages[0]["role"] != PROMPT_ROLES[-1]:
            images.insert(0, [])
            messages.insert(
                0,
                {
                    "role": PROMPT_ROLES[-1],
                    "content": (
                        "You are a helpful, respectful and honest assistant. "
                        "Always answer as helpfully as possible, while being safe.  "
                        "Your answers should not include any harmful, unethical, racist, "
                        "sexist, toxic, dangerous, or illegal content. Please ensure that "
                        "your responses are socially unbiased and positive in nature. "
                        "If a question does not make any sense, or is not factually coherent, "
                        "explain why instead of answering something not correct. If you don't "
                        "know the answer to a question, please don't share false information."
                    ),
                },
            )

        inp.messages = messages
        inp.prompt_images = images

        # max tokens
        if "max-tokens" in parameter:
            inp.max_tokens = int(parameter["max-tokens"])

        # temperature
        if "temperature" in parameter:
            inp.temperature = parameter["temperature"]

        # number of generated outputs
        if "n" in parameter:
            inp.n = int(parameter["n"])

        # top p
        if "top-p" in parameter:
            inp.top_p = int(parameter["top-p"])

        # seed
        if "seed" in parameter:
            inp.seed = int(parameter["seed"])

        # stream
        if "stream" in parameter:
            inp.seed = int(parameter["stream"])

        input_list.append(inp)

    return input_list


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
        task_input_dict = json_format.MessageToDict(task_input)

        data = task_input_dict["data"]
        parameter = (
            task_input_dict["parameter"] if "parameter" in task_input_dict else {}
        )

        inp = TextToImageInput()

        # prompt
        inp.prompt = data["prompt"]

        # negative prompt
        if "negative-prompt" in parameter:
            inp.negative_prompt = str(parameter["negative-prompt"])

        # aspect ratio
        if "aspect-ratio" in parameter:
            inp.aspect_ratio = str(parameter["aspect-ratio"])

        # number of generated outputs
        if "n" in parameter:
            inp.n = int(parameter["n"])

        # seed
        if "seed" in parameter:
            inp.seed = int(parameter["seed"])

        input_list.append(inp)

    return input_list


def construct_task_text_to_image_output(
    request: Union[CallRequest, Request],
    finish_reasons: List[List[str]],
    images: List[List[str]],
) -> Union[CallResponse, List]:
    """Construct trigger output for text to image task

    Args:
        images (List[List[str]]): for each input prompt,
        the generated jpeg image base64 string with the length of `samples`
    """

    if not len(finish_reasons) == len(images):
        raise InvalidOutputShapeException
    if len(images) > 0 and not len(finish_reasons[0]) == len(images[0]):
        raise InvalidOutputShapeException

    task_outputs = []
    for imgs, finishes in zip(images, finish_reasons):
        data = {}
        choices = []

        for img, finish in zip(imgs, finishes):
            choices.append(
                {
                    "finish-reason": finish,
                    "image": f"data:image/jpeg;base64,{img}",
                }
            )
        data["choices"] = choices
        task_outputs.append({"data": data})

    if isinstance(request, Request):
        return task_outputs

    for i, o in enumerate(task_outputs):
        task_outputs[i] = dict_to_struct(o)

    return CallResponse(task_outputs=task_outputs)


# async def parse_task_image_to_image_input(
#     request: Union[CallRequest, Request],
# ) -> List[ImageToImageInput]:

#     # http test input
#     if isinstance(request, Request):
#         data: dict = await request.json()

#         test_prompt = data["prompt"]
#         test_image_url = data["image_url"]

#         inp = ImageToImageInput()
#         inp.prompt = test_prompt
#         inp.prompt_image = url_to_pil_image(test_image_url)

#         return [inp]

#     input_list = []
#     for task_input in request.task_inputs:
#         task_input_dict = json_format.MessageToDict(task_input)["ImageToImage"]

#         inp = ImageToImageInput()

#         # prompt
#         inp.prompt = task_input_dict["prompt"]

#         # prompt images
#         if (
#             "Promptimage-url" in task_input_dict["Type"]
#             and "Promptimage-base64" in task_input_dict["Type"]
#         ) or (
#             "Promptimage-url" not in task_input_dict["Type"]
#             and "Promptimage-base64" not in task_input_dict["Type"]
#         ):
#             raise InvalidInputException
#         if "Promptimage-url" in task_input_dict["Type"]:
#             inp.prompt_image = url_to_pil_image(
#                 task_input_dict["Type"]["Promptimage-url"]
#             )
#         elif "Promptimage-base64" in task_input_dict["Type"]:
#             inp.prompt_image = base64_to_pil_image(
#                 task_input_dict["Type"]["Promptimage-base64"]
#             )

#         # steps
#         if "steps" in task_input_dict:
#             inp.steps = int(task_input_dict["steps"])

#         # cfg_scale
#         if "cfg_scale" in task_input_dict:
#             inp.cfg_scale = task_input_dict["cfg_scale"]

#         # samples
#         if "samples" in task_input_dict:
#             inp.samples = int(task_input_dict["samples"])

#         # seed
#         if "seed" in task_input_dict:
#             inp.seed = int(task_input_dict["seed"])

#         input_list.append(inp)

#     return input_list


# def construct_task_image_to_image_output(
#     request: Union[CallRequest, Request],
#     images: List[List[str]],
# ) -> Union[CallResponse, List[List[str]]]:
#     """Construct trigger output for keypoint task

#     Args:
#         images (List[List[str]]): for each input prompt, the generated images with the length of `samples`
#     """

#     if isinstance(request, Request):
#         return images

#     task_outputs = []
#     for imgs in images:
#         task_outputs.append(
#             protobuf_to_struct(
#                 modelpb.TaskOutput(
#                     image_to_image=imagetoimagepb.ImageToImageOutput(images=imgs)
#                 )
#             )
#         )

#     return CallResponse(task_outputs=task_outputs)


async def parse_task_embedding_to_text_embedding_input(
    request: Union[CallRequest, Request],
) -> List[TextEmbeddingInput]:

    # http test input
    if isinstance(request, Request):
        test_data: dict = await request.json()

        test_prompt = test_data["prompt"]

        inp = TextEmbeddingInput()
        inp.contents = [test_prompt]

        return [inp]

    input_list = []
    for task_input in request.task_inputs:
        task_input_dict = json_format.MessageToDict(task_input)

        data = task_input_dict["data"]
        parameter = (
            task_input_dict["parameter"] if "parameter" in task_input_dict else {}
        )

        inp = TextEmbeddingInput()

        # messages and prompt images
        contents: List[str] = []
        for embedding in data["embeddings"]:
            if embedding["type"] == "text":
                contents.append(embedding["text"])
            else:
                raise InvalidInputException("this model can only process text input")

        inp.contents = contents

        # format
        if "format" in parameter:
            inp.format = str(parameter["format"])

        # dimensions
        if "dimensions" in parameter:
            inp.dimensions = int(parameter["dimensions"])

        # input-type
        if "input-type" in parameter:
            inp.input_type = str(parameter["input-type"])

        # truncate
        if "truncate" in parameter:
            inp.truncate = str(parameter["truncate"])

        input_list.append(inp)

    return input_list


async def parse_task_embedding_to_image_embedding_input(
    request: Union[CallRequest, Request],
) -> List[ImageEmbeddingInput]:

    # http test input
    if isinstance(request, Request):
        test_data: dict = await request.json()

        test_img = test_data["image"]

        inp = ImageEmbeddingInput()
        inp.images = [url_to_pil_image(test_img)]

        return [inp]

    input_list = []
    for task_input in request.task_inputs:
        task_input_dict = json_format.MessageToDict(task_input)

        data = task_input_dict["data"]
        parameter = (
            task_input_dict["parameter"] if "parameter" in task_input_dict else {}
        )

        inp = ImageEmbeddingInput()

        # messages and prompt images
        images: List[Image.Image] = []
        for embedding in data["embeddings"]:
            if embedding["type"] == "image-url":
                images.append(url_to_pil_image(embedding[embedding["type"]]))
            elif embedding["type"] == "image-base64":
                images.append(base64_to_pil_image(embedding[embedding["type"]]))
            else:
                raise InvalidInputException("can only process image input")

        inp.images = images

        # format
        if "format" in parameter:
            inp.format = str(parameter["format"])

        # dimensions
        if "dimensions" in parameter:
            inp.dimensions = int(parameter["dimensions"])

        # input-type
        if "input-type" in parameter:
            inp.input_type = str(parameter["input-type"])

        # truncate
        if "truncate" in parameter:
            inp.truncate = str(parameter["truncate"])

        input_list.append(inp)

    return input_list


async def parse_task_embedding_to_multimodal_embedding_input(
    request: Union[CallRequest, Request],
) -> List[MultimodalEmbeddingInput]:

    # http test input
    if isinstance(request, Request):
        test_data: dict = await request.json()

        inp = MultimodalEmbeddingInput()
        inp.contents = []
        if "image" in test_data:
            inp.contents.append(
                {"type": "image", "image": url_to_pil_image(test_data["image"])}
            )
        if "text" in test_data:
            inp.contents.append({"type": "text", "text": test_data["text"]})

        return [inp]

    input_list = []
    for task_input in request.task_inputs:
        task_input_dict = json_format.MessageToDict(task_input)

        data = task_input_dict["data"]
        parameter = (
            task_input_dict["parameter"] if "parameter" in task_input_dict else {}
        )

        inp = MultimodalEmbeddingInput()

        contents: List[dict] = []
        for embedding in data["embeddings"]:
            if embedding["type"] == "image-url":
                contents.append(
                    {
                        "type": "image",
                        "image": url_to_pil_image(embedding[embedding["type"]]),
                    }
                )
            elif embedding["type"] == "image-base64":
                contents.append(
                    {
                        "type": "image",
                        "image": base64_to_pil_image(embedding[embedding["type"]]),
                    }
                )
            elif embedding["type"] == "text":
                contents.append({"type": "text", "text": embedding[embedding["type"]]})
            else:
                raise InvalidInputException("non supported input type")

        inp.contents = contents

        # format
        if "format" in parameter:
            inp.format = str(parameter["format"])

        # dimensions
        if "dimensions" in parameter:
            inp.dimensions = int(parameter["dimensions"])

        # input-type
        if "input-type" in parameter:
            inp.input_type = str(parameter["input-type"])

        # truncate
        if "truncate" in parameter:
            inp.truncate = str(parameter["truncate"])

        input_list.append(inp)

    return input_list


def construct_task_embedding_output(
    request: Union[CallRequest, Request],
    indexes: List[List[int]],
    created_timestamps: List[List[int]],
    embeddings: List[List[list]],
) -> Union[CallResponse, List]:

    if not len(embeddings) == len(indexes) == len(created_timestamps):
        raise InvalidOutputShapeException
    if len(embeddings) > 0 and not (
        len(embeddings[0]) == len(indexes[0]) == len(created_timestamps[0])
    ):
        raise InvalidOutputShapeException

    task_outputs = []
    # data
    for index_list, created_timestamp_list, embedding_list in zip(
        indexes, created_timestamps, embeddings
    ):
        data = {}
        embeds = []
        for (
            index,
            created_timestamp,
            embed,
        ) in zip(index_list, created_timestamp_list, embedding_list):
            if isinstance(embed, np.ndarray):
                embed = embed.tolist()
            embeds.append(
                {
                    "index": index,
                    "vector": list(embed),
                    "created": created_timestamp,
                }
            )
        data["embeddings"] = embeds
        task_outputs.append({"data": data})

    if isinstance(request, Request):
        return task_outputs

    for i, o in enumerate(task_outputs):
        task_outputs[i] = dict_to_struct(o)

    return CallResponse(task_outputs=task_outputs)


async def parse_custom_input(
    request: Union[CallRequest, Request],
) -> List[dict]:

    # http test input
    if isinstance(request, Request):
        test_data: dict = await request.json()

        return [test_data]

    input_list = []
    for task_input in request.task_inputs:
        task_input_dict = json_format.MessageToDict(task_input)

        input_list.append(task_input_dict)

    return input_list


def construct_custom_output(
    request: Union[CallRequest, Request], outputs: List[dict]
) -> Union[CallResponse, List]:

    if isinstance(request, Request):
        return outputs

    for i, o in enumerate(outputs):
        outputs[i] = dict_to_struct(o)

    return CallResponse(task_outputs=outputs)
