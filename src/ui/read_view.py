from tkinter import ttk, constants, scrolledtext, messagebox
from services.article_service import article_service


class ReadView:
    def __init__(self, root, article, change_to_articles_view):
        self._root = root
        self._article = article
        self._change_to_articles_view = change_to_articles_view
        self._frame = None

        self._initialize()

    def pack(self):
        self._frame.pack(fill=constants.X)

    def destroy(self):
        self._frame.destroy()

    def _initialize_article(self, article):
        title_label = ttk.Label(
            master=self._frame,
            text=article.title,
            font=("Times New Roman", 16, "bold"),
            wraplength=300
        )
        title_label.grid(row=1, column=1, padx=10,
                         pady=5, sticky=constants.EW)

        url_label = ttk.Label(
            master=self._frame,
            text=article.url
        )

        url_label.grid(row=2, column=1, padx=10, pady=5, sticky=constants.EW)

        content_text = scrolledtext.ScrolledText(
            master=self._frame,
            wrap="word",
            font=("Times New Roman", 10),
            background="#F1F8F2",
            padx=5,
            pady=5
        )

        content_text.insert("1.0", article.content)
        content_text.config(state="disabled")
        content_text.grid(row=3, column=1, padx=10,
                          pady=5, sticky=constants.EW)

    def _confirm_delete(self):
        if messagebox.askyesno("confirm delete", f"delete '{self._article.title}'?"):
            article_service.remove_article(self._article.id)
            self._change_to_articles_view()

    def _initialize_header(self):
        header_frame = ttk.Frame(master=self._frame)
        header_frame.grid(row=0, column=0, columnspan=2, sticky=constants.W)

        back_button = ttk.Button(
            master=header_frame,
            text="back",
            command=self._change_to_articles_view
        )

        back_button.grid(
            row=0,
            column=0,
            padx=5,
            pady=10,
            sticky=constants.W
        )

        delete_button = ttk.Button(
            master=header_frame,
            text="delete article",
            command=self._confirm_delete
        )

        delete_button.grid(
            row=0,
            column=1,
            padx=5,
            pady=10,
            sticky=constants.W
        )

    def _initialize(self):
        self._frame = ttk.Frame(master=self._root)

        self._initialize_header()
        self._initialize_article(self._article)

        self._frame.grid_columnconfigure(0, weight=1)
        self._frame.grid_columnconfigure(1, weight=2)
        self._frame.grid_columnconfigure(2, weight=1)
