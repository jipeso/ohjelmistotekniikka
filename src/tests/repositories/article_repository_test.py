import unittest
from repositories.article_repository import article_repository
from entities.article import Article

class TestArticleRepository(unittest.TestCase):
    def setUp(self):
        article_repository.delete_all()

        self.article = Article('test article', 'content for testing')

    def test_create(self):
        article_repository.create(self.article)
        articles = article_repository.find_all()

        self.assertEqual(len(articles), 1)
        self.assertEqual(articles[0].content, self.article.content)
