import unittest
from entities.article import Article
from services.article_service import ArticleService


class ArticleRepositoryStub:
    def __init__(self, articles=None):
        self.articles = articles or []
        self.id_count = 1

    def find_all(self):
        return self.articles

    def create(self, article):
        article.id = self.id_count
        self.id_count += 1
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
        self.article_service = ArticleService(ArticleRepositoryStub())
        self.article_a = Article(
            'test article a', 'testing a', 'https://example.com/a')
        self.article_b = Article(
            'test article b', 'testing b', 'https://example.com/b')

    def test_create(self):
        self.article_service.create_article(
            'test title', 'test content', 'https://example.com')
        articles = self.article_service.get_all_articles()

        self.assertEqual(len(articles), 1)
        self.assertEqual(articles[0].title, 'test title')
        self.assertEqual(articles[0].content, 'test content')
        self.assertEqual(articles[0].url, 'https://example.com')

    def test_remove(self):
        article_a = self.article_service.create_article(
            self.article_a.title, self.article_a.content, self.article_a.url)
        article_b = self.article_service.create_article(
            self.article_b.title, self.article_b.content, self.article_b.url)
        articles = self.article_service.get_all_articles()

        self.assertEqual(len(articles), 2)

        id_to_remove = articles[0].id
        self.article_service.remove_article(id_to_remove)

        articles_after_remove = self.article_service.get_all_articles()

        self.assertEqual(len(articles_after_remove), 1)
        self.assertEqual(articles_after_remove[0].title, article_b.title)
        self.assertNotEqual(articles_after_remove[0].title, article_a.title)

    def test_get(self):
        article = self.article_service.create_article(
            self.article_a.title, self.article_a.content, self.article_a.url)

        returned_article = self.article_service.get_article(article.id)

        self.assertEqual(article.title, returned_article.title)
        self.assertEqual(article.content, returned_article.content)
        self.assertEqual(article.url, returned_article.url)

        nonexistent_article = self.article_service.get_article("123")
        self.assertEqual(nonexistent_article, None)
