from tkinter import ttk, constants, scrolledtext, messagebox
from services.article_service import article_service


class CreateView:
    def __init__(self, root, show_articles_view):
        self._root = root
        self._show_articles_view = show_articles_view
        self._frame = None

        self._title_entry = None
        self._content_entry = None
        self._url_entry = None

        self._initialize()

    def pack(self):
        self._frame.pack(fill=constants.X)

    def destroy(self):
        self._frame.destroy()

    def _handle_create(self):
        title = self._title_entry.get()
        content = self._content_entry.get("1.0", constants.END)
        url = self._url_entry.get()

        if title and content and url:
            article_service.create_article(title, content, url)
            self._show_articles_view()

        else:
            messagebox.showerror(
                "empty fields", "missing title, content or url")

    def _initialize_header(self):
        header_frame = ttk.Frame(master=self._frame)
        header_frame.grid(row=0, column=0, columnspan=2, sticky=constants.EW)

        back_button = ttk.Button(
            master=header_frame,
            text="back",
            command=self._show_articles_view
        )

        back_button.grid(
            row=0,
            column=0,
            padx=5,
            pady=5,
            sticky=constants.W
        )

    def _initialize_fields(self):
        title_label = ttk.Label(
            master=self._frame, text="title"
        )
        title_label.grid(row=1, column=1, padx=5, pady=5, sticky=constants.W)

        self._title_entry = ttk.Entry(master=self._frame)
        self._title_entry.grid(row=2, column=1,  padx=5, sticky=constants.EW)

        content_label = ttk.Label(
            master=self._frame, text="content"
        )
        content_label.grid(row=3, column=1, padx=5,
                           pady=5, sticky=constants.W)

        self._content_entry = scrolledtext.ScrolledText(
            master=self._frame,
            wrap="word",
            height=7
        )

        self._content_entry.grid(row=4, column=1, padx=5, sticky=constants.EW)

        url_label = ttk.Label(
            master=self._frame, text="url"
        )
        url_label.grid(row=5, column=1, padx=5, pady=5, sticky=constants.W)

        self._url_entry = ttk.Entry(master=self._frame)

        self._url_entry.grid(row=6, column=1, padx=5, sticky=constants.EW)

        create_button = ttk.Button(
            master=self._frame,
            text="create",
            command=self._handle_create
        )

        create_button.grid(row=7, column=1, padx=5,
                           pady=10, sticky=constants.W)

    def _initialize(self):
        self._frame = ttk.Frame(master=self._root)

        self._initialize_header()
        self._initialize_fields()

        self._frame.grid_columnconfigure(0, weight=1)
        self._frame.grid_columnconfigure(1, weight=2)
        self._frame.grid_columnconfigure(2, weight=1)
