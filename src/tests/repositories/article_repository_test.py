import unittest
from repositories.article_repository import article_repository
from entities.article import Article


class TestArticleRepository(unittest.TestCase):
    def setUp(self):
        article_repository.delete_all()
        self.article_a = Article('test article a', 'testing a', 'test.com')
        self.article_b = Article('test article b', 'testing b', 'test.com')

    def test_create(self):
        article_repository.create(self.article_a)
        articles = article_repository.find_all()
        self.assertEqual(len(articles), 1)
        self.assertEqual(articles[0].content, self.article_a.content)
        self.assertEqual(articles[0].title, self.article_a.title)

    def test_find_all(self):
        article_repository.create(self.article_a)
        article_repository.create(self.article_b)
        articles = article_repository.find_all()

        self.assertEqual(len(articles), 2)
        self.assertEqual(articles[0].title, self.article_a.title)
        self.assertEqual(articles[0].content, self.article_a.content)
        self.assertEqual(articles[1].title, self.article_b.title)
        self.assertEqual(articles[1].content, self.article_b.content)

    def test_find_by_id(self):
        article_a = article_repository.create(self.article_a)
        article_b = article_repository.create(self.article_b)
        articles = article_repository.find_all()

        returned_article = article_repository.find_by_id(article_b.id)

        self.assertEqual(len(articles), 2)
        self.assertEqual(returned_article.title, article_b.title)
        self.assertEqual(returned_article.content, article_b.content)
        self.assertNotEqual(returned_article.title, article_a.title)

    def test_delete(self):
        article_a = article_repository.create(self.article_a)
        article_b = article_repository.create(self.article_b)
        articles = article_repository.find_all()

        self.assertEqual(len(articles), 2)

        article_repository.delete(article_b.id)

        articles_after_delete = article_repository.find_all()

        self.assertEqual(len(articles_after_delete), 1)
        self.assertEqual(articles[0].title, article_a.title)
