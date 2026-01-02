"""Configuration management for Naviterm."""

from platformdirs import user_config_dir
import os
import json

config_dir = user_config_dir("naviterm", appauthor=False)
config_file = os.path.join(config_dir, "config.json")


def get_config_path() -> str:
    """Get the path to the config file."""
    return config_file


def load_config() -> dict:
    """Load configuration from file, creating it if it doesn't exist."""
    config = {}
    if not os.path.exists(config_dir):
        os.makedirs(config_dir)
    if not os.path.exists(config_file):
        with open(config_file, "w") as f:
            json.dump({}, f)

    with open(config_file, "r") as f:
        config = json.load(f)
    return config


def save_config(username: str, password: str, server_url: str) -> None:
    """Save configuration to file."""
    with open(config_file, "w") as f:
        json.dump(
            {
                "username": username,
                "password": password,
                "server_url": server_url,
            },
            f,
        )

