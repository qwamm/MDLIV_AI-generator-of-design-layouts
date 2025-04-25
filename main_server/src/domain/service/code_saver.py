import os
import re
import html
from .base_llm import llm_logger
import shutil

class CodeSaver:
    def __init__(self):
        pass

    @staticmethod
    def save_code(llm_output: str, site_path: str):
        seq = re.finditer("\\[FILE: (.+)\\]", llm_output)
        positions = []
        for itr in seq:
            positions.append([itr.start(), itr.end(), itr.group(1)])

        try:
            os.mkdir('modified')
        except FileExistsError:
            pass

        for i in range(len(positions)):
            pos = positions[i]

            # seems expensive, but probably not so many files are modified on average
            for dirpath, _, files in os.walk(site_path):
                for file in files:
                    if file == pos[2]:
                        pos[2] = os.path.join(dirpath, file)

            try:
                os.makedirs(os.path.join('modified', os.path.dirname(pos[2])))
            except FileExistsError:
                pass

            with open(os.path.join('modified', f'{pos[2]}'), 'w', encoding='utf-8', errors='ignore') as file:
                payload = llm_output[pos[1]:positions[i+1][0] if i+1 != len(positions) else len(llm_output):]
                if pos[2].endswith('html'):
                    payload = html.unescape(payload)
                llm_logger.info(f'actual payload of {pos[2]}:\n{payload}\n')
                file.write(payload)
        CodeSaver._copy_sources([pos[2] for pos in positions], site_path)

    @staticmethod
    def _copy_sources(modified_files: list, site_path: str):
        print(modified_files)
        for dirpath, dirname, files in os.walk(site_path):
            print(dirpath, dirname, files)
            for file in files:
                if os.path.join(dirpath, file) not in modified_files:
                    print(os.path.join(dirpath, file))
                    try:
                        shutil.copy(os.path.join(dirpath, file),
                                    os.path.join('modified', dirpath if dirpath != 'tmp' else '', file))
                    except FileNotFoundError:
                        os.makedirs(os.path.join('modified', dirpath))

                        shutil.copy(os.path.join(dirpath, file),
                                    os.path.join('modified', dirpath if dirpath != 'tmp' else '', file))
