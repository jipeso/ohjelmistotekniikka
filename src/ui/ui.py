from ui.articles_view import ArticlesView
from ui.search_view import SearchView
from ui.read_view import ReadView
from ui.create_view import CreateView
from ui.edit_view import EditView


class UI:
    def __init__(self, root):
        self._root = root
        self._current_view = None

    def start(self):
        self._show_articles_view()

    def _hide_current_view(self):
        if self._current_view:
            self._current_view.destroy()

        self._current_view = None

    def _show_article_view(self, article_id):
        self._hide_current_view()

        self._current_view = ReadView(
            self._root,
            article_id,
            self._show_articles_view,
            self._show_edit_view
        )

        self._current_view.pack()

    def _show_create_view(self):
        self._hide_current_view()

        self._current_view = CreateView(
            self._root,
            self._show_articles_view
        )

        self._current_view.pack()

    def _show_articles_view(self):
        self._hide_current_view()

        self._current_view = ArticlesView(
            self._root,
            self._show_search_view,
            self._show_article_view,
            self._show_create_view
        )

        self._current_view.pack()

    def _show_search_view(self):
        self._hide_current_view()

        self._current_view = SearchView(
            self._root,
            self._show_articles_view
        )

        self._current_view.pack()

    def _show_edit_view(self, article_id):
        self._hide_current_view()

        self._current_view = EditView(
            self._root,
            article_id,
            self._show_article_view
        )

        self._current_view.pack()
