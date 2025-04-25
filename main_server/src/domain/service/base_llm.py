from copy import deepcopy
from logging import getLogger, FileHandler, DEBUG

llm_logger = getLogger('LLM_module')
handler = FileHandler('llm.log', mode='a')
llm_logger.setLevel(DEBUG)
llm_logger.addHandler(handler)


class BaseLLm:
    def __init__(self, path_to_model: str, tool_list: list):
        self.tools = BaseLLm._process_tools(tool_list)
        self.model = None

    def infer(self, system_prompt: str, user_prompt: str, tools_on: bool, tool_choice: dict):
        pass

    ''' Basically a converter from Anthropic tool format into OpenAI-compatible format '''
    @staticmethod
    def _convert_tool(tool: dict):
        new_tool = deepcopy(tool)
        new_tool['parameters'] = new_tool.pop('inputSchema')
        new_tool['parameters'].pop('title')
        for key in new_tool['parameters']['properties'].keys():
            new_tool['parameters']['properties'][key]['description'] = new_tool['parameters']['properties'][key].pop(
                'title')
        return {'type': 'function', 'function': new_tool}

    @staticmethod
    def _process_tools(tool_list: list):
        return [BaseLLm._convert_tool(tool) for tool in tool_list]

    def reset(self):
        pass
