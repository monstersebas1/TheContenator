"""Configuration reader — loads config.json from project root."""

import json
import os

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
CONFIG_PATH = os.path.join(ROOT_DIR, "config.json")


def load_config() -> dict:
    """Read and return the full config dict."""
    if not os.path.exists(CONFIG_PATH):
        raise FileNotFoundError(
            f"config.json not found at {CONFIG_PATH}. "
            "Copy config/config.example.json to config.json and fill in values."
        )
    with open(CONFIG_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


def get(key: str, default=None):
    """Get a single config value by key."""
    config = load_config()
    return config.get(key, default)
