import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    BASE_URL = os.getenv("BASE_URL")
    USERNAME = os.getenv("USERNAME")
    PASSWORD = os.getenv("PASSWORD")
    """HEADLESS = os.getenv("HEADLESS")
    BROWSER = os.getenv("BROWSER")
    BROWSER_OPTIONS = os.getenv("BROWSER_OPTIONS")
    BROWSER_OPTIONS_HEADLESS = os.getenv("BROWSER_OPTIONS_HEADLESS")"""