"""
Client Configuration for Offloaded Slide Generation
Reads worker endpoints from environment variables or config.json.
"""
import os
import json

CONFIG_FILE = os.path.join(os.path.dirname(__file__), "config.json")

# Default URLs (can be overridden by config.json or environment variables)
DEFAULT_CONFIG = {
    "screenshot_worker_url": "http://127.0.0.1:8000",
    "stitcher_worker_url": "http://127.0.0.1:8001",
    "screenshot_concurrency": 4,
    "stitcher_concurrency": 8,
    "request_timeout_sec": 120
}

def load_config() -> dict:
    config = dict(DEFAULT_CONFIG)
    if os.path.exists(CONFIG_FILE):
        try:
            with open(CONFIG_FILE, "r", encoding="utf-8") as f:
                user_conf = json.load(f)
                config.update(user_conf)
        except Exception:
            pass

    # Environment variables take highest precedence
    if os.environ.get("SCREENSHOT_WORKER_URL"):
        config["screenshot_worker_url"] = os.environ["SCREENSHOT_WORKER_URL"]
    if os.environ.get("STITCHER_WORKER_URL"):
        config["stitcher_worker_url"] = os.environ["STITCHER_WORKER_URL"]
    if os.environ.get("SCREENSHOT_CONCURRENCY"):
        config["screenshot_concurrency"] = int(os.environ["SCREENSHOT_CONCURRENCY"])
    if os.environ.get("STITCHER_CONCURRENCY"):
        config["stitcher_concurrency"] = int(os.environ["STITCHER_CONCURRENCY"])

    return config

def save_config(config_data: dict):
    with open(CONFIG_FILE, "w", encoding="utf-8") as f:
        json.dump(config_data, f, indent=2)
