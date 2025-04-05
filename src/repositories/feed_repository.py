import feedparser
from entities.feed import Feed
from entities.article import Article
from config import FEEDS_FILE_PATH
from util import read_file_lines, write_file_lines


class FeedRepository:
    def __init__(self, file_path):
        self._file_path = file_path

    def find_all(self):
        return self._read()

    def create(self, feed):
        feeds = self.find_all()
        feeds.append(feed)
        self._write(feeds)

        return feed

    def delete_all(self):
        self._write([])

    def _read(self):
        feeds = []
        data = read_file_lines(self._file_path)

        for feed in data:
            feed_id = feed.get("id")
            url = feed.get("url")
            name = feed.get("name")

            feeds.append(Feed(url, name, feed_id))

        return feeds

    def _write(self, feeds):
        feed_data = [
            {
                "id": feed.id,
                "url": feed.url,
                "name": feed.name
            }
            for feed in feeds
        ]

        write_file_lines(self._file_path, feed_data)

    def parse(self, url):
        feed = feedparser.parse(url)
        articles = []

        for entry in feed.entries:
            article = Article(
                title=entry.title,
                content=None,
                url=entry.link
            )
            articles.append(article)

        return articles

    def delete(self, feed_id):
        feeds = self.find_all()

        feeds_without_id = filter(
            lambda feed: feed.id != feed_id, feeds
        )

        self._write(feeds_without_id)


feed_repository = FeedRepository(FEEDS_FILE_PATH)
