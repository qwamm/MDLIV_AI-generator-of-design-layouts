from fastapi import FastAPI
from .backend import router
from contextlib import asynccontextmanager

from .domain import mcp_client
from .enviroments import MCP_SERVER_PATH

@asynccontextmanager
async def lifespan(app: FastAPI):
    await mcp_client.connect_to_server(MCP_SERVER_PATH)
    yield
    await mcp_client.disconnect()

app = FastAPI(
    docs_url="/api/docs",
    title='MDLIV',
    version="0.1",
    lifespan=lifespan
    )

app.include_router(router)
