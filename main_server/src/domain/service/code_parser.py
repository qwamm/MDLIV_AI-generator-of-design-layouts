import os


class CodeParser:
    def __init__(self):
        pass

    @staticmethod
    def parse_html(dir: str):
        CodeParser.parse_format(dir, 'html')

    @staticmethod
    def parse_css(dir: str):
        CodeParser.parse_format(dir, 'css')

    @staticmethod
    def parse_js(dir: str):
        CodeParser.parse_format(dir, 'js')

    @staticmethod
    def parse_format(dir: str, postfix: str):
        data = {}
        for dirpath, _, files in os.walk(dir):
            for file in files:
                if file.endswith(f'.{postfix}'):
                    with open(os.path.join(dirpath, file), 'r', encoding='utf8', errors='ignore') as f:
                        content = f.readlines()
                        if content != 'Not Found':
                            data[file] = content
        return data

    @staticmethod
    def parse_formats(dir: str, formats: list[str]):
        data = {}
        for format in formats:
            data[format] = CodeParser.parse_format(dir, format)
        return data
