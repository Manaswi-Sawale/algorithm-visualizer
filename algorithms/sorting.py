"""Sorting algorithm generators. Each yields (colors, callouts, status_text) for visualization."""


def bubble_sort(array):
    a = array
    n = len(a)
    for i in range(n - 1):
        for j in range(n - 1 - i):
            colors = ["#89b4fa"] * n
            colors[j] = "#f38ba8"
            colors[j + 1] = "#f38ba8"
            if a[j] > a[j + 1]:
                callouts = [
                    (j, f"[{a[j]}] > [{a[j+1]}] SWAP", "#f38ba8"),
                    (j + 1, f"<--", "#f38ba8"),
                ]
                status = f"Comparing {a[j]} > {a[j+1]} -> Swap!"
                a[j], a[j + 1] = a[j + 1], a[j]
                colors[j] = "#a6e3a1"
                colors[j + 1] = "#a6e3a1"
                callouts = [
                    (j, f"{a[j]} OK", "#a6e3a1"),
                    (j + 1, f"{a[j+1]} OK", "#a6e3a1"),
                ]
            else:
                callouts = [
                    (j, f"L: {a[j]}", "#f38ba8"),
                    (j + 1, f"R: {a[j+1]}", "#f38ba8"),
                ]
                status = f"Comparing {a[j]} <= {a[j+1]} -> No swap"
            yield colors, callouts, status
    yield ["#a6e3a1"] * n, None, "Bubble Sort complete! Array is sorted."


def selection_sort(array):
    a = array
    n = len(a)
    for i in range(n - 1):
        min_idx = i
        for j in range(i + 1, n):
            colors = ["#a6e3a1"] * i + ["#89b4fa"] * (n - i)
            colors[min_idx] = "#f9e2af"
            colors[j] = "#f38ba8"
            tag = " << new min!" if a[j] < a[min_idx] else ""
            callouts = [
                (min_idx, f"*min={a[min_idx]}*", "#f9e2af"),
                (j, f"check: {a[j]}{tag}", "#f38ba8"),
            ]
            status = f"Pass {i+1}: Current min={a[min_idx]} at [{min_idx}], checking {a[j]} at [{j}]"
            yield colors, callouts, status
            if a[j] < a[min_idx]:
                min_idx = j
        colors = ["#a6e3a1"] * i + ["#89b4fa"] * (n - i)
        colors[i] = "#a6e3a1"
        colors[min_idx] = "#a6e3a1"
        callouts = [
            (i, f"<-- {a[min_idx]}", "#a6e3a1"),
            (min_idx, f"--> {a[i]}", "#a6e3a1"),
        ]
        status = f"Pass {i+1}: Swapping {a[i]} <-> {a[min_idx]} (min found at [{min_idx}])"
        a[i], a[min_idx] = a[min_idx], a[i]
        yield colors, callouts, status
    yield ["#a6e3a1"] * n, None, "Selection Sort complete! Array is sorted."


def insertion_sort(array):
    a = array
    n = len(a)
    for i in range(1, n):
        key = a[i]
        j = i - 1
        while j >= 0 and a[j] > key:
            a[j + 1] = a[j]
            colors = ["#a6e3a1"] * (j + 1) + ["#89b4fa"] * (n - j - 1)
            colors[j + 1] = "#f38ba8"
            colors[j] = "#f9e2af"
            callouts = [
                (j, f"{a[j]} > key({key})", "#f9e2af"),
                (j + 1, f"shift -->", "#f38ba8"),
            ]
            yield colors, callouts, f"Key={key}: shifting {a[j]} right (key < {a[j]})"
            j -= 1
        a[j + 1] = key
        colors = ["#a6e3a1"] * (i + 1) + ["#89b4fa"] * (n - i - 1)
        callouts = [(j + 1, f"[insert {key}]", "#a6e3a1")]
        yield colors, callouts, f"Placed key={key} at index {j+1}"
    yield ["#a6e3a1"] * n, None, "Insertion Sort complete! Array is sorted."


def _merge_sort_helper(array, left, right):
    if left >= right:
        return
    mid = (left + right) // 2
    yield from _merge_sort_helper(array, left, mid)
    yield from _merge_sort_helper(array, mid + 1, right)
    yield from _merge(array, left, mid, right)


def _merge(array, left, mid, right):
    merged = []
    i, j = left, mid + 1
    while i <= mid and j <= right:
        if array[i] <= array[j]:
            merged.append(array[i])
            i += 1
        else:
            merged.append(array[j])
            j += 1
    merged.extend(array[i:mid + 1])
    merged.extend(array[j:right + 1])

    total = len(merged)
    for k, val in enumerate(merged):
        array[left + k] = val
        colors = ["#89b4fa"] * len(array)
        colors[left + k] = "#f9e2af"
        for idx in range(left, left + k):
            colors[idx] = "#a6e3a1"
        callouts = [
            (left + k, f"place {val} ({k+1}/{total})", "#f9e2af"),
        ]
        if left + k > left:
            callouts.append((left, f"merge [{left}..{right}]", "#a6e3a1"))
        yield colors, callouts, f"Merging [{left}..{mid}] + [{mid+1}..{right}]: placing {val} at [{left+k}]"

    colors = ["#89b4fa"] * len(array)
    for idx in range(left, right + 1):
        colors[idx] = "#a6e3a1"
    callouts = [(left, f"-- merged [{left}..{right}] --", "#a6e3a1")]
    yield colors, callouts, f"Merged [{left}..{right}] complete"


def merge_sort(array):
    yield from _merge_sort_helper(array, 0, len(array) - 1)
    yield ["#a6e3a1"] * len(array), None, "Merge Sort complete! Array is sorted."


def _partition(array, low, high):
    pivot = array[high]
    i = low - 1
    for j in range(low, high):
        colors = ["#89b4fa"] * len(array)
        colors[high] = "#f9e2af"
        colors[j] = "#f38ba8"
        if i >= low:
            colors[i] = "#cba6f7"
        if array[j] <= pivot:
            callouts = [
                (high, f"*pivot={pivot}*", "#f9e2af"),
                (j, f"{array[j]} <= {pivot} -> LEFT", "#f38ba8"),
            ]
            if i >= low:
                callouts.append((i, "<- boundary", "#cba6f7"))
            status = f"Pivot={pivot}: {array[j]} <= pivot -> swap to left side"
            i += 1
            array[i], array[j] = array[j], array[i]
        else:
            callouts = [
                (high, f"*pivot={pivot}*", "#f9e2af"),
                (j, f"{array[j]} > {pivot} -> RIGHT", "#f38ba8"),
            ]
            if i >= low:
                callouts.append((i, "<- boundary", "#cba6f7"))
            status = f"Pivot={pivot}: {array[j]} > pivot -> stays right"
        yield colors, callouts, status
    array[i + 1], array[high] = array[high], array[i + 1]
    colors = ["#89b4fa"] * len(array)
    colors[i + 1] = "#a6e3a1"
    callouts = [(i + 1, f"pivot {pivot} LOCKED at [{i+1}]", "#a6e3a1")]
    yield colors, callouts, f"Pivot {pivot} placed at final position [{i + 1}]"
    yield i + 1


def _quick_sort_helper(array, low, high):
    if low >= high:
        return
    pivot_idx = None
    for step in _partition(array, low, high):
        if isinstance(step, int):
            pivot_idx = step
        else:
            yield step
    if pivot_idx is not None:
        yield from _quick_sort_helper(array, low, pivot_idx - 1)
        yield from _quick_sort_helper(array, pivot_idx + 1, high)


def quick_sort(array):
    yield from _quick_sort_helper(array, 0, len(array) - 1)
    yield ["#a6e3a1"] * len(array), None, "Quick Sort complete! Array is sorted."


def _heapify(array, n, i):
    largest = i
    left = 2 * i + 1
    right = 2 * i + 2

    if left < n and array[left] > array[largest]:
        largest = left
    if right < n and array[right] > array[largest]:
        largest = right

    if largest != i:
        colors = ["#89b4fa"] * len(array)
        colors[i] = "#f38ba8"
        colors[largest] = "#f9e2af"
        callouts = [
            (i, f"parent={array[i]}", "#f38ba8"),
            (largest, f"child={array[largest]} > {array[i]} SWAP", "#f9e2af"),
        ]
        yield colors, callouts, f"Heapify: {array[largest]} > {array[i]} -> swap [{i}] <-> [{largest}]"
        array[i], array[largest] = array[largest], array[i]
        yield from _heapify(array, n, largest)


def heap_sort(array):
    n = len(array)
    for i in range(n // 2 - 1, -1, -1):
        yield from _heapify(array, n, i)
    colors = ["#f9e2af"] * n
    callouts = [(0, f"max={array[0]}", "#f9e2af")]
    yield colors, callouts, "Max-heap built! Now extracting elements..."

    for i in range(n - 1, 0, -1):
        colors = ["#89b4fa"] * n
        for k in range(i + 1, n):
            colors[k] = "#a6e3a1"
        colors[0] = "#f38ba8"
        colors[i] = "#f9e2af"
        callouts = [
            (0, f"max={array[0]}", "#f38ba8"),
            (i, f"swap -> end", "#f9e2af"),
        ]
        yield colors, callouts, f"Extract max={array[0]}: swap [{0}] <-> [{i}]"
        array[0], array[i] = array[i], array[0]
        yield from _heapify(array, i, 0)
    yield ["#a6e3a1"] * n, None, "Heap Sort complete! Array is sorted."


def shell_sort(array):
    a = array
    n = len(a)
    gap = n // 2
    while gap > 0:
        for i in range(gap, n):
            key = a[i]
            j = i
            while j >= gap and a[j - gap] > key:
                colors = ["#89b4fa"] * n
                colors[j] = "#f38ba8"
                colors[j - gap] = "#f9e2af"
                callouts = [
                    (j - gap, f"{a[j-gap]} > key({key})", "#f9e2af"),
                    (j, f"shift (gap={gap})", "#f38ba8"),
                ]
                yield colors, callouts, f"Gap={gap}: shifting {a[j-gap]} right, key={key}"
                a[j] = a[j - gap]
                j -= gap
            a[j] = key
            colors = ["#89b4fa"] * n
            colors[j] = "#a6e3a1"
            callouts = [(j, f"[insert {key}]", "#a6e3a1")]
            yield colors, callouts, f"Gap={gap}: placed key={key} at [{j}]"
        gap //= 2
    yield ["#a6e3a1"] * n, None, "Shell Sort complete! Array is sorted."


def counting_sort(array):
    a = array
    n = len(a)
    if n == 0:
        return
    max_val = max(a)
    count = [0] * (max_val + 1)

    for i in range(n):
        count[a[i]] += 1
        colors = ["#89b4fa"] * n
        colors[i] = "#f9e2af"
        callouts = [(i, f"count[{a[i]}]++", "#f9e2af")]
        yield colors, callouts, f"Counting: increment count[{a[i]}] (now={count[a[i]]})"

    idx = 0
    for val in range(max_val + 1):
        for _ in range(count[val]):
            a[idx] = val
            colors = ["#89b4fa"] * n
            colors[idx] = "#a6e3a1"
            for k in range(idx):
                colors[k] = "#a6e3a1"
            callouts = [(idx, f"place {val} ({idx+1}/{n})", "#a6e3a1")]
            yield colors, callouts, f"Rebuilding: place {val} at [{idx}]"
            idx += 1
    yield ["#a6e3a1"] * n, None, "Counting Sort complete! Array is sorted."
