import os
from urllib.parse import urlparse

from configs.config import REDIS_URL

if __name__ == "__main__":
    parsed_url = urlparse(REDIS_URL)
    port = parsed_url.port
    os.system(f"redis-server --port {port}")