# Algorithm Visualizer

A desktop application built with Python, Tkinter, and Matplotlib that visualizes sorting and searching algorithms step-by-step with animated bar charts, color-coded comparisons, and expressive annotations.

![Python](https://img.shields.io/badge/Python-3.8%2B-blue)
![Tkinter](https://img.shields.io/badge/GUI-Tkinter-green)
![Matplotlib](https://img.shields.io/badge/Charts-Matplotlib-orange)

---

## Features

- **8 Sorting Algorithms** — Bubble, Selection, Insertion, Merge, Quick, Heap, Shell, Counting Sort
- **3 Searching Algorithms** — Linear, Binary, Jump Search
- Real-time animated bar chart visualization
- Color-coded bars showing comparisons, swaps, sorted regions, and boundaries
- Expressive text callouts on bars (e.g. `5 > 3 SWAP`, `*pivot=7*`, `shift -->`)
- Adjustable array size (10–100) and animation speed
- Start/Stop controls
- Status bar with step-by-step explanations

---

## Project Structure

```
algorithm-visualizer/
├── main.py                  # Entry point — run this
├── requirements.txt         # Python dependencies
├── README.md
├── algorithms/
│   ├── __init__.py          # Re-exports all algorithm functions
│   ├── sorting.py           # Sorting algorithm generators
│   └── searching.py         # Searching algorithm generators
└── ui/
    ├── __init__.py
    ├── controls.py          # Control panel (combobox, sliders, buttons)
    ├── canvas.py            # Matplotlib bar chart drawing logic
    └── visualizer.py        # Main orchestrator — ties UI + algorithms
```

### Architecture

Algorithms are **generator functions** that yield visualization state at each step. They have zero knowledge of the UI — they just yield data. The visualizer iterates the generator and draws each frame.

```
[ Algorithm Generators ]  →  yield (colors, callouts, status)  →  [ Visualizer ]  →  [ Canvas ]
```

This means:
- Algorithms are independently unit-testable (pure logic, no UI)
- Adding a new algorithm requires no changes to the drawing or control code
- UI changes don't affect algorithm logic

### Application Flow

Below is the end-to-end execution path from startup to a completed visualization.

```
main.py
  │
  ├─ Creates Tk root window
  └─ Instantiates AlgorithmVisualizer (ui/visualizer.py)
       │
       ├─ ControlPanel (ui/controls.py)    ← algorithm dropdown, size/speed sliders, buttons
       ├─ ArrayCanvas  (ui/canvas.py)      ← Matplotlib bar chart embedded in Tkinter
       ├─ Status bar label                 ← step-by-step text updates
       └─ Calls generate_array()           ← creates initial random array
```

**1. Generate** — User clicks Generate (or app starts):
```
generate_array()
  ├─ Creates a shuffled array of [1..n] using random.sample()
  ├─ Draws all bars in blue (#89b4fa) via ArrayCanvas.draw()
  └─ Updates status bar: "Array generated with n elements."
```

**2. Start (Sorting)** — User clicks Start with a sorting algorithm selected:
```
start()
  ├─ Looks up the generator function from SORT_MAP (e.g. "Bubble Sort" → bubble_sort)
  └─ _run_sort(algo_func)
       └─ for colors, callouts, status in algo_func(array):
            ├─ Updates status bar text
            ├─ ArrayCanvas.draw(array, colors, callouts)
            │    ├─ Clears axes, redraws bars with per-bar colors
            │    ├─ Adds annotated callouts (arrows + text) on highlighted bars
            │    └─ canvas.draw() + root.update() to render the frame
            └─ time.sleep(speed) to control animation pace
```

**3. Start (Searching)** — User clicks Start with a search algorithm selected:
```
start()
  ├─ Validates target input (must be integer in [1..n])
  ├─ If Binary Search or Jump Search → sorts the array first
  ├─ Looks up the generator function from SEARCH_MAP
  └─ _run_search(algo_func, target)
       └─ for colors, callouts, status, found in algo_func(array, target):
            ├─ Updates status bar text
            ├─ ArrayCanvas.draw(array, colors, callouts)
            ├─ If found == True → shows "Found" messagebox and returns
            └─ time.sleep(speed)
       └─ If generator exhausts without found → shows "Not Found" messagebox
```

**4. Stop** — User clicks Stop at any time:
```
stop()
  └─ Sets self.running = False
       └─ The active _run_sort / _run_search loop checks this flag
            each iteration and exits early if False
```

**Generator ↔ Visualizer contract:**
```
┌──────────────────────┐       yield (colors, callouts, status)      ┌────────────────┐
│  Algorithm Generator │ ─────────────────────────────────────────▶  │  Visualizer    │
│  (sorting.py /       │                                             │  _run_sort()   │
│   searching.py)      │  ◀── next() called each iteration ────────  │  _run_search() │
└──────────────────────┘                                             └──────┬─────────┘
                                                                            │
                                                                            ▼
                                                                     ┌───────────────┐
                                                                     │ ArrayCanvas   │
                                                                     │  .draw()      │
                                                                     │ (Matplotlib)  │
                                                                     └───────────────┘
```

The generator never imports or references any UI code — it only yields data tuples. The visualizer is the sole consumer that translates those tuples into visual frames.

---

## Getting Started

### Prerequisites

- Python 3.8 or higher
- Tkinter (included with most Python installations)

### Installation

```bash
# Clone or download the project
cd algorithm-visualizer

# Install dependencies
pip install -r requirements.txt
```

### Running

```bash
python main.py
```

---

## How to Use

1. **Select an algorithm** from the dropdown menu
2. **Adjust array size** using the Size slider (10–100 elements)
3. **Adjust speed** using the Speed slider (left = slow, right = fast)
4. Click **Generate** to create a new random array
5. Click **Start** to begin the visualization
6. Click **Stop** at any time to halt the animation

### For Search Algorithms

- When you select Linear Search, Binary Search, or Jump Search, a **Target** input field appears
- Enter a number between 1 and the array size
- Binary Search and Jump Search will automatically sort the array before searching

### Color Legend

| Color | Meaning |
|-------|---------|
| Blue (`#89b4fa`) | Unsorted / unchecked elements |
| Red/Pink (`#f38ba8`) | Currently being compared |
| Yellow (`#f9e2af`) | Key element (pivot, min, mid, current check) |
| Green (`#a6e3a1`) | Sorted / confirmed in place |
| Purple (`#cba6f7`) | Partition boundary (Quick Sort) |
| Dark Gray (`#45475a`) | Eliminated / out of search range |

---

## Supported Algorithms

### Sorting

| Algorithm | Time (Best) | Time (Avg) | Time (Worst) | Space |
|-----------|-------------|------------|--------------|-------|
| Bubble Sort | O(n) | O(n²) | O(n²) | O(1) |
| Selection Sort | O(n²) | O(n²) | O(n²) | O(1) |
| Insertion Sort | O(n) | O(n²) | O(n²) | O(1) |
| Merge Sort | O(n log n) | O(n log n) | O(n log n) | O(n) |
| Quick Sort | O(n log n) | O(n log n) | O(n²) | O(log n) |
| Heap Sort | O(n log n) | O(n log n) | O(n log n) | O(1) |
| Shell Sort | O(n log n) | O(n^1.25) | O(n²) | O(1) |
| Counting Sort | O(n + k) | O(n + k) | O(n + k) | O(k) |

### Searching

| Algorithm | Time (Best) | Time (Avg) | Time (Worst) | Requires Sorted |
|-----------|-------------|------------|--------------|-----------------|
| Linear Search | O(1) | O(n) | O(n) | No |
| Binary Search | O(1) | O(log n) | O(log n) | Yes |
| Jump Search | O(1) | O(√n) | O(√n) | Yes |

---

## How to Add a New Algorithm

Adding a new algorithm takes 3 simple steps:

### Step 1: Write the Generator

**For a sorting algorithm** — add to `algorithms/sorting.py`:

```python
def my_sort(array):
    n = len(array)
    # your sorting logic here...
    for each_visual_step:
        colors = ["#89b4fa"] * n          # color per bar
        colors[i] = "#f38ba8"             # highlight active elements
        callouts = [                       # text annotations on bars
            (i, "some label", "#f38ba8"),
        ]
        status = "Description of current step"
        yield colors, callouts, status

    # final frame — all green
    yield ["#a6e3a1"] * n, None, "My Sort complete! Array is sorted."
```

**For a searching algorithm** — add to `algorithms/searching.py`:

```python
def my_search(array, target):
    n = len(array)
    # your search logic here...
    for each_visual_step:
        colors = ["#89b4fa"] * n
        colors[i] = "#f9e2af"
        callouts = [(i, f"checking {array[i]}", "#f9e2af")]
        status = "Description of current step"

        if array[i] == target:
            colors[i] = "#a6e3a1"
            callouts = [(i, f"** FOUND {target} **", "#a6e3a1")]
            yield colors, callouts, "Found!", True    # True = found
            return

        yield colors, callouts, status, False         # False = not found yet

    # not found
    yield ["#f38ba8"] * n, None, "Not found.", False
```

### Step 2: Export It

In `algorithms/__init__.py`, add the import:

```python
from .sorting import my_sort       # for sorting
from .searching import my_search   # for searching
```

### Step 3: Register It

**In `ui/controls.py`:**
- Add the name to `ALGO_LIST`
- If it's a search algorithm, add it to `SEARCH_ALGOS`

**In `ui/visualizer.py`:**
- Import it
- Add it to `SORT_MAP` or `SEARCH_MAP`
- If the search requires a sorted array, add its name to the pre-sort condition:
  ```python
  if algo in ("Binary Search", "Jump Search", "My Search"):
  ```

That's it — no changes needed to the canvas, drawing logic, or control panel wiring.

### Generator Yield Format

**Sorting algorithms** yield 3 values per step:
```python
yield colors, callouts, status_text
# colors:    list of hex color strings, one per bar
# callouts:  list of (index, text, color) tuples, or None
# status:    string shown in the status bar
```

**Searching algorithms** yield 4 values per step:
```python
yield colors, callouts, status_text, found
# found:     True if target was found at this step, False otherwise
```

---

## Dependencies

- **matplotlib** — bar chart rendering via `FigureCanvasTkAgg`
- **tkinter** — GUI framework (bundled with Python)

Install with:
```bash
pip install -r requirements.txt
```

---

## License

This project is part of an Intern Spot Project.
