import os
from pathlib import Path

from urllib.parse import urlparse

from configs.config import VECTOR_STORE_FOLDER, VECTOR_STORE_URL

if __name__ == "__main__":
    parsed_url = urlparse(VECTOR_STORE_URL)
    host = parsed_url.hostname
    port = parsed_url.port
    path = Path(VECTOR_STORE_FOLDER)
    log_path = Path(os.path.join(VECTOR_STORE_FOLDER, "chroma.log"))
    os.system(f"chroma run --host {host} --port {port} --path \"{path}\" --log-path \"{log_path}\"")
