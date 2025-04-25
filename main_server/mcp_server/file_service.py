import os
import hashlib
import threading
from filelock import FileLock
from pywebcopy import save_webpage
from file_cache import LRUCacheTTL
from beautify import beautify_files

def _get_project_name(url: str) -> str:
    url_hash = hashlib.sha256(url.encode()).hexdigest()
    return f"site_{url_hash}"


class FileService:
    def __init__(
            self,
            projects_folder: str = "tmp/pywebcopy",
            cache_max_size: int = 128,
            cache_ttl: int = 600
    ):
        self.projects_folder = projects_folder
        os.makedirs(self.projects_folder, exist_ok=True)
        self.cache = LRUCacheTTL(max_size=cache_max_size, ttl=cache_ttl)

    def get_folder(self, url: str) -> str:
        print(f"GETTING FILE {url}")
        cached = self.cache.get(url)
        if cached and os.path.exists(cached):
            return cached
        print(f"NOT CACHED FILE {url}")

        target_folder = self.download(url)
        self.cache.set(url, target_folder)
        return target_folder

    def download(self, url: str) -> str:
        project_name = _get_project_name(url)
        target_folder = os.path.join(self.projects_folder, project_name)

        if os.path.exists(target_folder):
            self.cache.set(url, target_folder)
            return target_folder

        site_lock_path = os.path.join(self.projects_folder, f"{project_name}.lock")

        try:
            with FileLock(site_lock_path, timeout=10):
                if os.path.exists(target_folder):
                    self.cache.set(url, target_folder)
                    return target_folder

                save_webpage(
                    url=url,
                    project_folder=self.projects_folder,
                    project_name=project_name,
                    bypass_robots=True,
                    debug=False,
                    open_in_browser=False,
                    threaded=False
                )

                js_files = []
                for root, _, files in os.walk(target_folder):
                    for file in files:
                        if file.endswith(".js"):
                            js_files.append(os.path.join(root, file))

                beautify_files(js_files)

                self.cache.set(url, target_folder)

        except Exception as e:
            if os.path.exists(target_folder):
                import shutil
                shutil.rmtree(target_folder)
            raise e

        return target_folder

    def get_file_content(self, path: str) -> str:
        if not os.path.exists(path):
            raise Exception(f"File {path} not found.")

        cached = self.cache.get(path)
        if cached:
            return cached

        with open(path, "r") as f:
            content = f.read()

        self.cache.set(path, content)
        return content