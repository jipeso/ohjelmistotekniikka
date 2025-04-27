from tkinter import ttk, constants, messagebox, Canvas

from services.feed_service import feed_service
from services.article_service import article_service


class SearchView:
    """Artikkelien etsimisestä vastaava näkymä"""

    def __init__(self, root, show_articles_view):
        """Luokan konstruktori. Luo uuden artikkelien etsimisnäkymän.

        Args:
            root:
                Tkinter-elementti, jonka sisään näkymä alustetaan.
            show_articles_view:
                Kutsuttava funktio, joka vaihtaa näkymän päänäkymään.
        """

        self._root = root
        self._show_articles_view = show_articles_view
        self._frame = None
        self._search_entry = None
        self._result_list_frame = None
        self._result_list_view = None

        self._initialize()

    def pack(self):
        """Näyttää näkymän."""
        self._frame.pack(fill=constants.X)

    def destroy(self):
        """Tuhoaa näkymän."""
        self._frame.destroy()

    def _initialize_feed_selector(self):
        feed_label = ttk.Label(
            master=self._frame, text="browse news pages"
        )
        feed_label.grid(row=1, column=1, pady=5, sticky=constants.W)

        feeds = feed_service.get_all_feeds()
        feed_names = ["choose a feed..."] + [feed.name for feed in feeds]

        feed_selector = ttk.Combobox(
            master=self._frame,

            values=feed_names,
            state="readonly",
        )

        feed_selector.grid(row=2, column=1, pady=5, sticky=constants.W)
        feed_selector.current(0)

        def on_select(event):
            feed_name = feed_selector.get()

            if feed_name == "choose a feed...":
                return

            selected_feed = next(
                (f for f in feeds if f.name == feed_name), None)

            if selected_feed:
                print("searching from this url:", selected_feed.url)
                articles = feed_service.parse_feed(selected_feed.url)

                if len(articles) > 0:
                    self._initialize_result_list(articles)

        feed_selector.bind("<<ComboboxSelected>>", on_select)

    def _initialize_header(self):
        header_frame = ttk.Frame(master=self._frame)
        header_frame.grid(row=0, column=0, columnspan=2, sticky=constants.EW)

        articles_page_button = ttk.Button(
            master=header_frame,
            text="back",
            command=self._show_articles_view
        )

        articles_page_button.grid(
            row=0,
            column=0,
            padx=5,
            pady=5,
            sticky=constants.W
        )

    def _initialize_result_list(self, articles):
        if self._result_list_view:
            self._result_list_view.destroy()

        self._result_list_view = ResultView(
            self._result_list_frame,
            articles,
            self._handle_add_article
        )

        self._result_list_view.pack()

    def _handle_add_article(self, article):
        if messagebox.askyesno("add to article list", f"add '{article.title}'?"):
            try:
                article_service.scrape_web_article(article.url)
                messagebox.showinfo(
                    "success", f"added article '{article.title}' ")
            except Exception:
                messagebox.showerror("fail", "failed to add article")
                print(f"could not scrape article from url: {article.url}")

    def _initialize(self):
        self._frame = ttk.Frame(master=self._root)
        self._result_list_frame = ttk.Frame(master=self._frame)

        self._initialize_header()
        self._initialize_feed_selector()

        self._result_list_frame.grid(
            row=4,
            column=1,
            columnspan=2,
            sticky=constants.EW
        )

        self._frame.grid_columnconfigure(0, weight=1)
        self._frame.grid_columnconfigure(1, weight=1)
        self._frame.grid_columnconfigure(2, weight=1)
        self._frame.grid_columnconfigure(3, weight=1)


class ResultView:
    """RSS-syötteen tuloksista vastaava näkymä."""

    def __init__(self, root, articles, handle_add_article):
        """Luokan konstruktori. Luo uuden tulokset-näkymän.

        Args:
            root:
                Tkinter-elementti, jonka sisään näkymä luodaan.
            articles:
                Lista Article-olioita, jotka näkymässä näytetään.
            handle_add_article:
                Kutsuttava funktio, jota kutsutaan klikatessa hakutuloslistan artikkelien otsikoita. Saa argumentiksi Article-olion.
        """

        self._root = root
        self._articles = articles
        self._handle_add_article = handle_add_article
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

    def _initialize_result_item(self, article, index):
        item_frame = ttk.Frame(master=self._list_frame)

        bg_color = "#f2f2f2" if index % 2 == 0 else "#ffffff"

        label = ttk.Label(
            master=item_frame,
            text=article.title,
            background=bg_color,
            cursor="hand2",
            wraplength=400,
            padding=5
        )
        label.grid(row=0, column=0, sticky=constants.EW)
        label.bind("<Button-1>", lambda e: self._handle_add_article(article))

        item_frame.grid_columnconfigure(0, weight=1)

        item_frame.pack(fill=constants.X)

    def _on_canvas_configure(self, event=None):
        self._canvas.itemconfig(self._list_frame_window,
                                width=self._canvas.winfo_width())

    def _initialize(self):
        self._frame = ttk.Frame(master=self._root)
        self._canvas = Canvas(self._frame)
        self._list_frame = ttk.Frame(self._canvas)
        self._scrollbar = ttk.Scrollbar(
            self._frame, command=self._canvas.yview)

        self._canvas.configure(yscrollcommand=self._scrollbar.set)

        results_label = ttk.Label(
            master=self._frame,
            text="results",
            font=('Times', '16', 'bold')
        )

        results_label.pack(pady=5, anchor=constants.W)

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
            self._initialize_result_item(article, index)

        self._frame.pack(fill=constants.BOTH, expand=True)

        self._canvas.update_idletasks()
        self._canvas.config(scrollregion=self._canvas.bbox("all"))
