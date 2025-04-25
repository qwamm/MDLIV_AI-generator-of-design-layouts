from .base_llm import llm_logger
from .openrouter_llm import OpenRouter
from .llm import LocalModel
from .mcp_client import mcp_client
from .code_parser import CodeParser
from .code_saver import CodeSaver


class PromptAnalyze:
    def __init__(self, model: LocalModel | OpenRouter):
        self.model = model

    async def process_user_request(self, prompt: str, url: str):
        call = await mcp_client.call_tool('get_site_sources', {'url': url})
        llm_logger.info(f'mcp_server_call_response: {call.content[0].text}, {call.isError}\n')

        if call.isError:
            return "URL sources are unavailiable. Try different one."

        # parsing loaded files
        formats = ['html', 'css', 'js']
        parsed_data = CodeParser.parse_formats(call.content[0].text, formats)

        # forming new user prompt
        system_prompt = f'You are an AI assistant that modifies site code.\n\n' \
                        f'YOU SHOULD ONLY MODIFY CODE IN THE GIVEN FILES. DO NOT ADD ANY COMMENTS.\n' \
                        f'OUTPUT THE CODE IN THE FOLLOWING FORMAT:\n' \
                        f'[FILE: file_name]\n' \
                        f'modified code\n\n' \
                        f'IF THE FILE SHOULD NOT BE MODIFIED THEN DO NOT OUTPUT IT.\n' \
                        f'DO NOT ADD ANY COMMENTS' \
                        f'DO NOT ENCODE HTML TAGS'
        user_prompt = 'Current files:\n'

        for file_format in parsed_data.keys():
            if not len(parsed_data[file_format].keys()):
                continue
            user_prompt += f'{file_format} files:\n\n'
            for file in parsed_data[file_format].keys():
                user_prompt += f'[FILE: {file}]\n\n{"".join(parsed_data[file_format][file])}\n\n'
        user_prompt += f'Task: {prompt}'

        llm_logger.info(f'system: {system_prompt}\n')
        llm_logger.info(f'user: {user_prompt}\n')

        response = self.model.infer(system_prompt, user_prompt, False, {})
        llm_logger.info(f'model: {response}\n')
        llm_logger.info(f'saving output {response["choices"][0]["message"]["content"]}')
        CodeSaver.save_code(response['choices'][0]['message']['content'], call.content[0].text)
        self.model.reset()
        return response['choices'][0]['message']['content']

