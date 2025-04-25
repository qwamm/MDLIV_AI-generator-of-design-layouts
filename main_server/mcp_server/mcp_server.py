from mcp.server.fastmcp import FastMCP
from file_service import FileService

mcp = FastMCP("DesignServer")
file_service = FileService()
@mcp.tool()
async def get_site_sources(url: str) -> str:
    target_folder = file_service.get_folder(url)
    return target_folder

@mcp.tool()
async def get_file(file: str) -> str:
    return file_service.get_file_content(file)

if __name__ == "__main__":
    mcp.run()
