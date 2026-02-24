import os
import configparser
from dotenv import load_dotenv

# Load .env
load_dotenv()
load_dotenv(override=True)

# Load .env ONLY locally, NOT in GitHub Actions
if not os.getenv("GITHUB_ACTIONS"):
    load_dotenv()

# ---------- Dynamic path ----------
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(current_dir)
config_path = os.path.join(project_root, "configurations", "config.ini")
# ----------------------------------

config = configparser.RawConfigParser()
config.read(config_path)

class ReadConfig:

    # ---------- Non-secret config ----------
    URL = config.get("credentials", "url", fallback=None)

    # ---------- Secrets from .env / GitHub ----------

    DEV_USERNAME = os.getenv("DEV_USERNAME")
    DEV_PASSWORD = os.getenv("DEV_PASSWORD")
    DEV_URL = os.getenv("DEV_URL")

    UAT_USERNAME = os.getenv("UAT_USERNAME")
    UAT_PASSWORD = os.getenv("UAT_PASSWORD")
    UAT_URL = os.getenv("UAT_URL")

    env = os.getenv("ENV")

    if env == "DEV":
        url =os.getenv("DEV_URL")
        username = os.getenv("DEV_USERNAME")
        password = os.getenv("DEV_PASSWORD")
    else:
        url =os.getenv("UAT_URL")
        username = os.getenv("UAT_USERNAME")
        password = os.getenv("UAT_PASSWORD")


