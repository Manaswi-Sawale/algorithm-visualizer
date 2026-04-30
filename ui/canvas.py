import tkinter as tk
import matplotlib
matplotlib.use("TkAgg")
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


class ArrayCanvas:
    def __init__(self, parent):
        self.root = parent
        self.fig = Figure(figsize=(9, 5), facecolor="#1e1e2e")
        self.ax = self.fig.add_subplot(111)
        self._style_axes()

        self.canvas = FigureCanvasTkAgg(self.fig, master=parent)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True, padx=10, pady=(0, 10))

    def _style_axes(self):
        self.ax.set_facecolor("#1e1e2e")
        self.ax.tick_params(colors="#6c7086")
        for spine in self.ax.spines.values():
            spine.set_color("#45475a")

    def draw(self, array, colors, callouts=None):
        self.ax.clear()
        self._style_axes()
        self.ax.bar(range(len(array)), array, color=colors,
                    edgecolor="#1e1e2e", linewidth=0.5)
        self.ax.set_xlim(-0.5, len(array) - 0.5)
        ymax = max(array) if array else 1
        self.ax.set_ylim(0, ymax * 1.25)
        if callouts:
            for idx, text, clr in callouts:
                self.ax.annotate(text, xy=(idx, array[idx]),
                                 xytext=(0, 8), textcoords="offset points",
                                 ha="center", va="bottom", fontsize=8,
                                 fontweight="bold", color=clr,
                                 arrowprops=dict(arrowstyle="->", color=clr, lw=1.2))
        self.canvas.draw()
        self.root.update()
