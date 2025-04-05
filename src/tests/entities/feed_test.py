import unittest
from entities.feed import Feed


class TestFeed(unittest.TestCase):
    def setUp(self):
        self.feed = Feed(
            "https://example.com",
            "testing name",
        )

    def test_created_feed_exists(self):
        self.assertNotEqual(self.feed, None)

    def test_created_feed_url_is_correct(self):
        self.assertEqual(self.feed.url, "https://example.com")

    def test_created_feed_name_is_correct(self):
        self.assertEqual(self.feed.name, "testing name")
