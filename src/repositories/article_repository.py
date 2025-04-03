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
        rows = read_file_lines(self._file_path)

        for parts in rows:
            article_id, title, content = parts[:3]

            articles.append(Article(title, content, article_id))

        return articles

    def _write(self, articles):
        article_data = [(article.id, article.title, article.content)
                        for article in articles]
        write_file_lines(self._file_path, article_data)


article_repository = ArticleRepository(ARTICLES_FILE_PATH)
