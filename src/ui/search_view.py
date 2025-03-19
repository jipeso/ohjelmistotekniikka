from tkinter import ttk, constants


class SearchView:
    def __init__(self, root, handle_search, change_to_articles_view):
        self._root = root
        self._handle_search = handle_search
        self._change_to_articles_view = change_to_articles_view
        self._frame = None
        self._search_input = None

        self._initialize()

    def pack(self):
        self._frame.pack(fill=constants.X)

    def destroy(self):
        self._frame.destroy()

    def _initialize_search_field(self):
        search_label = ttk.Label(
            master=self._frame, text="Search for articles")

        self._search_input = ttk.Entry(master=self._frame)

        search_label.grid(column=1, row=1, padx=10,
                          pady=10, sticky=constants.W)
        self._search_input.grid(column=1, row=2, padx=10,
                                pady=10, sticky=constants.W)

    def _initialize(self):
        self._frame = ttk.Frame(master=self._root)

        back_button = ttk.Button(
            master=self._frame,
            text="back to articles",
            command=self._change_to_articles_view
        )
        back_button.grid(row=0, column=0, padx=10, pady=10, sticky=constants.W)

        self._initialize_search_field()

        search_button = ttk.Button(
            master=self._frame,
            text="Search",
            command=self._handle_search
        )

        search_button.grid(column=1, row=3, padx=10,
                           pady=10, sticky=constants.W)

        self._frame.grid_columnconfigure(0, weight=1, minsize=150)
        self._frame.grid_columnconfigure(1, weight=2, minsize=300)
        self._frame.grid_columnconfigure(2, weight=1, minsize=150)
