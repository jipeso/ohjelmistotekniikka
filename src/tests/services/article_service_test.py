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

        return article

    def find_by_id(self, article_id):
        return next((a for a in self.articles if a.id == article_id), None)

    def delete(self, article_id):
        articles_after_delete = filter(
            lambda article: article.id != article_id, self.articles)

        self.articles = list(articles_after_delete)


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
        article_a = self.article_service.create(
            self.article_a.title, self.article_a.content)
        article_b = self.article_service.create(
            self.article_b.title, self.article_b.content)
        articles = self.article_service.get_all()

        self.assertEqual(len(articles), 2)
        self.article_service.remove(article_a.id)

        articles_after_remove = self.article_service.get_all()

        self.assertEqual(len(articles_after_remove), 1)
        self.assertNotEqual(articles_after_remove[0].id, article_a.id)

    def test_get(self):
        article_a = self.article_service.create(
            self.article_a.title, self.article_a.content)
        article_b = self.article_service.create(
            self.article_b.title, self.article_b.content)
        returned_article_b = self.article_service.get(article_b.id)

        self.assertEqual(article_b.title, returned_article_b.title)
        self.assertEqual(article_b.content, returned_article_b.content)

        nonexistent_article = self.article_service.get("123")
        self.assertEqual(nonexistent_article, None)
