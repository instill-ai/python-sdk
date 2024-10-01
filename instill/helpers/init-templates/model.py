# type: ignore
# you can find a list of supported task in the helpers module
from instill.helpers import (
    construct_task_chat_output,
    parse_task_chat_to_multimodal_chat_input,
)
from instill.helpers.ray_config import InstillDeployable, instill_deployment


@instill_deployment
class ModelName:
    """Custom model implementation"""

    def __init__(self):
        """Load model into memory"""
        # self.pipeline = pipeline(
        #     "text-generation",
        #     model="tinyllama",
        #     torch_dtype=torch.float16,
        #     device_map="cuda:0",
        # )

    async def __call__(self, request):
        """Run inference logic"""

        # parse request into conversation chat input

        # conversation_inputs = await parse_task_chat_to_chat_input(request=request)

        # finish_reasons = []
        # indexes = []
        # created = []
        # messages = []
        # for i, inp in enumerate(conversation_inputs):
        #     prompt = self.pipeline.tokenizer.apply_chat_template(
        #         inp.messages,
        #         tokenize=False,
        #         add_generation_prompt=True,
        #     )

        #     # inference
        #     sequences = self.pipeline(
        #         prompt,
        #         max_new_tokens=inp.max_tokens,
        #         do_sample=True,
        #         temperature=inp.temperature,
        #         top_p=inp.top_p,
        #     )

        #     output = sequences[0]["generated_text"].split("<|assistant|>\n")[-1].strip()

        #     messages.append([{"content": output, "role": "assistant"}])
        #     finish_reasons.append(["length"])
        #     indexes.append([i])
        #     created.append([int(time.time())])

        # construct chat output

        # return construct_task_chat_output(
        #     request=request,
        #     finish_reasons=finish_reasons,
        #     indexes=indexes,
        #     messages=messages,
        #     created_timestamps=created,
        # )


# define model deployment entrypoint
entrypoint = InstillDeployable(ModelName).get_deployment_handle()
