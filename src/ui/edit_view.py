from tkinter import ttk, constants, scrolledtext, messagebox
from services.article_service import article_service


class EditView:
    def __init__(self, root, article, show_read_view):
        self._root = root
        self._article = article
        self._show_read_view = show_read_view
        self._frame = None

        self._title_entry = None
        self._url_entry = None
        self._content_entry = None

        self._initialize()

    def pack(self):
        self._frame.pack(fill=constants.X)

    def destroy(self):
        self._frame.destroy()

    def _initialize_fields(self):
        title_label = ttk.Label(self._frame, text="title")
        self._title_entry = ttk.Entry(self._frame)
        self._title_entry.insert(0, self._article.title)

        url_label = ttk.Label(self._frame, text="url")
        self._url_entry = ttk.Entry(self._frame)
        self._url_entry.insert(0, self._article.url)

        content_label = ttk.Label(self._frame, text="content")
        self._content_entry = scrolledtext.ScrolledText(
            master=self._frame,
            wrap="word",
            font=("Times", 12),
            padx=5,
            pady=5,
            height=15
        )
        self._content_entry.insert("1.0", self._article.content)

        title_label.grid(row=1, column=1, padx=5, pady=5, sticky=constants.W)
        self._title_entry.grid(row=2, column=1, padx=5,
                               pady=5, sticky=constants.EW)

        url_label.grid(row=3, column=1, padx=5, pady=5, sticky=constants.W)
        self._url_entry.grid(row=4, column=1, padx=5,
                             pady=5, sticky=constants.EW)

        content_label.grid(row=5, column=1, padx=5, pady=5, sticky=constants.W)
        self._content_entry.grid(
            row=6, column=1, padx=5, pady=5, sticky=constants.EW)

    def _on_save_click(self):
        title = self._title_entry.get()
        content = self._content_entry.get("1.0", constants.END)
        url = self._url_entry.get()

        if title and content and url:
            article = article_service.edit_article(
                self._article.id,
                title,
                content,
                url
            )
            self._show_read_view(article)

        else:
            messagebox.showerror(
                "empty fields", "missing title, content or url")

    def _on_cancel_click(self):
        self.destroy()
        self._show_read_view(self._article)

    def _initialize_header(self):
        header_frame = ttk.Frame(master=self._frame)
        header_frame.grid(row=0, column=0, columnspan=3, sticky=constants.EW)

        save_button = ttk.Button(
            master=header_frame,
            text="save changes",
            command=self._on_save_click
        )
        cancel_button = ttk.Button(
            master=header_frame,
            text="cancel",
            command=self._on_cancel_click
        )
        save_button.grid(row=0, column=0, padx=5, pady=5, sticky=constants.W)
        cancel_button.grid(row=0, column=1, padx=5, pady=5, sticky=constants.W)

    def _initialize(self):
        self._frame = ttk.Frame(master=self._root)

        self._initialize_header()
        self._initialize_fields()

        self._frame.grid_columnconfigure(1, weight=1)
        self._frame.grid_columnconfigure(2, weight=2)
        self._frame.grid_columnconfigure(3, weight=1)
