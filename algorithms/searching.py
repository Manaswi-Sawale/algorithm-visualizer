"""Search algorithm generators. Each yields (colors, callouts, status_text, found?) for visualization."""


def linear_search(array, target):
    n = len(array)
    for i in range(n):
        colors = ["#45475a"] * n
        for k in range(i):
            colors[k] = "#f38ba8"
        colors[i] = "#f9e2af"
        for k in range(i + 1, n):
            colors[k] = "#89b4fa"

        if array[i] == target:
            colors[i] = "#a6e3a1"
            callouts = [(i, f"** FOUND {target} **", "#a6e3a1")]
            if i > 0:
                callouts.append((0, f"x {i} checked", "#f38ba8"))
            yield colors, callouts, f"FOUND! Target {target} at index {i} in {i + 1} steps.", True
            return
        else:
            remaining = n - i - 1
            callouts = [
                (i, f"? {array[i]} != {target}", "#f9e2af"),
            ]
            if i > 0:
                callouts.append((0, f"x {i} skipped", "#f38ba8"))
            if remaining > 0 and i + 1 < n:
                callouts.append((n - 1, f"{remaining} left", "#89b4fa"))
            yield colors, callouts, f"Step {i + 1}/{n}: {array[i]} != {target}, moving on...", False

    yield ["#f38ba8"] * n, None, f"NOT FOUND: Target {target} not in array ({n} checked).", False


def binary_search(array, target):
    n = len(array)
    lo, hi = 0, n - 1
    step = 0

    while lo <= hi:
        step += 1
        mid = (lo + hi) // 2
        window = hi - lo + 1

        colors = ["#45475a"] * n
        for k in range(lo, hi + 1):
            colors[k] = "#89b4fa"
        colors[mid] = "#f9e2af"

        if array[mid] == target:
            colors[mid] = "#a6e3a1"
            callouts = [
                (mid, f"** FOUND {target} **", "#a6e3a1"),
                (lo, f"lo={lo}", "#89b4fa"),
                (hi, f"hi={hi}", "#89b4fa"),
            ]
            yield colors, callouts, f"FOUND! Target {target} at index {mid} in {step} steps.", True
            return
        elif array[mid] < target:
            callouts = [
                (mid, f"{array[mid]} < {target} -> go RIGHT -->", "#f9e2af"),
                (lo, f"lo={lo}", "#89b4fa"),
                (hi, f"hi={hi}", "#89b4fa"),
            ]
            yield colors, callouts, f"Step {step}: {array[mid]} < {target} -> search right (window={window})", False
            lo = mid + 1
        else:
            callouts = [
                (mid, f"{array[mid]} > {target} -> go LEFT <--", "#f9e2af"),
                (lo, f"lo={lo}", "#89b4fa"),
                (hi, f"hi={hi}", "#89b4fa"),
            ]
            yield colors, callouts, f"Step {step}: {array[mid]} > {target} -> search left (window={window})", False
            hi = mid - 1

    yield ["#f38ba8"] * n, None, f"NOT FOUND: Target {target} not in array after {step} steps.", False


def jump_search(array, target):
    import math
    n = len(array)
    jump = int(math.sqrt(n))
    prev = 0
    step = 0

    while prev < n and array[min(jump, n) - 1] < target:
        step += 1
        colors = ["#45475a"] * n
        block_end = min(jump, n) - 1
        for k in range(prev, block_end + 1):
            colors[k] = "#89b4fa"
        colors[block_end] = "#f9e2af"
        for k in range(prev):
            colors[k] = "#f38ba8"
        callouts = [
            (block_end, f"{array[block_end]} < {target} -> jump", "#f9e2af"),
            (prev, f"block [{prev}..{block_end}]", "#89b4fa"),
        ]
        yield colors, callouts, f"Step {step}: block [{prev}..{block_end}], {array[block_end]} < {target} -> jump ahead", False
        prev = jump
        jump += int(math.sqrt(n))

    for i in range(prev, min(jump, n)):
        step += 1
        colors = ["#45475a"] * n
        for k in range(prev):
            colors[k] = "#f38ba8"
        for k in range(prev, min(jump, n)):
            colors[k] = "#89b4fa"
        colors[i] = "#f9e2af"

        if array[i] == target:
            colors[i] = "#a6e3a1"
            callouts = [(i, f"** FOUND {target} **", "#a6e3a1")]
            yield colors, callouts, f"FOUND! Target {target} at index {i} in {step} steps.", True
            return
        elif array[i] > target:
            callouts = [(i, f"{array[i]} > {target} -> stop", "#f9e2af")]
            yield colors, callouts, f"Step {step}: {array[i]} > {target} -> not in array", False
            break
        else:
            callouts = [
                (i, f"? {array[i]} != {target}", "#f9e2af"),
            ]
            yield colors, callouts, f"Step {step}: linear scan, {array[i]} != {target}", False

    yield ["#f38ba8"] * n, None, f"NOT FOUND: Target {target} not in array after {step} steps.", False
