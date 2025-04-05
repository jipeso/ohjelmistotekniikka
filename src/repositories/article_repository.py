from entities.article import Article
from config import ARTICLES_FILE_PATH
from util import read_file_lines, write_file_lines


class ArticleRepository:
    def __init__(self, file_path):
        self._file_path = file_path

    def find_all(self):
        return self._read()

    def find_by_id(self, article_id):
        articles = self.find_all()

        return next((a for a in articles if a.id == article_id), None)

    def create(self, article):
        articles = self.find_all()

        articles.append(article)

        self._write(articles)

        return article

    def delete(self, article_id):
        articles = self.find_all()

        articles_without_id = filter(
            lambda article: article.id != article_id, articles
        )

        self._write(articles_without_id)

    def delete_all(self):
        self._write([])

    def _read(self):
        articles = []
        data = read_file_lines(self._file_path)

        for article in data:
            article_id = article.get("id")
            title = article.get("title")
            content = article.get("content")
            url = article.get("url")

            articles.append(Article(title, content, url, article_id))

        return articles

    def _write(self, articles):
        data = [
            {
                "id": article.id,
                "title": article.title,
                "content": article.content,
                "url": article.url
            }
            for article in articles
        ]

        write_file_lines(self._file_path, data)


article_repository = ArticleRepository(ARTICLES_FILE_PATH)
