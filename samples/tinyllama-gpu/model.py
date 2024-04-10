import numpy as np
import random
import torch
from transformers import pipeline

from instill.helpers.const import DataType, TextGenerationChatInput
from instill.helpers.ray_io import StandardTaskIO
from instill.helpers.ray_config import instill_deployment, InstillDeployable
from instill.helpers import (
    construct_infer_response,
    construct_metadata_response,
    Metadata,
)


@instill_deployment
class TinyLlama:
    def __init__(self):
        self.pipeline = pipeline(
            "text-generation",
            model="tinyllama",
            torch_dtype=torch.float16,
            device_map="cuda",
        )

    def ModelMetadata(self, req):
        resp = construct_metadata_response(
            req=req,
            inputs=[
                Metadata(
                    name="prompt",
                    datatype=str(DataType.TYPE_STRING.name),
                    shape=[1],
                ),
                Metadata(
                    name="prompt_images",
                    datatype=str(DataType.TYPE_STRING.name),
                    shape=[1],
                ),
                Metadata(
                    name="chat_history",
                    datatype=str(DataType.TYPE_STRING.name),
                    shape=[1],
                ),
                Metadata(
                    name="system_message",
                    datatype=str(DataType.TYPE_STRING.name),
                    shape=[1],
                ),
                Metadata(
                    name="max_new_tokens",
                    datatype=str(DataType.TYPE_UINT32.name),
                    shape=[1],
                ),
                Metadata(
                    name="temperature",
                    datatype=str(DataType.TYPE_FP32.name),
                    shape=[1],
                ),
                Metadata(
                    name="top_k",
                    datatype=str(DataType.TYPE_UINT32.name),
                    shape=[1],
                ),
                Metadata(
                    name="seed",
                    datatype=str(DataType.TYPE_UINT64.name),
                    shape=[1],
                ),
                Metadata(
                    name="extra_params",
                    datatype=str(DataType.TYPE_STRING.name),
                    shape=[1],
                ),
            ],
            outputs=[
                Metadata(
                    name="text",
                    datatype=str(DataType.TYPE_STRING.name),
                    shape=[-1, -1],
                ),
            ],
        )
        return resp

    async def __call__(self, request):
        resp_outputs = []
        resp_raw_outputs = []

        task_text_generation_chat_input: TextGenerationChatInput = (
            StandardTaskIO.parse_task_text_generation_chat_input(request=request)
        )

        if task_text_generation_chat_input.random_seed > 0:
            random.seed(task_text_generation_chat_input.random_seed)
            np.random.seed(task_text_generation_chat_input.random_seed)
            torch.manual_seed(task_text_generation_chat_input.random_seed)
            if torch.cuda.is_available():
                torch.cuda.manual_seed_all(task_text_generation_chat_input.random_seed)

        conv = [
            {
                "role": "system",
                "content": "You are a friendly chatbot",
            },
            {
                "role": "user",
                "content": task_text_generation_chat_input.prompt,
            },
        ]

        prompt = self.pipeline.tokenizer.apply_chat_template(
            conv,
            tokenize=False,
            add_generation_prompt=True,
        )

        sequences = self.pipeline(
            prompt,
            max_new_tokens=task_text_generation_chat_input.max_new_tokens,
            do_sample=True,
            temperature=task_text_generation_chat_input.temperature,
            top_k=task_text_generation_chat_input.top_k,
            top_p=0.95,
        )

        task_text_generation_chat_output = (
            StandardTaskIO.parse_task_text_generation_chat_output(sequences=sequences)
        )

        resp_outputs.append(
            Metadata(
                name="text",
                shape=[1, len(sequences)],
                datatype=str(DataType.TYPE_STRING),
            )
        )

        resp_raw_outputs.append(task_text_generation_chat_output)

        return construct_infer_response(
            req=request,
            outputs=resp_outputs,
            raw_outputs=resp_raw_outputs,
        )


entrypoint = (
    InstillDeployable(TinyLlama)
    .get_deployment_handle()
)
