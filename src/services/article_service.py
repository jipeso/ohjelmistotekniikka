from entities.article import Article

from repositories.article_repository import (
    article_repository as default_article_repository
)


class ArticleService:
    def __init__(
        self,
        article_repository=default_article_repository
    ):
        self._article_repository = article_repository

    def get_all_articles(self):
        return self._article_repository.find_all()

    def create_article(self, title, content):
        article = Article(title=title, content=content)

        return self._article_repository.create(article)

    def get_article(self, article_id):
        return self._article_repository.find_by_id(article_id)

    def remove_article(self, article_id):
        self._article_repository.delete(article_id)


article_service = ArticleService()
