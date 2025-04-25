import hashlib
from fastapi.responses import JSONResponse, FileResponse
from fastapi_controllers import Controller, get, post, delete
from fastapi import HTTPException
from pydantic import BaseModel
import os
from starlette.responses import RedirectResponse

def _get_project_url(url: str) -> str:
    url_hash = hashlib.sha256(url.encode()).hexdigest()
    return f"site_{url_hash}"

class ServerRequest(BaseModel):
    url: str
    path: str

# !TODO Этот костыль надо вынести в БД
active_routes = {}

class HostsController(Controller):
    prefix = "/hosts"
    tags = ["hosts"]

    def __init__(self, base_site_dir: str = "modified/tmp/pywebcopy/"):
        super().__init__()
        self.base_site_dir = base_site_dir

    @get("/list")
    async def list_hosts(self):
        return active_routes.copy()

    @get("/site/{mount_path}")
    async def redirect_to_index(self, mount_path: str):
        site_dir = active_routes.get(mount_path)
        if not site_dir:
            raise HTTPException(status_code=404, detail="Site not mounted")
        if not os.path.isdir(site_dir):
            active_routes.pop(mount_path)
            raise HTTPException(status_code=404, detail="Site not mounted")

        index_path = None
        for root, dirs, files in os.walk(site_dir):
            if "index.html" in files:
                index_path = os.path.relpath(os.path.join(root, "index.html"),site_dir)
                break

        if not index_path:
            raise HTTPException(status_code=404, detail="index.html not found")

        url = f"/api/hosts/site/{mount_path}/{index_path}"
        return RedirectResponse(url=url)

    @get("/site/{mount_path}/{requested_path:path}")
    async def serve_hosted(self, mount_path: str, requested_path: str):
        site_dir = active_routes.get(mount_path)
        if not site_dir:
            raise HTTPException(status_code=404, detail="Site not mounted")

        full_path = os.path.join(site_dir, requested_path)

        if not os.path.isfile(full_path):
            raise HTTPException(status_code=404, detail="File not found")
        return FileResponse(full_path)

    @post("/deploy")
    async def deploy_host(self, request: ServerRequest):
        mount_path = _get_project_url(request.url)
        file_path = self.base_site_dir + request.path

        if not os.path.exists(file_path):
            return JSONResponse(status_code=404, content={"detail": f"Site folder not found {file_path}"})

        if mount_path in active_routes:
            return JSONResponse(status_code=400, content={"detail": "Already mounted"})

        active_routes[mount_path] = file_path
        return {"detail": f"Mounted at {mount_path} {active_routes}",
                'mount_path': f'{mount_path}'}

    @delete("/delete")
    async def delete_host(self, request: ServerRequest):
        mount_path = _get_project_url(request.url)

        if mount_path not in active_routes:
            return JSONResponse(status_code=404, content={"detail": "Not mounted"})

        del active_routes[mount_path]
        return {"detail": f"Unmounted {mount_path}"}
