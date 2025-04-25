from llama_cpp import Llama
from .mcp_client import mcp_client
import os
from .base_llm import BaseLLm, llm_logger
from .model_downloader import ModelDownloader
from src.enviroments import HUGGING_FACE_ID, HUGGING_FACE_TOKEN, MODEL_PATH


class LocalModel(BaseLLm):
    def __init__(self, path_to_model: str, tool_list: list):
        super().__init__(path_to_model, tool_list)

        if not os.path.isfile(os.path.join(os.path.dirname(__file__), path_to_model)):
            llm_logger.warning('Model not found. Trying to get from hugging face.')
            try:
                ModelDownloader.get_model(HUGGING_FACE_ID,
                                          HUGGING_FACE_TOKEN,
                                          os.path.join(os.path.dirname(__file__), MODEL_PATH))
            finally:
                llm_logger.critical('Unable to download model.')
                raise ValueError('Invalid model_id, model_path or hugging face token')

        self.model = Llama(
            model_path=os.path.join(os.path.dirname(__file__), path_to_model),
            chat_format="chatml-function-calling",
            n_threads=12,
            n_ctx=16384,
            n_gpu_layers=-1
        )

    def infer(self, system_prompt: str, user_prompt: str, tools_on: bool, tool_choice: dict):
        messages = [
            {'role': 'system', 'content': system_prompt},
            {'role': 'user', 'content': user_prompt}
        ]
        return self.model.create_chat_completion(messages=messages, tools=self.tools if tools_on else None,
                                                 tool_choice=tool_choice if tools_on else None,
                                                 max_tokens=8192)

    def reset(self):
        self.model.reset()
