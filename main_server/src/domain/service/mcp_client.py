
from contextlib import AsyncExitStack
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
from typing import Any, Dict, List, Optional

class MCPClient:
    def __init__(self):
        # Initialize session and client objects
        self.write = None
        self.stdio = None
        self.session: Optional[ClientSession] = None
        self.exit_stack = AsyncExitStack()
        self.tools = None

    async def connect_to_server(self, server_script_path: str):
        is_python = server_script_path.endswith('.py')
        is_js = server_script_path.endswith('.js')
        if not (is_python or is_js):
            raise ValueError("Server script must be a .py or .js file")

        command = "python" if is_python else "node"
        server_params = StdioServerParameters(
            command=command,
            args=[server_script_path],
            env=None
        )

        stdio_transport = await self.exit_stack.enter_async_context(stdio_client(server_params))
        self.stdio, self.write = stdio_transport
        self.session = await self.exit_stack.enter_async_context(ClientSession(self.stdio, self.write))

        await self.session.initialize()

        # List available tools
        response = await self.session.list_tools()
        self.tools = [dict(tool) for tool in response.tools]
        print("\nConnected to server with tools:", [tool['name'] for tool in self.tools])

    async def disconnect(self) -> None:
        await self.exit_stack.aclose()

    async def call_tool(self, name: str, arguments: Dict[str, Any]) -> Any:
        if not self.session:
            raise RuntimeError("MCPClient is not connected")
        return await self.session.call_tool(name, arguments)

mcp_client = MCPClient()