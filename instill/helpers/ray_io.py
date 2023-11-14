import json
import struct
from typing import List

import numpy as np
from const import TextGenerationInput


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
        sb = struct.unpack_from("<{}s".format(l), val_buf, offset)[0]
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
                    f"[DEBUG] input `prompt` type({type(text_generation_input.prompt)}): {text_generation_input.prompt}"
                )

            if input_name == "max_new_tokens":
                text_generation_inputmax_new_tokens = int.from_bytes(
                    b_input_tensor, "little"
                )
                print(
                    f"[DEBUG] input `max_new_tokens` type({type(text_generation_inputmax_new_tokens)}): {text_generation_inputmax_new_tokens}"
                )

            if input_name == "top_k":
                text_generation_input.top_k = int.from_bytes(b_input_tensor, "little")
                print(
                    f"[DEBUG] input `top_k` type({type(text_generation_input.top_k)}): {text_generation_input.top_k}"
                )

            if input_name == "temperature":
                text_generation_input.temperature = struct.unpack("f", b_input_tensor)[
                    0
                ]
                print(
                    f"[DEBUG] input `temperature` type({type(text_generation_input.temperature)}): {text_generation_input.temperature}"
                )
                temperature: float = round(temperature, 2)

            if input_name == "random_seed":
                text_generation_input.random_seed = int.from_bytes(
                    b_input_tensor, "little"
                )
                print(
                    f"[DEBUG] input `random_seed` type({type(text_generation_input.random_seed)}): {text_generation_input.random_seed}"
                )

            if input_name == "stop_words":
                input_tensor = deserialize_bytes_tensor(b_input_tensor)
                text_generation_input.stop_words = input_tensor[0]
                print(
                    f"[DEBUG] input `stop_words` type({type(text_generation_input.stop_words)}): {text_generation_input.stop_words}"
                )
                if len(text_generation_input.stop_words) == 0:
                    text_generation_input.stop_words = None
                elif text_generation_input.stop_words.shape[0] > 1:
                    # TODO: Check wether shoule we decode this words
                    text_generation_input.stop_words = list(
                        text_generation_input.stop_words
                    )
                else:
                    text_generation_input.stop_words = [
                        str(text_generation_input.stop_words[0])
                    ]
                print(
                    f"[DEBUG] parsed input `stop_words` type({type(text_generation_input.stop_words)}): {text_generation_input.stop_words}"
                )

            if input_name == "extra_params":
                input_tensor = deserialize_bytes_tensor(b_input_tensor)
                extra_params_str = str(input_tensor[0].decode("utf-8"))
                print(
                    f"[DEBUG] input `extra_params` type({type(extra_params_str)}): {extra_params_str}"
                )

                try:
                    text_generation_input.extra_params = json.loads(extra_params_str)
                except json.decoder.JSONDecodeError:
                    print("[DEBUG] WARNING `extra_params` parsing faield!")
                    continue

        return text_generation_input

    @staticmethod
    def parse_task_text_generation_output(sequences: list):
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
