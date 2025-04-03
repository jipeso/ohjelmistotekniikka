import unittest
from entities.article import Article
from services.article_service import ArticleService

class StubArticleRepository:
    def __init__(self, articles=None):
        self.articles = articles or []

    def find_all(self):
        return self.articles

    def create(self, article):
        self.articles.append(article)

    def find_by_id(self, article_id):
        articles = self.find_all()

        return next((a for a in articles if a.id == article_id), None)

    def delete(self, article_id):
        self.articles = [a for a in self.articles if a.id != article_id]

class TestArticleService(unittest.TestCase):
    def setUp(self):
        self.article_service = ArticleService(StubArticleRepository())
        self.article_a = Article('test article a', 'testing a')
        self.article_b = Article('test article b', 'testing b')

    def test_create(self):
        self.article_service.create('test title', 'test content')
        articles = self.article_service.get_all()

        self.assertEqual(len(articles), 1)
        self.assertEqual(articles[0].title, 'test title')
        self.assertEqual(articles[0].content, 'test content')

    def test_remove(self):
        self.article_service.create(self.article_a.title, self.article_a.content)
        self.article_service.create(self.article_b.title, self.article_b.content)
        articles = self.article_service.get_all()

        self.assertEqual(len(articles), 2)

        id_to_delete = articles[0].id
        self.article_service.remove(id_to_delete)

        articles_after_delete = self.article_service.get_all()

        self.assertEqual(len(articles_after_delete), 1)
        self.assertNotEqual(articles_after_delete[0].id, id_to_delete)
