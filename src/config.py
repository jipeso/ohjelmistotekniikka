import os
from dotenv import load_dotenv

dirname = os.path.dirname(__file__)

try:
    load_dotenv(dotenv_path=os.path.join(dirname, "..", ".env"))
except FileNotFoundError:
    pass

ARTICLES_FILENAME = os.getenv("ARTICLES_FILENAME") or "articles.csv"
ARTICLES_FILE_PATH = os.path.join(dirname, "..", "data", ARTICLES_FILENAME)

FEEDS_FILENAME = os.getenv("FEEDS_FILENAME") or "feeds.csv"
FEEDS_FILE_PATH = os.path.join(dirname, "..", "data", FEEDS_FILENAME)
