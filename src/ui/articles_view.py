from tkinter import ttk, constants, Canvas, messagebox
from services.article_service import article_service


class ArticleListView:
    """Artikkelilistasta vastaava näkymä."""

    def __init__(self, root, articles, show_article_view):
        """Luokan konstruktori. Luo uuden listanäkymän.

        Args:
            root:
                Tkinter-elementti, jonka sisään näkymä alustetaan.
            articles:
                Lista Article-olioita, jotka näytetään näkymässä.
            show_article_view:
                Kutsuttava funktio, jota kutsutaan artikkelin otsikkoa klikatessa. Saa argumentiksi Article-olion.
        """

        self._root = root
        self._articles = articles
        self._show_article_view = show_article_view
        self._frame = None
        self._canvas = None
        self._list_frame = None
        self._scrollbar = None

        self._initialize()

    def pack(self):
        """Näyttää näkymän."""
        self._frame.pack(fill=constants.X)

    def destroy(self):
        """Tuhoaa näkymän."""
        self._frame.destroy()

    def _initialize_article_item(self, article, index):
        item_frame = ttk.Frame(master=self._list_frame)

        bg_color = "#F2F2F2" if index % 2 == 0 else "#FFFFFF"

        label = ttk.Label(
            master=item_frame,
            text=article.title,
            wraplength=400,
            background=bg_color,
            cursor="hand2",
            padding=5
        )
        label.grid(row=0, column=0, sticky=constants.EW)

        label.bind("<Button-1>", lambda e: self._show_article_view(article.id))
        item_frame.grid_columnconfigure(0, weight=1)

        item_frame.pack(fill=constants.X)

    def _on_canvas_configure(self, event=None):
        self._canvas.itemconfig(self._list_frame_window,
                                width=self._canvas.winfo_width())

    def _initialize(self):
        self._frame = ttk.Frame(master=self._root)
        self._canvas = Canvas(self._frame, bg="#D3D3D3")
        self._list_frame = ttk.Frame(self._canvas)
        self._scrollbar = ttk.Scrollbar(
            self._frame, command=self._canvas.yview)

        self._canvas.configure(yscrollcommand=self._scrollbar.set)

        articles_label = ttk.Label(
            master=self._frame,
            text="articles",
            font=('Times', '16', 'bold')
        )

        articles_label.pack(pady=5, anchor=constants.W)

        self._scrollbar.pack(side=constants.RIGHT, fill=constants.Y)
        self._canvas.pack(side=constants.LEFT,
                          fill=constants.BOTH, expand=True)

        self._list_frame_window = self._canvas.create_window(
            (0, 0),
            window=self._list_frame,
            anchor=constants.NW
        )

        self._canvas.bind("<Configure>", self._on_canvas_configure)

        for index, article in enumerate(self._articles):
            self._initialize_article_item(article, index)

        self._frame.pack(fill=constants.BOTH, expand=True)

        self._canvas.update_idletasks()
        self._canvas.config(scrollregion=self._canvas.bbox("all"))


class ArticlesView:
    """Sovelluksen päänäkymä, joka vastaa artikkelien listauksesta ja sovelluksen navigaatiosta"""

    def __init__(self, root, show_search_view, show_article_view, show_create_view):
        """Luokan konsttruktori. Luo uuden päänäkymän.

        Args:
            root:
                Tkinter-elementti, jonka sisään näkymä alustetaan.
            show_search_view:
                Kutsuttava funktio, joka vaihtaa näkymän etsimis-näkymään.
            show_article_view:
                Kutsuttava funktio, jota kutsutaan artikkelin otsikkoa klikatessa. Saa argumentiksi artikkelin id-arvon.
            show_create_view:
                Kutsuttava funktio, joka vaihtaa näkymän artikkelin luonti-näkymään
        """

        self._root = root
        self._frame = None
        self._articles = []
        self._show_search_view = show_search_view
        self._show_article_view = show_article_view
        self._show_create_view = show_create_view
        self._article_list_frame = None
        self._article_list_view = None

        self._initialize()

    def pack(self):
        """Näyttää näkymän"""
        self._frame.pack(fill=constants.X)

    def destroy(self):
        """Tuhoaa näkymän"""
        self._frame.destroy()

    def _initialize_article_list(self, filtered_articles=None):
        if self._article_list_view:
            self._article_list_view.destroy()

        if filtered_articles is None:
            print("fetching articles from db")
            articles = article_service.get_all_articles()
            self._articles = articles
        else:
            articles = filtered_articles

        self._article_list_view = ArticleListView(
            self._article_list_frame,
            articles,
            self._show_article_view
        )

        self._article_list_view.pack()

    def _on_clear_article_list(self):
        if messagebox.askyesno("confirm delete", "delete all articles?"):
            article_service.remove_all_articles()
            self._initialize_article_list()

    def _on_filter_change(self, filter_text):
        if len(self._articles) == 0:
            return

        if not filter_text.strip():
            self._initialize_article_list(self._articles)
            return

        filtered_articles = article_service.filter_articles(
            self._articles,
            filter_text
        )
        self._initialize_article_list(filtered_articles)

    def _initialize_filter_field(self):
        placeholder_text = "filter articles"

        filter_entry = ttk.Entry(
            master=self._frame,
            width=15,
            foreground="gray"
        )

        filter_entry.insert(0, placeholder_text)

        def on_focus_in(event):
            if filter_entry.get() == "filter articles":
                filter_entry.delete(0, constants.END)
                filter_entry.config(foreground="black")

        def on_focus_out(event):
            if not filter_entry.get():
                filter_entry.insert(0, placeholder_text)
                filter_entry.config(foreground="gray")

        filter_entry.bind("<FocusIn>", on_focus_in)
        filter_entry.bind("<FocusOut>", on_focus_out)
        filter_entry.bind(
            "<KeyRelease>", lambda e: self._on_filter_change(filter_entry.get()))

        filter_entry.grid(
            row=1,
            column=1,
            sticky=constants.E
        )

    def _initialize_header(self):
        header_frame = ttk.Frame(master=self._frame)
        header_frame.grid(row=0, column=0, columnspan=3, sticky=constants.EW)

        search_page_button = ttk.Button(
            master=header_frame,
            text="find articles",
            command=self._show_search_view
        )

        search_page_button.grid(
            row=0,
            column=0,
            padx=5,
            pady=5,
            sticky=constants.W
        )

        create_page_button = ttk.Button(
            master=header_frame,
            text="create article",
            command=self._show_create_view
        )

        create_page_button.grid(
            row=0,
            column=1,
            padx=5,
            pady=5,
            sticky=constants.W
        )

    def _initialize(self):
        self._frame = ttk.Frame(master=self._root)
        self._article_list_frame = ttk.Frame(master=self._frame)

        self._initialize_header()
        self._initialize_article_list()
        self._initialize_filter_field()

        self._article_list_frame.grid(
            row=2,
            column=1,
            sticky=constants.EW
        )

        clear_list_button = ttk.Button(
            master=self._frame,
            text="clear articles",
            command=self._on_clear_article_list
        )

        clear_list_button.grid(
            row=3,
            column=1,
            padx=5,
            pady=5,
            sticky=constants.E
        )

        self._frame.grid_columnconfigure(0, weight=1)
        self._frame.grid_columnconfigure(1, weight=2)
        self._frame.grid_columnconfigure(2, weight=1)
