from openai import OpenAI
from .base_llm import BaseLLm


class OpenRouter(BaseLLm):
    def __init__(self, api_key: str, model_name: str, tool_list: list):
        super().__init__(model_name, tool_list)
        self.llm = OpenAI(
            base_url='https://openrouter.ai/api/v1',
            api_key=api_key
        )
        self.model = model_name

    def infer(self, system_prompt: str, user_prompt: str, tools_on: bool, tool_choice: dict):
        messages = [
            {'role': 'system', 'content': system_prompt},
            {'role': 'user', 'content': user_prompt}
        ]
        return self.llm.chat.completions.create(model=self.model, messages=messages,
                                                tools=self.tools if tools_on else None,
                                                tool_choice=tool_choice if tools_on else None,
                                                max_tokens=96000,
                                                extra_body={'transforms': ['middle-out']}
                                                ).model_dump()

    def reset(self):
        pass


# OPENROUTER_MODEL = 'deepseek/deepseek-r1-zero:free'
#
# with open('open_router_key', 'r') as file:
#     OPENROUTER_KEY = file.readline()
#
# llm = OpenRouter(OPENROUTER_KEY, OPENROUTER_MODEL, [])
# response = llm.infer('You are a helpful AI assistant',
#           'Do you know any popular AI agents for prompt-based site creation or modification?',
#           False,
#           {})
# print(response.choices[0].message.content)
# response = llm.infer('You are a helpful AI assistant',
#           'Which of them is free to use?',
#           False,
#           {})
# print(response.choices[0].message.content)
# llm = OpenAI(
#     base_url='https://openrouter.ai/api/v1',
#     api_key=''
# )
#
# response = llm.chat.completions.create(
#     model='deepseek/deepseek-r1-zero:free',
#     messages=[
#         {
#             'role': 'system',
#             'content': 'You are helpful AI assistant'
#         },
#         {
#             'role': 'user',
#             'content': 'Do you know any popular AI agents for prompt-based site creation or modification?'
#         }
#     ]
# )
#
# print(response.choices[0].message.content)
