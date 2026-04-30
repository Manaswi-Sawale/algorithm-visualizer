import tkinter as tk
from tkinter import ttk

ALGO_LIST = ["Bubble Sort", "Selection Sort", "Insertion Sort",
             "Merge Sort", "Quick Sort", "Heap Sort", "Shell Sort",
             "Counting Sort", "Linear Search", "Binary Search", "Jump Search"]

SEARCH_ALGOS = ("Binary Search", "Linear Search", "Jump Search")

STYLE = {"bg": "#1e1e2e", "fg": "#cdd6f4", "font": ("Segoe UI", 10)}
BTN_STYLE = {"bg": "#45475a", "fg": "#cdd6f4", "font": ("Segoe UI", 10, "bold"),
             "activebackground": "#585b70", "activeforeground": "#cdd6f4",
             "relief": tk.FLAT, "padx": 10, "pady": 4}


class ControlPanel(tk.Frame):
    def __init__(self, parent, on_generate, on_start, on_stop):
        super().__init__(parent, bg="#1e1e2e")
        self.pack(side=tk.TOP, fill=tk.X, padx=10, pady=8)

        tk.Label(self, text="Algorithm:", **STYLE).pack(side=tk.LEFT, padx=(0, 5))
        self.algo_var = tk.StringVar(value="Bubble Sort")
        combo = ttk.Combobox(self, textvariable=self.algo_var, width=16,
                             state="readonly", values=ALGO_LIST)
        combo.pack(side=tk.LEFT, padx=5)
        combo.bind("<<ComboboxSelected>>", self._on_algo_change)

        tk.Label(self, text="Size:", **STYLE).pack(side=tk.LEFT, padx=(15, 5))
        self.size_var = tk.IntVar(value=30)
        tk.Scale(self, from_=10, to=100, orient=tk.HORIZONTAL, variable=self.size_var,
                 bg="#1e1e2e", fg="#cdd6f4", troughcolor="#313244",
                 highlightthickness=0, length=100).pack(side=tk.LEFT, padx=5)

        tk.Label(self, text="Speed:", **STYLE).pack(side=tk.LEFT, padx=(15, 5))
        self.speed_var = tk.IntVar(value=50)
        tk.Scale(self, from_=1, to=100, orient=tk.HORIZONTAL, variable=self.speed_var,
                 bg="#1e1e2e", fg="#cdd6f4", troughcolor="#313244",
                 highlightthickness=0, length=100).pack(side=tk.LEFT, padx=5)

        tk.Button(self, text="Generate", command=on_generate, **BTN_STYLE).pack(side=tk.LEFT, padx=10)
        tk.Button(self, text="▶ Start", command=on_start, **BTN_STYLE).pack(side=tk.LEFT, padx=5)
        tk.Button(self, text="■ Stop", command=on_stop, **BTN_STYLE).pack(side=tk.LEFT, padx=5)

        self.target_label = tk.Label(self, text="Target:", **STYLE)
        self.target_var = tk.StringVar(value="")
        self.target_entry = tk.Entry(self, textvariable=self.target_var, width=5,
                                     bg="#313244", fg="#cdd6f4",
                                     insertbackground="#cdd6f4", font=("Segoe UI", 10))

    def _on_algo_change(self, _=None):
        if self.algo_var.get() in SEARCH_ALGOS:
            self.target_label.pack(side=tk.LEFT, padx=(15, 5))
            self.target_entry.pack(side=tk.LEFT)
        else:
            self.target_label.pack_forget()
            self.target_entry.pack_forget()

    @property
    def speed(self):
        return 1.0 - (self.speed_var.get() / 100) * 0.995
