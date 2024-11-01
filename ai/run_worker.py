import os

from configs.config import REDIS_URL
import argparse

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--name", type=str, default="default")
    args = parser.parse_args()

    os.system(f"rq worker --url {REDIS_URL} {args.name}")
