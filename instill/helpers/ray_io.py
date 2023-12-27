import base64
import io
import json
import struct
from json.decoder import JSONDecodeError
from typing import List

import numpy as np
from PIL import Image

from instill.helpers.const import (
    ImageToImageInput,
    TextGenerationChatInput,
    TextGenerationInput,
    TextToImageInput,
    VisualQuestionAnsweringInput,
)


def serialize_byte_tensor(input_tensor):
    """
    Serializes a bytes tensor into a flat numpy array of length prepended
    bytes. The numpy array should use dtype of np.object_. For np.bytes_,
    numpy will remove trailing zeros at the end of byte sequence and because
    of this it should be avoided.
    Parameters
    ----------
    input_tensor : np.array
        The bytes tensor to serialize.
    Returns
    -------
    serialized_bytes_tensor : np.array
        The 1-D numpy array of type uint8 containing the serialized bytes in 'C' order.
    Raises
    ------
    InferenceServerException
        If unable to serialize the given tensor.
    """

    if input_tensor.size == 0:
        return ()

    # If the input is a tensor of string/bytes objects, then must flatten those
    # into a 1-dimensional array containing the 4-byte byte size followed by the
    # actual element bytes. All elements are concatenated together in "C" order.
    if (input_tensor.dtype == np.object_) or (input_tensor.dtype.type == np.bytes_):
        flattened_ls: list = []
        for obj in np.nditer(input_tensor, flags=["refs_ok"], order="C"):
            # If directly passing bytes to BYTES type,
            # don't convert it to str as Python will encode the
            # bytes which may distort the meaning
            assert isinstance(obj, np.ndarray)
            if input_tensor.dtype == np.object_:
                if isinstance(obj.item(), bytes):
                    s = obj.item()
                else:
                    s = str(obj.item()).encode("utf-8")
            else:
                s = obj.item()
            flattened_ls.append(struct.pack("<I", len(s)))
            flattened_ls.append(s)
        flattened = b"".join(flattened_ls)
        return flattened
    return None


def deserialize_bytes_tensor(encoded_tensor):
    """
    Deserializes an encoded bytes tensor into an
    numpy array of dtype of python objects

    Parameters
    ----------
    encoded_tensor : bytes
        The encoded bytes tensor where each element
        has its length in first 4 bytes followed by
        the content
    Returns
    -------
    string_tensor : np.array
        The 1-D numpy array of type object containing the
        deserialized bytes in 'C' order.

    """
    strs = []
    offset = 0
    val_buf = encoded_tensor
    while offset < len(val_buf):
        l = struct.unpack_from("<I", val_buf, offset)[0]
        offset += 4
        sb = struct.unpack_from(f"<{l}s", val_buf, offset)[0]
        offset += l
        strs.append(sb)
    return np.array(strs, dtype=bytes)


class StandardTaskIO:
    @staticmethod
    def parse_task_text_generation_input(request) -> TextGenerationInput:
        text_generation_input = TextGenerationInput()

        for i, b_input_tensor in zip(request.inputs, request.raw_input_contents):
            input_name = i.name

            if input_name == "prompt":
                input_tensor = deserialize_bytes_tensor(b_input_tensor)
                text_generation_input.prompt = str(input_tensor[0].decode("utf-8"))
                print(
                    f"[DEBUG] input `prompt` type\
                        ({type(text_generation_input.prompt)}): {text_generation_input.prompt}"
                )

            if input_name == "prompt_images":
                input_tensors = deserialize_bytes_tensor(b_input_tensor)
                images = []
                for enc in input_tensors:
                    if len(enc) == 0:
                        continue
                    try:
                        enc_json = json.loads(str(enc.decode("utf-8")))
                        if len(enc_json) == 0:
                            continue
                        decoded_enc = enc_json[0]
                    except JSONDecodeError:
                        print("[DEBUG] WARNING `enc_json` parsing faield!")
                    # pil_img = Image.open(io.BytesIO(enc.astype(bytes)))  # RGB
                    pil_img = Image.open(io.BytesIO(base64.b64decode(decoded_enc)))

                    image = np.array(pil_img)
                    if len(image.shape) == 2:  # gray image
                        raise ValueError(
                            f"The image shape with {image.shape} is "
                            f"not in acceptable"
                        )
                    images.append(image)
                # TODO: check wethere there are issues in batch size dimention
                text_generation_input.prompt_images = images
                print(
                    "[DEBUG] input `prompt_images` type"
                    f"({type(text_generation_input.prompt_images)}): "
                    f"{text_generation_input.prompt_images}"
                )

            if input_name == "chat_history":
                input_tensor = deserialize_bytes_tensor(b_input_tensor)
                chat_history_str = str(input_tensor[0].decode("utf-8"))
                print(
                    "[DEBUG] input `chat_history_str` type"
                    f"({type(chat_history_str)}): "
                    f"{chat_history_str}"
                )
                try:
                    text_generation_input.chat_history = json.loads(chat_history_str)
                except JSONDecodeError:
                    print("[DEBUG] WARNING `extra_params` parsing faield!")
                    continue

            if input_name == "system_message":
                input_tensor = deserialize_bytes_tensor(b_input_tensor)
                text_generation_input.system_message = str(
                    input_tensor[0].decode("utf-8")
                )
                print(
                    "[DEBUG] input `system_message` type"
                    f"({type(text_generation_input.system_message)}): "
                    f"{text_generation_input.system_message}"
                )

            if input_name == "max_new_tokens":
                text_generation_input.max_new_tokens = int.from_bytes(
                    b_input_tensor, "little"
                )
                print(
                    "[DEBUG] input `max_new_tokens` type"
                    f"({type(text_generation_input.max_new_tokens)}): "
                    f"{text_generation_input.max_new_tokens}"
                )

            if input_name == "top_k":
                text_generation_input.top_k = int.from_bytes(b_input_tensor, "little")
                print(
                    "[DEBUG] input `top_k` type"
                    f"({type(text_generation_input.top_k)}): "
                    f"{text_generation_input.top_k}"
                )

            if input_name == "temperature":
                text_generation_input.temperature = struct.unpack("f", b_input_tensor)[
                    0
                ]
                print(
                    "[DEBUG] input `temperature` type"
                    f"({type(text_generation_input.temperature)}): "
                    f"{text_generation_input.temperature}"
                )
                text_generation_input.temperature = round(
                    text_generation_input.temperature, 2
                )

            if input_name == "random_seed":
                text_generation_input.random_seed = int.from_bytes(
                    b_input_tensor, "little"
                )
                print(
                    "[DEBUG] input `random_seed` type"
                    f"({type(text_generation_input.random_seed)}): "
                    f"{text_generation_input.random_seed}"
                )

            if input_name == "extra_params":
                input_tensor = deserialize_bytes_tensor(b_input_tensor)
                extra_params_str = str(input_tensor[0].decode("utf-8"))
                print(
                    "[DEBUG] input `extra_params` type"
                    f"({type(extra_params_str)}): "
                    f"{extra_params_str}"
                )

                try:
                    text_generation_input.extra_params = json.loads(extra_params_str)
                except JSONDecodeError:
                    print("[DEBUG] WARNING `extra_params` parsing faield!")
                    continue

        return text_generation_input

    @staticmethod
    def parse_task_text_generation_output(sequences: list):
        text_outputs = [seq["generated_text"].encode("utf-8") for seq in sequences]

        return serialize_byte_tensor(np.asarray(text_outputs))

    @staticmethod
    def parse_task_text_to_image_input(request) -> TextToImageInput:
        text_to_image_input = TextToImageInput()

        for i, b_input_tensor in zip(request.inputs, request.raw_input_contents):
            input_name = i.name

            if input_name == "prompt":
                input_tensor = deserialize_bytes_tensor(b_input_tensor)
                text_to_image_input.prompt = str(input_tensor[0].decode("utf-8"))
                print(
                    f"[DEBUG] input `prompt` type\
                        ({type(text_to_image_input.prompt)}): {text_to_image_input.prompt}"
                )

            if input_name == "negative_prompt":
                input_tensor = deserialize_bytes_tensor(b_input_tensor)
                text_to_image_input.negative_prompt = str(
                    input_tensor[0].decode("utf-8")
                )
                print(
                    f"[DEBUG] input `negative_prompt` type\
                        ({type(text_to_image_input.negative_prompt)}): {text_to_image_input.negative_prompt}"
                )

            if input_name == "steps":
                text_to_image_input.steps = int.from_bytes(b_input_tensor, "little")
                print(
                    f"[DEBUG] input `steps` type\
                        ({type(text_to_image_input.steps)}): {text_to_image_input.steps}"
                )

            if input_name == "seed":
                text_to_image_input.seed = int.from_bytes(b_input_tensor, "little")
                print(
                    f"[DEBUG] input `seed` type\
                        ({type(text_to_image_input.seed)}): {text_to_image_input.seed}"
                )

            if input_name == "guidance_scale":
                text_to_image_input.guidance_scale = struct.unpack("f", b_input_tensor)[
                    0
                ]
                print(
                    f"[DEBUG] input `guidance_scale` type\
                        ({type(text_to_image_input.guidance_scale)}): {text_to_image_input.guidance_scale}"
                )
                text_to_image_input.guidance_scale = round(
                    text_to_image_input.guidance_scale, 2
                )

            if input_name == "samples":
                text_to_image_input.samples = int.from_bytes(b_input_tensor, "little")
                print(
                    f"[DEBUG] input `samples` type\
                        ({type(text_to_image_input.samples)}): {text_to_image_input.samples}"
                )

            if input_name == "extra_params":
                input_tensor = deserialize_bytes_tensor(b_input_tensor)
                extra_params_str = str(input_tensor[0].decode("utf-8"))
                print(
                    f"[DEBUG] input `extra_params` type\
                        ({type(extra_params_str)}): {extra_params_str}"
                )

                try:
                    text_to_image_input.extra_params = json.loads(extra_params_str)
                except JSONDecodeError:
                    print("[DEBUG] WARNING `extra_params` parsing faield!")
                    continue

        return text_to_image_input

    @staticmethod
    def parse_task_text_to_image_output(image):
        return np.asarray(image).tobytes()

    @staticmethod
    def parse_task_image_to_image_input(request) -> ImageToImageInput:
        image_to_image_input = ImageToImageInput()

        for i, b_input_tensor in zip(request.inputs, request.raw_input_contents):
            input_name = i.name

            if input_name == "prompt_image":
                input_tensors = deserialize_bytes_tensor(b_input_tensor)
                images = []
                for enc in input_tensors:
                    pil_img = Image.open(io.BytesIO(enc.astype(bytes)))  # RGB
                    image = np.array(pil_img)
                    if len(image.shape) == 2:  # gray image
                        raise ValueError(
                            f"The image shape with {image.shape} is "
                            f"not in acceptable"
                        )
                    images.append(image)
                image_to_image_input.prompt_image = images[0]
                print(
                    f"[DEBUG] input `prompt_image` type\
                        ({type(image_to_image_input.prompt_image)}): {image_to_image_input.prompt_image}"
                )

            if input_name == "prompt":
                input_tensor = deserialize_bytes_tensor(b_input_tensor)
                image_to_image_input.prompt = str(input_tensor[0].decode("utf-8"))
                print(
                    f"[DEBUG] input `prompt` type\
                        ({type(image_to_image_input.prompt)}): {image_to_image_input.prompt}"
                )

            if input_name == "steps":
                image_to_image_input.steps = int.from_bytes(b_input_tensor, "little")
                print(
                    f"[DEBUG] input `steps` type\
                        ({type(image_to_image_input.steps)}): {image_to_image_input.steps}"
                )

            if input_name == "seed":
                image_to_image_input.seed = int.from_bytes(b_input_tensor, "little")
                print(
                    f"[DEBUG] input `seed` type\
                        ({type(image_to_image_input.seed)}): {image_to_image_input.seed}"
                )

            if input_name == "guidance_scale":
                image_to_image_input.guidance_scale = struct.unpack(
                    "f", b_input_tensor
                )[0]
                print(
                    f"[DEBUG] input `guidance_scale` type\
                        ({type(image_to_image_input.guidance_scale)}): {image_to_image_input.guidance_scale}"
                )
                image_to_image_input.guidance_scale = round(
                    image_to_image_input.guidance_scale, 2
                )

            if input_name == "samples":
                image_to_image_input.samples = int.from_bytes(b_input_tensor, "little")
                print(
                    f"[DEBUG] input `samples` type\
                        ({type(image_to_image_input.samples)}): {image_to_image_input.samples}"
                )

            if input_name == "extra_params":
                input_tensor = deserialize_bytes_tensor(b_input_tensor)
                extra_params_str = str(input_tensor[0].decode("utf-8"))
                print(
                    f"[DEBUG] input `extra_params` type\
                        ({type(extra_params_str)}): {extra_params_str}"
                )

                try:
                    image_to_image_input.extra_params = json.loads(extra_params_str)
                except JSONDecodeError:
                    print("[DEBUG] WARNING `extra_params` parsing faield!")
                    continue

        return image_to_image_input

    @staticmethod
    def parse_task_image_to_image_output(image):
        return np.asarray(image).tobytes()

    @staticmethod
    def parse_task_text_generation_chat_input(request) -> TextGenerationChatInput:
        text_generation_chat_input = TextGenerationChatInput()

        for i, b_input_tensor in zip(request.inputs, request.raw_input_contents):
            input_name = i.name

            if input_name == "prompt":
                input_tensor = deserialize_bytes_tensor(b_input_tensor)
                text_generation_chat_input.prompt = str(input_tensor[0].decode("utf-8"))
                print(
                    f"[DEBUG] input `prompt` type\
                        ({type(text_generation_chat_input.prompt)}): {text_generation_chat_input.prompt}"
                )

            if input_name == "prompt_images":
                input_tensors = deserialize_bytes_tensor(b_input_tensor)
                images = []
                for enc in input_tensors:
                    if len(enc) == 0:
                        continue
                    try:
                        enc_json = json.loads(str(enc.decode("utf-8")))
                        if len(enc_json) == 0:
                            continue
                        decoded_enc = enc_json[0]
                    except JSONDecodeError:
                        print("[DEBUG] WARNING `enc_json` parsing faield!")
                    # pil_img = Image.open(io.BytesIO(enc.astype(bytes)))  # RGB
                    pil_img = Image.open(io.BytesIO(base64.b64decode(decoded_enc)))

                    image = np.array(pil_img)
                    if len(image.shape) == 2:  # gray image
                        raise ValueError(
                            f"The image shape with {image.shape} is "
                            f"not in acceptable"
                        )
                    images.append(image)
                text_generation_chat_input.prompt_images = images
                print(
                    "[DEBUG] input `prompt_images` type"
                    f"({type(text_generation_chat_input.prompt_images)}): "
                    f"{text_generation_chat_input.prompt_images}"
                )

            if input_name == "chat_history":
                input_tensor = deserialize_bytes_tensor(b_input_tensor)
                chat_history_str = str(input_tensor[0].decode("utf-8"))
                print(
                    "[DEBUG] input `chat_history_str` type"
                    f"({type(chat_history_str)}): "
                    f"{chat_history_str}"
                )
                try:
                    text_generation_chat_input.chat_history = json.loads(
                        chat_history_str
                    )
                except JSONDecodeError:
                    print("[DEBUG] WARNING `extra_params` parsing faield!")
                    continue

            if input_name == "system_message":
                input_tensor = deserialize_bytes_tensor(b_input_tensor)
                text_generation_chat_input.system_message = str(
                    input_tensor[0].decode("utf-8")
                )
                print(
                    "[DEBUG] input `system_message` type"
                    f"({type(text_generation_chat_input.system_message)}): "
                    f"{text_generation_chat_input.system_message}"
                )

            if input_name == "max_new_tokens":
                text_generation_chat_input.max_new_tokens = int.from_bytes(
                    b_input_tensor, "little"
                )
                print(
                    "[DEBUG] input `max_new_tokens` type"
                    f"({type(text_generation_chat_input.max_new_tokens)}): "
                    f"{text_generation_chat_input.max_new_tokens}"
                )

            if input_name == "top_k":
                text_generation_chat_input.top_k = int.from_bytes(
                    b_input_tensor, "little"
                )
                print(
                    "[DEBUG] input `top_k` type"
                    f"({type(text_generation_chat_input.top_k)}): "
                    f"{text_generation_chat_input.top_k}"
                )

            if input_name == "temperature":
                text_generation_chat_input.temperature = struct.unpack(
                    "f", b_input_tensor
                )[0]
                print(
                    "[DEBUG] input `temperature` type"
                    f"({type(text_generation_chat_input.temperature)}): "
                    f"{text_generation_chat_input.temperature}"
                )
                text_generation_chat_input.temperature = round(
                    text_generation_chat_input.temperature, 2
                )

            if input_name == "random_seed":
                text_generation_chat_input.random_seed = int.from_bytes(
                    b_input_tensor, "little"
                )
                print(
                    "[DEBUG] input `random_seed` type"
                    f"({type(text_generation_chat_input.random_seed)}): "
                    f"{text_generation_chat_input.random_seed}"
                )

            if input_name == "extra_params":
                input_tensor = deserialize_bytes_tensor(b_input_tensor)
                extra_params_str = str(input_tensor[0].decode("utf-8"))
                print(
                    "[DEBUG] input `extra_params` type"
                    f"({type(extra_params_str)}): "
                    f"{extra_params_str}"
                )

                try:
                    text_generation_chat_input.extra_params = json.loads(
                        extra_params_str
                    )
                except JSONDecodeError:
                    print("[DEBUG] WARNING `extra_params` parsing faield!")
                    continue

        return text_generation_chat_input

    @staticmethod
    def parse_task_text_generation_chat_output(sequences: list):
        text_outputs = [seq["generated_text"].encode("utf-8") for seq in sequences]

        return serialize_byte_tensor(np.asarray(text_outputs))

    @staticmethod
    def parse_task_visual_question_answering_input(
        request,
    ) -> VisualQuestionAnsweringInput:
        text_visual_question_answering_input = VisualQuestionAnsweringInput()

        for i, b_input_tensor in zip(request.inputs, request.raw_input_contents):
            input_name = i.name

            if input_name == "prompt":
                input_tensor = deserialize_bytes_tensor(b_input_tensor)
                text_visual_question_answering_input.prompt = str(
                    input_tensor[0].decode("utf-8")
                )
                print(
                    "[DEBUG] input `prompt` type"
                    f"({type(text_visual_question_answering_input.prompt)}): "
                    f"{text_visual_question_answering_input.prompt}"
                )

            if input_name == "prompt_images":
                input_tensors = deserialize_bytes_tensor(b_input_tensor)
                images = []
                for enc in input_tensors:
                    if len(enc) == 0:
                        continue
                    try:
                        enc_json = json.loads(str(enc.decode("utf-8")))
                        if len(enc_json) == 0:
                            continue
                        decoded_enc = enc_json[0]
                    except JSONDecodeError:
                        print("[DEBUG] WARNING `enc_json` parsing faield!")
                    # pil_img = Image.open(io.BytesIO(enc.astype(bytes)))  # RGB
                    pil_img = Image.open(io.BytesIO(base64.b64decode(decoded_enc)))

                    image = np.array(pil_img)
                    if len(image.shape) == 2:  # gray image
                        raise ValueError(
                            f"The image shape with {image.shape} is "
                            f"not in acceptable"
                        )
                    images.append(image)
                # TODO: check wethere there are issues in batch size dimention
                text_visual_question_answering_input.prompt_images = images
                print(
                    "[DEBUG] input `prompt_images` type"
                    f"({type(text_visual_question_answering_input.prompt_images)}): "
                    f"{text_visual_question_answering_input.prompt_images}"
                )

            if input_name == "chat_history":
                input_tensor = deserialize_bytes_tensor(b_input_tensor)
                chat_history_str = str(input_tensor[0].decode("utf-8"))
                print(
                    "[DEBUG] input `chat_history_str` type"
                    f"({type(chat_history_str)}): "
                    f"{chat_history_str}"
                )
                try:
                    text_visual_question_answering_input.chat_history = json.loads(
                        chat_history_str
                    )
                except JSONDecodeError:
                    print("[DEBUG] WARNING `extra_params` parsing faield!")
                    continue

            if input_name == "system_message":
                input_tensor = deserialize_bytes_tensor(b_input_tensor)
                text_visual_question_answering_input.system_message = str(
                    input_tensor[0].decode("utf-8")
                )
                print(
                    "[DEBUG] input `system_message` type"
                    f"({type(text_visual_question_answering_input.system_message)}): "
                    f"{text_visual_question_answering_input.system_message}"
                )

            if input_name == "max_new_tokens":
                text_visual_question_answering_input.max_new_tokens = int.from_bytes(
                    b_input_tensor, "little"
                )
                print(
                    "[DEBUG] input `max_new_tokens` type"
                    f"({type(text_visual_question_answering_input.max_new_tokens)}): "
                    f"{text_visual_question_answering_input.max_new_tokens}"
                )

            if input_name == "top_k":
                text_visual_question_answering_input.top_k = int.from_bytes(
                    b_input_tensor, "little"
                )
                print(
                    "[DEBUG] input `top_k` type"
                    f"({type(text_visual_question_answering_input.top_k)}): "
                    f"{text_visual_question_answering_input.top_k}"
                )

            if input_name == "temperature":
                text_visual_question_answering_input.temperature = struct.unpack(
                    "f", b_input_tensor
                )[0]
                print(
                    "[DEBUG] input `temperature` type"
                    f"({type(text_visual_question_answering_input.temperature)}): "
                    f"{text_visual_question_answering_input.temperature}"
                )
                text_visual_question_answering_input.temperature = round(
                    text_visual_question_answering_input.temperature, 2
                )

            if input_name == "random_seed":
                text_visual_question_answering_input.random_seed = int.from_bytes(
                    b_input_tensor, "little"
                )
                print(
                    "[DEBUG] input `random_seed` type"
                    f"({type(text_visual_question_answering_input.random_seed)}): "
                    f"{text_visual_question_answering_input.random_seed}"
                )

            if input_name == "extra_params":
                input_tensor = deserialize_bytes_tensor(b_input_tensor)
                extra_params_str = str(input_tensor[0].decode("utf-8"))
                print(
                    "[DEBUG] input `extra_params` type"
                    f"({type(extra_params_str)}): "
                    f"{extra_params_str}"
                )

                try:
                    text_visual_question_answering_input.extra_params = json.loads(
                        extra_params_str
                    )
                except JSONDecodeError:
                    print("[DEBUG] WARNING `extra_params` parsing faield!")
                    continue

        return text_visual_question_answering_input

    @staticmethod
    def parse_task_visual_question_answering_output(sequences: list):
        text_outputs = [seq["generated_text"].encode("utf-8") for seq in sequences]

        return serialize_byte_tensor(np.asarray(text_outputs))


class RawIO:
    @staticmethod
    def parse_byte_tensor(byte_tensor) -> List[str]:
        input_tensors = deserialize_bytes_tensor(byte_tensor)
        outs = [str(tensor.decode("utf-8")) for tensor in input_tensors]

        return outs

    @staticmethod
    def parse_unsigned_int_tensor(int_tensor) -> int:
        return int.from_bytes(int_tensor, "little")

    @staticmethod
    def parse_signed_int_tensor(int_tensor) -> int:
        return int.from_bytes(int_tensor, "little", signed=True)

    @staticmethod
    def parse_float_tensor(float_tensor) -> float:
        return struct.unpack("f", float_tensor)[0]

    @staticmethod
    def parse_boolean_tensor(bool_tensor) -> bool:
        return struct.unpack("?", bool_tensor)[0]
