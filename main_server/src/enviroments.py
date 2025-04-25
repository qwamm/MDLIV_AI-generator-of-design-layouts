import sys

SITE_HOST = "localhost"
SITE_PORT = 8000
DEBUG = not sys.platform.startswith('win')

MCP_SERVER_PATH = "main_server/mcp_server/mcp_server.py"
OPENROUTER_MODEL = 'mistralai/mistral-small-3.1-24b-instruct:free'

# https://huggingface.co/mistralai/Mistral-Small-3.1-24B-Instruct-2503
HUGGING_FACE_ID = 'mistralai/Mistral-Small-3.1-24B-Instruct-2503'
MODEL_PATH = f'{HUGGING_FACE_ID.split("/")[-1]}.gguf'

# DEPLOY_SERVER_URL = "http://deploy_server:8080"
DEPLOY_HOST = "localhost"
DEPLOY_PORT = 8080
SITES_DIR = '/sites/deployed'

with open('open_router_key', 'r') as file:
    OPENROUTER_KEY = file.readline()

with open('hugging_face_token', 'r') as file:
    HUGGING_FACE_TOKEN = file.readline()

# if set to true OpenRouter model will be used instead of local one
REMOTE = True
