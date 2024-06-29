# type: ignore
from instill.helpers import (
    construct_text_generation_chat_infer_response,
    construct_text_generation_chat_metadata_response,
)
from instill.helpers.const import TextGenerationChatInput
from instill.helpers.ray_config import InstillDeployable, instill_deployment
from instill.helpers.ray_io import StandardTaskIO


@instill_deployment
class Phimini:
    """Custom model implementation"""

    def __init__(self):
        """Load model into memory"""
        # model = AutoModelForCausalLM.from_pretrained(
        #     "microsoft/Phi-3-mini-4k-instruct",
        #     device_map="cuda",
        #     torch_dtype="auto",
        #     trust_remote_code=True,
        # )
        # tokenizer = AutoTokenizer.from_pretrained("microsoft/Phi-3-mini-4k-instruct")

        # self.pipeline = pipeline(
        #     "text-generation",
        #     model=model,
        #     tokenizer=tokenizer,
        # )

    def ModelMetadata(self, req):
        """Define model input and output shape base on task type"""
        # return construct_text_generation_chat_metadata_response(req=req)

    async def __call__(self, request):
        """Run inference logic"""

        # deserialize input base on task type
        # task_text_generation_chat_input: TextGenerationChatInput = (
        #     StandardTaskIO.parse_task_text_generation_chat_input(request=request)
        # )

        # preprocess
        # conv = [
        #     {
        #         "role": "system",
        #         "content": task_text_generation_chat_input.system_message,
        #     },
        #     {
        #         "role": "user",
        #         "content": task_text_generation_chat_input.prompt,
        #     },
        # ]
        # generation_args = {
        #     "max_new_tokens": task_text_generation_chat_input.max_new_tokens,
        #     "return_full_text": False,
        #     "temperature": task_text_generation_chat_input.temperature,
        #     "top_k": task_text_generation_chat_input.top_k,
        #     "top_p": 0.95,
        #     "do_sample": False,
        # }

        # inference
        # sequences = self.pipeline(conv, **generation_args)

        # convert the model output into response output using StandardTaskIO
        # task_text_generation_chat_output = (
        #     StandardTaskIO.parse_task_text_generation_chat_output(sequences=sequences)
        # )

        # return response
        # return construct_text_generation_chat_infer_response(
        #     req=request,
        #     # specify the output dimension
        #     shape=[1, len(sequences)],
        #     raw_outputs=[task_text_generation_chat_output],
        # )


# define model deployment entrypoint
entrypoint = InstillDeployable(Phimini).get_deployment_handle()
