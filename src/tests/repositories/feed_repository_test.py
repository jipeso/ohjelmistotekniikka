import unittest
from repositories.feed_repository import feed_repository
from entities.feed import Feed


class TestFeedRepository(unittest.TestCase):
    def setUp(self):
        feed_repository.delete_all()

        self.feed_a = Feed('https://test.com/rss/a', 'testing a', '1')
        self.feed_b = Feed('https://test.com/rss/b', 'testing b', '2')

    def test_create(self):
        feed_repository.create(self.feed_a)
        feeds = feed_repository.find_all()

        self.assertEqual(len(feeds), 1)
        self.assertEqual(feeds[0].url, self.feed_a.url)
        self.assertEqual(feeds[0].name, self.feed_a.name)

    def test_find_all(self):
        feed_repository.create(self.feed_a)
        feed_repository.create(self.feed_b)
        feeds = feed_repository.find_all()

        self.assertEqual(len(feeds), 2)
        self.assertEqual(feeds[0].url, self.feed_a.url)
        self.assertEqual(feeds[0].name, self.feed_a.name)
        self.assertEqual(feeds[1].url, self.feed_b.url)
        self.assertEqual(feeds[1].name, self.feed_b.name)
