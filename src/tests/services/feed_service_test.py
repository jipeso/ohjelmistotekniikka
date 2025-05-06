import unittest
from entities.feed import Feed
from services.feed_service import FeedService


class FeedRepositoryStub:
    def __init__(self, feeds=None):
        self.feeds = feeds or []
        self.id_count = 1

    def find_all(self):
        return self.feeds

    def create(self, feed):
        feed.id = self.id_count
        self.id_count += 1
        self.feeds.append(feed)

        return feed

    def delete(self, feed_id):
        feeds_after_delete = filter(
            lambda feed: feed.id != feed_id, self.feeds)

        self.feeds = list(feeds_after_delete)

    def delete_all(self):
        self.feeds = []


class TestFeedService(unittest.TestCase):
    def setUp(self):
        self.feed_service = FeedService(FeedRepositoryStub())
        self.feed_a = Feed('https://example.com/a', 'testing a')
        self.feed_b = Feed('https://example.com/b', 'testing b')

    def test_create_feed(self):
        self.feed_service.create_feed('https://example.com', 'testing')
        feeds = self.feed_service.get_all_feeds()

        self.assertEqual(len(feeds), 1)
        self.assertEqual(feeds[0].url, 'https://example.com')
        self.assertEqual(feeds[0].name, 'testing')

    def test_remove_feed(self):
        feed_a = self.feed_service.create_feed(
            self.feed_a.url, self.feed_a.name)
        feed_b = self.feed_service.create_feed(
            self.feed_b.url, self.feed_b.name)
        feeds = self.feed_service.get_all_feeds()

        self.assertEqual(len(feeds), 2)
        self.assertEqual(feeds[1].name, feed_b.name)

        self.feed_service.remove_feed(feed_a.id)

        feeds_after_remove = self.feed_service.get_all_feeds()

        self.assertEqual(len(feeds_after_remove), 1)
        self.assertNotEqual(feeds_after_remove[0].id, feed_a.id)
