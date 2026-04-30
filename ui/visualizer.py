import tkinter as tk
from tkinter import messagebox
import random
import time

from ui.controls import ControlPanel, SEARCH_ALGOS
from ui.canvas import ArrayCanvas
from algorithms import (bubble_sort, selection_sort, insertion_sort,
                        merge_sort, quick_sort, heap_sort, shell_sort,
                        counting_sort, linear_search, binary_search, jump_search)

SORT_MAP = {
    "Bubble Sort": bubble_sort,
    "Selection Sort": selection_sort,
    "Insertion Sort": insertion_sort,
    "Merge Sort": merge_sort,
    "Quick Sort": quick_sort,
    "Heap Sort": heap_sort,
    "Shell Sort": shell_sort,
    "Counting Sort": counting_sort,
}

SEARCH_MAP = {
    "Linear Search": linear_search,
    "Binary Search": binary_search,
    "Jump Search": jump_search,
}


class AlgorithmVisualizer:
    def __init__(self, root):
        self.root = root
        self.root.title("Algorithm Visualizer")
        self.root.geometry("900x650")
        self.root.configure(bg="#1e1e2e")

        self.array = []
        self.running = False

        self.controls = ControlPanel(root, self.generate_array, self.start, self.stop)
        self.canvas = ArrayCanvas(root)

        self.status_var = tk.StringVar(value="Ready. Click Generate to create an array.")
        tk.Label(root, textvariable=self.status_var, bg="#313244", fg="#a6adc8",
                 font=("Segoe UI", 10), anchor=tk.W, padx=10, pady=4
                 ).pack(side=tk.BOTTOM, fill=tk.X)

        self.generate_array()

    def generate_array(self):
        self.running = False
        n = self.controls.size_var.get()
        self.array = random.sample(range(1, n + 1), n)
        self.canvas.draw(self.array, ["#89b4fa"] * n)
        self.status_var.set(f"Array generated with {n} elements. Select an algorithm and click Start.")

    def stop(self):
        self.running = False

    def start(self):
        if self.running:
            return
        if not self.array:
            messagebox.showwarning("No Array", "Click 'Generate' to create an array first.")
            return

        algo = self.controls.algo_var.get()

        if algo in SEARCH_ALGOS:
            target = self._validate_target()
            if target is None:
                return

        self.running = True
        self.status_var.set(f"Running {algo}...")

        if algo in SORT_MAP:
            self._run_sort(SORT_MAP[algo])
        elif algo in SEARCH_MAP:
            if algo in ("Binary Search", "Jump Search"):
                self.array.sort()
                self.canvas.draw(self.array, ["#89b4fa"] * len(self.array))
                time.sleep(0.5)
            self._run_search(SEARCH_MAP[algo], target)

        if not self.running:
            self.status_var.set("Stopped.")
        self.running = False

    def _validate_target(self):
        raw = self.controls.target_var.get().strip()
        if not raw:
            messagebox.showwarning("Missing Target", "Please enter a target number in the Target field.")
            return None
        try:
            target = int(raw)
        except ValueError:
            messagebox.showerror("Invalid Target", f"'{raw}' is not a valid integer. Enter a whole number.")
            return None
        n = self.controls.size_var.get()
        if target < 1 or target > n:
            messagebox.showwarning("Out of Range", f"Target must be between 1 and {n} (current array size).")
            return None
        return target

    def _run_sort(self, algo_func):
        for colors, callouts, status in algo_func(self.array):
            if not self.running:
                return
            self.status_var.set(status)
            self.canvas.draw(self.array, colors, callouts)
            time.sleep(self.controls.speed)

    def _run_search(self, algo_func, target):
        for colors, callouts, status, found in algo_func(self.array, target):
            if not self.running:
                return
            self.status_var.set(status)
            self.canvas.draw(self.array, colors, callouts)
            if found:
                messagebox.showinfo("Found", status)
                return
            time.sleep(self.controls.speed)
        # last yield was "not found"
        messagebox.showinfo("Not Found", f"Target {target} is not in the array.")
