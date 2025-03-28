from pathlib import Path
import feedparser
from entities.feed import Feed
from entities.article import Article
from config import FEEDS_FILE_PATH


class FeedRepository:
    def __init__(self, file_path):
        self._file_path = file_path

    def find_all(self):
        return self._read()

    def _ensure_file_exists(self):
        Path(self._file_path).touch()

    def _read(self):
        feeds = []

        self._ensure_file_exists()

        with open(self._file_path, encoding="utf-8") as file:
            for row in file:
                row = row.replace("\n", "")
                parts = row.split(";")

                feed_id = parts[0]
                url = parts[1]
                name = parts[2]

                feeds.append(
                    Feed(url, name, feed_id)
                )

        return feeds

    def parse_feed(self, url):
        feed = feedparser.parse(url)
        articles = []

        for entry in feed.entries:
            article = Article(
                title=entry.title,
                content=entry.link
            )
            articles.append(article)

        return articles


feed_repository = FeedRepository(FEEDS_FILE_PATH)
