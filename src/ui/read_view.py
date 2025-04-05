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
        back_button = ttk.Button(
            master=self._frame,
            text="back",
            command=self._change_to_articles_view
        )
        back_button.grid(row=0, column=0, padx=10, pady=10, sticky=constants.W)

        title_label = ttk.Label(
            master=self._frame,
            text=article.title,
            font=("Times New Roman", 16, "bold"),
            wraplength=300
        )
        title_label.grid(row=1, column=1, padx=10,
                         pady=10, sticky=constants.EW)

        content_text = scrolledtext.ScrolledText(
            master=self._frame,
            wrap="word",
            font=("Times New Roman", 12),
            background="#F1F8F2",
            padx=10,
            pady=10
        )

        content_text.insert("1.0", article.content)
        content_text.config(state="disabled")
        content_text.grid(row=2, column=1, padx=10,
                          pady=10, sticky=constants.EW)

        def confirm_delete():
            if messagebox.askyesno("confirm delete", f"delete '{article.title}'?"):
                article_service.remove_article(article.id)
                self._change_to_articles_view()

        delete_button = ttk.Button(
            master=self._frame,
            text="delete article",
            command=confirm_delete
        )

        delete_button.grid(row=0, column=1, padx=10,
                           pady=10, sticky=constants.E)

    def _initialize(self):
        self._frame = ttk.Frame(master=self._root)

        self._initialize_article(self._article)

        self._frame.grid_columnconfigure(0, weight=1, minsize=150)
        self._frame.grid_columnconfigure(1, weight=2, minsize=300)
        self._frame.grid_columnconfigure(2, weight=1, minsize=150)

        self._frame.grid_rowconfigure(3, weight=1)
