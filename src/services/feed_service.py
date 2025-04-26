from entities.feed import Feed

from repositories.feed_repository import (
    feed_repository as default_feed_repository
)


class FeedService:
    def __init__(
        self,
        feed_repository=default_feed_repository
    ):
        self._feed_repository = feed_repository

    def create_feed(self, url, name):
        feed = Feed(url=url, name=name)

        return self._feed_repository.create(feed)

    def parse_feed(self, url):
        articles = self._feed_repository.parse(url)

        return articles

    def get_all_feeds(self):
        return self._feed_repository.find_all()

    def remove_feed(self, feed_id):
        self._feed_repository.delete(feed_id)


feed_service = FeedService()
