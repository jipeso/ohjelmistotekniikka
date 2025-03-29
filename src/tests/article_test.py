import unittest
from entities.article import Article


class TestArticle(unittest.TestCase):
    def setUp(self):
        self.article = Article(
            "test article",
            "content for testing"
        )

    def test_created_article_exists(self):
        self.assertNotEqual(self.article, None)

    def test_created_article_title_is_correct(self):
        self.assertEqual(self.article.title, "test article")

    def test_create_article_content_is_correct(self):
        self.assertEqual(self.article.content, "content for testing")
