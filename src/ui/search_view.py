from tkinter import ttk, constants

from services.feed_service import feed_service


class SearchView:
    def __init__(self, root, change_to_articles_view):
        self._root = root
        self._change_to_articles_view = change_to_articles_view
        self._frame = None
        self._search_input = None
        self._result_list_frame = None
        self._result_list_view = None

        self._initialize()

    def pack(self):
        self._frame.pack(fill=constants.X)

    def destroy(self):
        self._frame.destroy()

    def _initialize_feed_selector(self):
        feed_label = ttk.Label(
            master=self._frame, text="browse news pages"
        )
        feed_label.grid(row=1, column=2, padx=10, pady=10, sticky=constants.W)

        feeds = feed_service.get_all_feeds()
        feed_names = ["choose a feed..."] + [feed.name for feed in feeds]

        feed_selector = ttk.Combobox(
            master=self._frame,

            values=feed_names,
            state="readonly"
        )
        feed_selector.grid(row=2, column=2, padx=10,
                           pady=10, sticky=constants.W)
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

    def _initialize_search_field(self):
        search_label = ttk.Label(
            master=self._frame, text="search for articles")

        self._search_input = ttk.Entry(master=self._frame)

        search_label.grid(row=1, column=1, padx=10,
                          pady=10, sticky=constants.W)
        self._search_input.grid(row=2, column=1, padx=10,
                                pady=10, sticky=constants.W)

        search_button = ttk.Button(
            master=self._frame,
            text="search",
            command=self._handle_search
        )

        search_button.grid(row=3, column=1, padx=10,
                           pady=10, sticky=constants.W)

    def _initialize_result_list(self, articles):
        if self._result_list_view:
            self._result_list_view.destroy()

        self._result_list_view = ResultView(
            self._result_list_frame,
            articles
        )

        self._result_list_view.pack()

    def _handle_search(self):
        pass

    def _initialize(self):
        self._frame = ttk.Frame(master=self._root)
        self._result_list_frame = ttk.Frame(master=self._frame)

        back_button = ttk.Button(
            master=self._frame,
            text="articles page",
            command=self._change_to_articles_view
        )
        back_button.grid(row=0, column=0, padx=10, pady=10, sticky=constants.W)

        self._initialize_search_field()
        self._initialize_feed_selector()

        self._result_list_frame.grid(
            row=4, column=1, columnspan=2, sticky=constants.EW)

        self._frame.grid_columnconfigure(0, weight=1, minsize=150)
        self._frame.grid_columnconfigure(1, weight=1, minsize=150)
        self._frame.grid_columnconfigure(2, weight=1, minsize=150)
        self._frame.grid_columnconfigure(3, weight=1, minsize=150)


class ResultView:
    def __init__(self, root, articles):
        self._root = root
        self._articles = articles
        self._initialize()

    def pack(self):
        self._frame.pack(fill=constants.X)

    def destroy(self):
        self._frame.destroy()

    def _initialize_result_item(self, article, index):
        item_frame = ttk.Frame(master=self._frame)

        bg_color = "#f2f2f2" if index % 2 == 0 else "#ffffff"

        label = ttk.Label(
            master=item_frame,
            text=article.title,
            background=bg_color,
            cursor="hand2",
            padding=10
        )
        label.grid(row=0, column=0, sticky=constants.EW)

        item_frame.grid_columnconfigure(0, weight=1)

        item_frame.pack(fill=constants.X)

    def _initialize(self):
        self._frame = ttk.Frame(master=self._root)

        results_label = ttk.Label(
            master=self._frame,
            text="results",
            font=('Times', '16', 'bold')
        )

        results_label.pack(pady=20, anchor=constants.W)

        for index, article in enumerate(self._articles):
            self._initialize_result_item(article, index)
