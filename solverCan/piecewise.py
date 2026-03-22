"""Piecewise method - splits range at deviation points, fits each piece."""

from .core import (forward_diff, compute_cv, poly_eval, poly_fit,
                   detect_degree, gauss_elimination, format_equation)


def solve(y, x=None, threshold=5.0):
    """
    Find piecewise polynomial equation from dataset.

    Args:
        y: list of values
        x: list of x values (default: 1, 2, 3, ...)
        threshold: max deviation % before splitting (default: 5.0)

    Returns:
        dict with keys: equation, compute, pieces, method
    """
    if x is None:
        x = list(range(1, len(y) + 1))

    pieces = []  # [(x_start, x_end, coeffs), ...]
    start_idx = 0
    n_train = min(10, len(y))

    while start_idx < len(y):
        end_idx = min(start_idx + n_train, len(y))
        x_seg = x[start_idx:end_idx]
        y_seg = y[start_idx:end_idx]

        if len(x_seg) < 3:
            if pieces:
                old = pieces[-1]
                pieces[-1] = (old[0], x[-1], old[2])
            break

        # Iterative polynomial fit
        coeffs = _iterative_fit(x_seg, y_seg)

        # Find valid range (check deviation)
        valid_end_idx = start_idx
        for idx in range(start_idx, len(y)):
            pred = poly_eval(coeffs, x[idx])
            actual = y[idx]
            dev = (abs(pred - actual) / abs(actual) * 100) if abs(actual) > 1e-10 else 0
            if dev > threshold:
                break
            valid_end_idx = idx

        pieces.append((x[start_idx], x[valid_end_idx], list(coeffs)))

        if valid_end_idx >= len(y) - 1:
            break

        new_start = valid_end_idx + 1
        if new_start <= start_idx:
            new_start = start_idx + max(3, n_train // 2)
        start_idx = new_start

        if len(pieces) >= 20:
            break

    if not pieces:
        return None

    # Build equation strings
    eq_parts = []
    for i, (xs, xe, c) in enumerate(pieces):
        eq_parts.append(f"f{i+1}(x) = {format_equation(c)}  [{xs}-{xe}]")

    def compute_fn(val, p=pieces):
        for xs, xe, c in p:
            if xs <= val <= xe:
                return poly_eval(c, val)
        return poly_eval(p[-1][2], val)

    return {
        'equation': "\n  ".join(eq_parts),
        'compute': compute_fn,
        'pieces': pieces,
        'method': f'Piecewise ({len(pieces)} pieces)'
    }


def _iterative_fit(x_vals, y_vals, cv_threshold=2.0, max_iter=10):
    """Iterative polynomial fitting with residual correction."""
    parts = []
    residual = list(y_vals)

    for _ in range(max_iter):
        degree = detect_degree(residual, cv_threshold)
        try:
            coeffs = poly_fit(x_vals, residual, degree)
        except:
            break

        if all(abs(k) < 1e-10 for k in coeffs):
            break

        parts.append(list(coeffs))
        new_res = [residual[i] - poly_eval(coeffs, x_vals[i]) for i in range(len(x_vals))]

        if max(abs(r) for r in new_res) < 1e-8:
            break
        residual = new_res

    if not parts:
        return [0.0]

    max_d = max(len(p) for p in parts)
    total = [0.0] * max_d
    for p in parts:
        for i, k in enumerate(p):
            total[i] += k

    for i in range(len(total)):
        if abs(total[i]) < 1e-12:
            total[i] = 0.0
    return total
