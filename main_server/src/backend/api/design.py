from time import sleep

import httpx
import requests
from fastapi_controllers import Controller, get, post
from pydantic import BaseModel
from src.domain import mcp_client, PromptAnalyze, OpenRouter, LocalModel
from src.enviroments import MODEL_PATH, OPENROUTER_KEY, OPENROUTER_MODEL, REMOTE, HUGGING_FACE_ID
from src.enviroments import DEPLOY_HOST, DEPLOY_PORT
import hashlib


class UserRequest(BaseModel):
    url: str
    prompt: str


class DesignBaseController(Controller):
    prefix = "/design"
    tags = ["design"]

    def __init__(self):
        super().__init__()
        self.analyzer = PromptAnalyze(
            OpenRouter(OPENROUTER_KEY, OPENROUTER_MODEL, mcp_client.tools) if REMOTE else
            LocalModel(MODEL_PATH, mcp_client.tools)
        )

    @post("/redesign")
    async def redesign(self, request :UserRequest):
        resp = await self.analyzer.process_user_request(request.prompt, request.url)

        response = httpx.post(
            url=f'http://{DEPLOY_HOST}:{DEPLOY_PORT}/api/hosts/deploy?base_site_dir=modified%2Ftmp%2Fpywebcopy%2F',
            headers={
                'accept': 'application/json',
                'Content-Type': 'application/json'
            },
            json={
                'url': request.url,
                'path': ''
            }
        )
        print(response.content)
        print(response.json())

        return {"message": f'url: {request.url}, prompt: {request.prompt}', 'response': f'http://{DEPLOY_HOST}:{DEPLOY_PORT}/api/hosts/site/{response.json()["mount_path"]}'}
