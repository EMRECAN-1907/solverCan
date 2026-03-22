"""Exponential method - derivative ratio analysis."""

import math
from .core import forward_diff, compute_cv


def solve(y, x=None):
    """
    Find exponential equation from dataset using derivative ratios.

    Args:
        y: list of values
        x: list of x values (default: 1, 2, 3, ...)

    Returns:
        dict or None
    """
    if x is None:
        x = list(range(1, len(y) + 1))

    parts = []
    residual = list(y)
    best_dev = float('inf')
    best_parts = []

    for _ in range(10):
        ratio, level = _find_best_ratio(residual)
        if ratio is None:
            break

        try:
            a = math.log(ratio)
            temp = list(residual)
            for _ in range(level):
                temp = forward_diff(temp)
            K = temp[0] / math.exp(a * x[0])
            A = K / (a ** level)
            c = residual[0] - A * math.exp(a * x[0])
        except:
            break

        parts.append((A, a, c))
        residual = [residual[i] - (A * math.exp(a * x[i]) + c) for i in range(len(x))]

        # Check deviation
        max_dev = 0
        for i in range(len(x)):
            total = sum(Ai * math.exp(ai * x[i]) + ci for Ai, ai, ci in parts)
            if abs(y[i]) > 1e-10:
                dev = abs(total - y[i]) / abs(y[i]) * 100
                if dev > max_dev:
                    max_dev = dev

        if max_dev < best_dev:
            best_dev = max_dev
            best_parts = list(parts)

        if max_dev < 0.01:
            break
        if max_dev > best_dev * 1.5 and len(parts) > 1:
            parts = best_parts
            break
        if max(abs(r) for r in residual) < 1e-8:
            break

    if not parts:
        return None

    # Merge same-a parts
    groups = {}
    for A, a, c in parts:
        key = round(a, 6)
        if key in groups:
            gA, gc = groups[key]
            groups[key] = (gA + A, gc + c)
        else:
            groups[key] = (A, c)

    merged = [(A, a, c) for a, (A, c) in groups.items()]

    # Build equation string
    terms = []
    total_const = sum(c for _, _, c in merged)
    for A, a, c in merged:
        if abs(A) > 1e-10:
            terms.append(f"{A:.4f}*exp({a:.6f}*x)")
    if abs(total_const) > 1e-6:
        terms.append(f"{total_const:.4f}")
    eq_str = " + ".join(terms).replace("+ -", "- ")

    def compute_fn(val, p=merged):
        return sum(A * math.exp(a * val) + c for A, a, c in p)

    return {
        'equation': f"f(x) = {eq_str}",
        'compute': compute_fn,
        'parts': merged,
        'method': f'Exponential ({len(parts)} iterations)'
    }


def _find_best_ratio(values):
    """Find best constant ratio in derivative levels."""
    current = list(values)
    best_cv = float('inf')
    best_ratio = None
    best_level = None

    for level in range(1, len(current) - 1):
        current = forward_diff(current)
        if len(current) < 3:
            break

        ratios = []
        valid = True
        for i in range(len(current) - 1):
            if abs(current[i]) < 1e-15:
                valid = False
                break
            ratios.append(current[i + 1] / current[i])

        if not valid or len(ratios) < 2:
            continue

        avg = sum(ratios) / len(ratios)
        if abs(avg) < 1e-15 or avg <= 0:
            continue

        std = (sum((r - avg) ** 2 for r in ratios) / len(ratios)) ** 0.5
        cv = (std / abs(avg)) * 100

        if cv < best_cv:
            best_cv = cv
            best_ratio = avg
            best_level = level

        if cv < 0.1:
            break

    if best_ratio is not None and best_cv < 15.0:
        return best_ratio, best_level
    return None, None
