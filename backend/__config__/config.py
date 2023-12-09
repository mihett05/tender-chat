from pathlib import Path

from dotenv import load_dotenv

PROJECT_PATH = Path(__file__).resolve().parent.parent.parent
BACKEND_PATH = Path(__file__).resolve().parent.parent


def load_config(path=f"{PROJECT_PATH}/.env") -> None:
    load_dotenv(path)
