import feedparser
from entities.feed import Feed
from entities.article import Article
from config import FEEDS_FILE_PATH
from util import read_file_lines


class FeedRepository:
    def __init__(self, file_path):
        self._file_path = file_path

    def find_all(self):
        return self._read()

    def _read(self):
        feeds = []
        rows = read_file_lines(self._file_path)

        for parts in rows:
            feed_id, url, name = parts[:3]

            feeds.append(Feed(url, name, feed_id))

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
