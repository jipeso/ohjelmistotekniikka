from newspaper import Article as NewsArticle
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

    def create_article(self, title, content, url):
        article = Article(title=title, content=content, url=url)

        return self._article_repository.create(article)

    def get_article(self, article_id):
        return self._article_repository.find_by_id(article_id)

    def remove_article(self, article_id):
        self._article_repository.delete(article_id)

    def remove_all_articles(self):
        self._article_repository.delete_all()

    def edit_article(self, article_id, title, content, url):
        edited_article = Article(
            article_id=article_id, title=title, content=content, url=url)

        return self._article_repository.edit(edited_article)

    def scrape_web_article(self, url):
        news_article = NewsArticle(url)
        news_article.download()
        news_article.parse()

        article = Article(
            title=news_article.title,
            content=news_article.text,
            url=url
        )

        return self._article_repository.create(article)


article_service = ArticleService()
