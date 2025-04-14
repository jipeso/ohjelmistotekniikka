from tkinter import ttk, constants, scrolledtext, messagebox
from services.article_service import article_service
import webbrowser


class ReadView:
    def __init__(self, root, article, show_articles_view):
        self._root = root
        self._article = article
        self._show_articles_view = show_articles_view
        self._frame = None
        self._is_editing = False

        self._initialize()

    def pack(self):
        self._frame.pack(fill=constants.X)

    def destroy(self):
        self._frame.destroy()

    def _on_link_click(self, url):
        if not self._is_editing and url:
            try:
                webbrowser.open_new(url)
            except Exception:
                messagebox.showError("could not open URL")

    def _initialize_article(self, article):
        title_label = ttk.Label(
            master=self._frame,
            text=article.title,
            font=("Times", 16, "bold"),
            wraplength=400
        )
        title_label.grid(row=1, column=1, padx=10,
                         pady=5, sticky=constants.EW)

        url_label = ttk.Label(
            master=self._frame,
            text=article.url,
            cursor="hand2",
            foreground="blue"
        )
        url_label.bind("<Button-1>", lambda e: self._on_link_click(article.url))

        url_label.grid(row=2, column=1, padx=10, pady=5, sticky=constants.EW)    

        content_text = scrolledtext.ScrolledText(
            master=self._frame,
            wrap="word",
            font=("Times", 12),
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
            self._show_articles_view()

    def _on_edit_button_click(self):
        pass


    def _initialize_header(self):
        header_frame = ttk.Frame(master=self._frame)
        header_frame.grid(row=0, column=0, columnspan=3, sticky=constants.EW)

        back_button = ttk.Button(
            master=header_frame,
            text="back",
            command=self._show_articles_view
        )

        back_button.grid(
            row=0,
            column=0,
            padx=5,
            pady=10,
            sticky=constants.W
        )

        edit_button = ttk.Button(
            master=header_frame,
            text="modify article",
            command=self._on_edit_button_click
        )

        edit_button.grid(
            row=0,
            column=1,
            padx=5,
            pady=5,
            sticky=constants.W
        )

        delete_button = ttk.Button(
            master=header_frame,
            text="delete article",
            command=self._confirm_delete
        )

        delete_button.grid(
            row=0,
            column=2,
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

class EditView:
    def __init__(self, root, article, show_read_view):
        self._root = root
        self._article = article
        self._show_read_view = show_read_view
        self._frame = None

        self._title_entry = None
        self._url_entry = None
        self._content_text = None

        self._initialize()

    def pack(self):
        self._frame.pack(fill=constants.X)

    def destroy(self):
        self._frame.destroy()

    def _initialize_fields(self):
        title_label = ttk.Label(self._frame, text="title")
        self._title_entry = ttk.Entry(self._frame)
        self._title_entry.insert(0, self.article.url)

        url_label = ttk.Label(self._frame, text="url")
        self._url_entry = ttk.Entry(self._frame)
        self._url_entry.insert(0, self.article.url)

        content_label = ttk.Label(self._frame, text="content")
        self._content_text = scrolledtext.ScrolledText(
            master=self._frame,
            wrap="word",
            font=("Times", 12),
            background="#FFFFFF",
            padx=5,
            pady=5,
            height=15
        )
        self._content_text.insert("1.0", self._original_content)

        button_frame = ttk.Frame(self._frame)

        save_button = ttk.Button(
            master=button_frame,
            text="save Changes",
            command=self._save_changes
        )
        cancel_button = ttk.Button(
            master=button_frame,
            text="cancel",
            command=self._cancel_changes
        )

        title_label.grid(row=0, column=0, padx=(10, 2), pady=5, sticky=constants.W)
        self._title_entry.grid(row=0, column=1, padx=(0, 10), pady=5, sticky=constants.EW)

        url_label.grid(row=1, column=0, padx=(10, 2), pady=5, sticky=constants.W)
        self._url_entry.grid(row=1, column=1, padx=(0, 10), pady=5, sticky=constants.EW)

        content_label.grid(row=2, column=0, padx=(10, 2), pady=5, sticky=constants.NW)
        self._content_text.grid(row=2, column=1, padx=(0, 10), pady=5, sticky=constants.NSEW)

        button_frame.grid(row=3, column=0, columnspan=2, padx=10, pady=10, sticky=constants.E)
        save_button.grid(row=0, column=0, padx=5)
        cancel_button.grid(row=0, column=1, padx=5)

        self._frame.grid_columnconfigure(1, weight=1)
        self._frame.grid_rowconfigure(2, weight=1)

    def _initialize(self):
        self._frame = ttk.Frame(master=self._root)
        self._initialize_fields()
       