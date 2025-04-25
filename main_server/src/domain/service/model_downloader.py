from huggingface_hub import snapshot_download
import os.path
import subprocess


class ModelDownloader:
    def __init__(self):
        pass

    @staticmethod
    def get_model(model_id: str, api_token: str, outfile: str):
        ModelDownloader._download(model_id, api_token)
        ModelDownloader._to_gguf(outfile)

    @staticmethod
    def _download(model_id: str, api_token: str):
        snapshot_download(
            repo_id=model_id,
            local_dir=os.path.join(os.path.dirname(__file__), 'model'),
            token=api_token
        )

    @staticmethod
    def _to_gguf(outfile: str):
        subprocess.run('git clone https://github.com/ggerganov/llama.cpp.git')
        subprocess.run('pip install -r llama.cpp/requirements.txt')
        subprocess.run(f'python llama.cpp/convert_hf_to_gguf.py {os.path.join(os.path.dirname(__file__), "model")} '
                       f'--outfile {outfile} --outtype f32')

