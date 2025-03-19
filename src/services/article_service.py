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

    def get_all(self):
        return self._article_repository.find_all()

    def create(self, title, content):
        article = Article(title=title, content=content)

        return self._article_repository.create(article)

    def get(self, article_id):
        return self._article_repository.find_by_id(article_id)


article_service = ArticleService()
