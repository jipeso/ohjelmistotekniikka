from repositories.feed_repository import (
    feed_repository as default_feed_repository
)


class FeedService:
    def __init__(self):
        self._feed_repository = default_feed_repository

    def parse_feed(self, url, limit=10):
        articles = self._feed_repository.parse_feed(url)

        return articles[:limit]

    def get_all(self):
        return self._feed_repository.find_all()


feed_service = FeedService()
