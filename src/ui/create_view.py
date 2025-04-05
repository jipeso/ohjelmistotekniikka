from tkinter import ttk, constants, scrolledtext
from services.article_service import article_service


class CreateView:
    def __init__(self, root, change_to_articles_view):
        self._root = root
        self._change_to_articles_view = change_to_articles_view
        self._frame = None

        self._title_input = None
        self._content_input = None
        self._url_input = None

        self._initialize()

    def pack(self):
        self._frame.pack(fill=constants.X)

    def destroy(self):
        self._frame.destroy()

    def _handle_create(self):
        title = self._title_input.get()
        content = self._content_input.get("1.0", constants.END).strip()
        url = self._url_input.get()

        if title and content and url:
            article_service.create_article(title, content, url)
            self._change_to_articles_view()

    def _initialize_fields(self):
        title_label = ttk.Label(
            master=self._frame, text="title"
        )
        title_label.grid(row=1, column=1, padx=10, pady=5, sticky=constants.W)

        self._title_input = ttk.Entry(master=self._frame)
        self._title_input.grid(row=2, column=1,  padx=10,
                               pady=5, sticky=constants.EW)

        content_label = ttk.Label(
            master=self._frame, text="content"
        )
        content_label.grid(row=3, column=1, padx=10,
                           pady=5, sticky=constants.W)

        self._content_input = scrolledtext.ScrolledText(
            master=self._frame,
            wrap="word",
            height=7
        )

        self._content_input.grid(row=4, column=1, padx=10,
                                 pady=5, sticky=constants.EW)

        url_label = ttk.Label(
            master=self._frame, text="url"
        )
        url_label.grid(row=5, column=1, padx=10, pady=5, sticky=constants.W)

        self._url_input = ttk.Entry(master=self._frame)

        self._url_input.grid(row=6, column=1, padx=10,
                             pady=5, sticky=constants.W)

    def _initialize(self):
        self._frame = ttk.Frame(master=self._root)

        back_button = ttk.Button(
            master=self._frame,
            text="back to articles",
            command=self._change_to_articles_view
        )
        back_button.grid(row=0, column=0, padx=10, pady=10, sticky=constants.W)

        self._initialize_fields()

        create_button = ttk.Button(
            master=self._frame,
            text="create",
            command=self._handle_create
        )

        create_button.grid(row=7, column=1, padx=10,
                           pady=10, sticky=constants.W)

        self._frame.grid_columnconfigure(0, weight=1, minsize=150)
        self._frame.grid_columnconfigure(1, weight=2, minsize=300)
        self._frame.grid_columnconfigure(2, weight=1, minsize=150)
