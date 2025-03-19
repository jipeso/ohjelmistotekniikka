from pathlib import Path
from entities.article import Article
from config import ARTICLES_FILE_PATH


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
            lambda article: article.id != article_id, articles)

        self._write(articles_without_id)

    def delete_all(self):
        self._write([])

    def _ensure_file_exists(self):
        Path(self._file_path).touch()

    def _read(self):
        articles = []

        self._ensure_file_exists()

        with open(self._file_path, encoding="utf-8") as file:
            for row in file:
                row = row.replace("\n", "")
                parts = row.split(";")

                article_id = parts[0]
                title = parts[1]
                content = parts[2]

                articles.append(
                    Article(title, content, article_id)
                )

        return articles

    def _write(self, articles):
        self._ensure_file_exists()

        with open(self._file_path, "w", encoding="utf-8") as file:
            for article in articles:

                row = f"{article.id};{article.title};{article.content}"

                file.write(row+"\n")


article_repository = ArticleRepository(ARTICLES_FILE_PATH)
