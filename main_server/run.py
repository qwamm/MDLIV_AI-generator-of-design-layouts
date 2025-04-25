import uvicorn
from src import SITE_PORT, SITE_HOST, DEBUG, app
import sys

if __name__ == "__main__":
    uvicorn.run(app if sys.platform.startswith('win') else 'src:app', host=SITE_HOST, port=SITE_PORT, reload=DEBUG)
