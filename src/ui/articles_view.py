from tkinter import ttk, constants
from services.article_service import article_service


class ArticleListView:
    def __init__(self, root, articles, change_to_article_view):
        self._root = root
        self._articles = articles
        self._change_to_article_view = change_to_article_view
        self._frame = None

        self._initialize()

    def pack(self):
        self._frame.pack(fill=constants.X)

    def destroy(self):
        self._frame.destroy()

    def _initialize_article_item(self, article):
        item_frame = ttk.Frame(master=self._frame)

        label = ttk.Label(
            master=item_frame,
            text=article.title,
            wraplength=300,
            cursor="hand2",
        )

        label.bind("<Button-1>", lambda e: self._change_to_article_view(article))

        label.grid(row=0, column=0, padx=10, pady=10, sticky=constants.W)

        item_frame.grid_columnconfigure(0, weight=1, )

        item_frame.pack(fill=constants.X)

    def _initialize(self):
        self._frame = ttk.Frame(master=self._root)

        for article in self._articles:
            self._initialize_article_item(article)


class ArticlesView:
    def __init__(self, root, change_to_search_view, change_to_article_view):
        self._root = root
        self._frame = None
        self._change_to_search_view = change_to_search_view
        self._change_to_article_view = change_to_article_view
        self._article_list_frame = None
        self._article_list_view = None

        self._initialize()

    def pack(self):
        self._frame.pack(fill=constants.X)

    def destroy(self):
        self._frame.destroy()

    def _initialize_article_list(self):
        if self._article_list_view:
            self._article_list_view.destroy()

        articles = article_service.get_all()

        self._article_list_view = ArticleListView(
            self._article_list_frame,
            articles,
            self._change_to_article_view
        )

        self._article_list_view.pack()

    def _initialize_header(self):
        search_page_button = ttk.Button(
            master=self._frame,
            text="Search page",
            command=self._change_to_search_view
        )

        search_page_button.grid(
            row=0,
            column=0,
            padx=10,
            pady=10,
            sticky=constants.W
        )

    def _initialize(self):
        self._frame = ttk.Frame(master=self._root)
        self._article_list_frame = ttk.Frame(master=self._frame)

        self._initialize_header()
        self._initialize_article_list()

        self._article_list_frame.grid(
            row=1,
            column=1,
            sticky=constants.EW
        )

        self._frame.grid_columnconfigure(0, weight=1, minsize=150)
        self._frame.grid_columnconfigure(1, weight=2, minsize=300)
        self._frame.grid_columnconfigure(2, weight=1, minsize=300)
