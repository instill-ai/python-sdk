# pylint: disable=no-member,wrong-import-position
from typing import Union

from instill.resources import Component
from instill.resources.schema import (
    base64_task_decode_input,
    base64_task_encode_input,
    helper,
    image_task_draw_classification_input,
    image_task_draw_detection_input,
    image_task_draw_instance_segmentation_input,
    image_task_draw_keypoint_input,
    image_task_draw_ocr_input,
    image_task_draw_semantic_segmentation_input,
    json_task_marshal_input,
    json_task_unmarshal_input,
    text_task_convert_to_text_input,
    text_task_split_by_token_input,
)


class Base64Operator(Component):
    """Base64 Operator"""

    def __init__(
        self,
        name: str,
        inp: Union[
            base64_task_encode_input.Input,
            base64_task_decode_input.Input,
        ],
    ) -> None:
        definition_name = "operator-definitions/base64"
        component_type = "operator"

        component = helper.construct_component_config(
            component_type, definition_name, inp
        )

        super().__init__(name, component)


class JSONOperator(Component):
    """JSON Operator"""

    def __init__(
        self,
        name: str,
        inp: Union[
            json_task_marshal_input.Input,
            json_task_unmarshal_input.Input,
        ],
    ) -> None:
        definition_name = "operator-definitions/json"
        component_type = "operator"

        component = helper.construct_component_config(
            component_type, definition_name, inp
        )

        super().__init__(name, component)


class ImageOperator(Component):
    """Image Operator"""

    def __init__(
        self,
        name: str,
        inp: Union[
            image_task_draw_classification_input.Input,
            image_task_draw_detection_input.Input,
            image_task_draw_instance_segmentation_input.Input,
            image_task_draw_semantic_segmentation_input.Input,
            image_task_draw_keypoint_input.Input,
            image_task_draw_ocr_input.Input,
        ],
    ) -> None:
        definition_name = "operator-definitions/image"
        component_type = "operator"

        component = helper.construct_component_config(
            component_type, definition_name, inp
        )

        super().__init__(name, component)


class TextOperator(Component):
    """Text Operator"""

    def __init__(
        self,
        name: str,
        inp: Union[
            text_task_convert_to_text_input.Input,
            text_task_split_by_token_input.Input,
        ],
    ) -> None:
        definition_name = "operator-definitions/text"
        component_type = "operator"

        component = helper.construct_component_config(
            component_type, definition_name, inp
        )

        super().__init__(name, component)
