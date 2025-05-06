from entities.article import Article
from database_connection import get_database_connection


def get_article_by_row(row):
    return Article(row["title"], row["content"], row["url"], row["id"]) if row else None


class ArticleRepository:
    def __init__(self, connection):
        self._connection = connection

    def find_all(self):
        cursor = self._connection.cursor()

        cursor.execute("select * from articles")

        rows = cursor.fetchall()

        return list(map(get_article_by_row, rows))

    def find_by_id(self, article_id):
        cursor = self._connection.cursor()

        cursor.execute(
            "select * from articles where id=?",
            (article_id,)
        )
        row = cursor.fetchone()

        return get_article_by_row(row)

    def create(self, article):
        cursor = self._connection.cursor()

        cursor.execute(
            "insert into articles (title, content, url) values (?, ?, ?)",
            (article.title, article.content, article.url)
        )

        self._connection.commit()

        article.id = cursor.lastrowid

        return article

    def delete(self, article_id):
        cursor = self._connection.cursor()

        cursor.execute("delete from articles where id=?", (article_id,))

        self._connection.commit()

    def delete_all(self):
        cursor = self._connection.cursor()

        cursor.execute("delete from articles")

        self._connection.commit()

    def edit(self, edited_article):
        cursor = self._connection.cursor()

        cursor.execute("""
            update articles
            set title=?,
                content=?,
                url=?
            where id=?
            """,
                       (edited_article.title, edited_article.content,
                        edited_article.url, edited_article.id)
                       )

        self._connection.commit()
        return edited_article


article_repository = ArticleRepository(get_database_connection())
