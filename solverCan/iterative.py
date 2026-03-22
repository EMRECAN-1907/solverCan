"""Iterative polynomial method - finds single combined equation by iterative correction."""

from .core import forward_diff, compute_cv, poly_eval, poly_fit, detect_degree, format_equation


def solve(y, x=None, cv_threshold=2.0, max_iter=None):
    """
    Find equation using iterative polynomial correction.
    Finds f1, computes residual, finds f2 from residual, sums: ftotal = f1 + f2 + ...
    Produces a SINGLE combined equation (not piecewise).

    Args:
        y: list of values
        x: list of x values (default: 1, 2, 3, ...)
        cv_threshold: CV threshold for degree detection (default: 2.0)
        max_iter: max iterations (default: None = auto, stops when residual ~0)

    Returns:
        dict with keys: equation, compute, coefficients, iterations, method
    """
    if x is None:
        x = list(range(1, len(y) + 1))

    limit = max_iter if max_iter is not None else 10
    parts = []
    residual = list(y)

    for iteration in range(1, limit + 1):
        degree = detect_degree(residual, cv_threshold)
        try:
            coeffs = poly_fit(x, residual, degree)
        except:
            break

        if all(abs(k) < 1e-10 for k in coeffs):
            break

        parts.append(list(coeffs))

        # Compute new residual
        new_residual = [residual[i] - poly_eval(coeffs, x[i]) for i in range(len(x))]
        max_res = max(abs(r) for r in new_residual)

        if max_res < 1e-8:
            break

        residual = new_residual

    if not parts:
        return None

    # Combine all parts into single polynomial
    max_deg = max(len(p) for p in parts)
    total_coeffs = [0.0] * max_deg
    for p in parts:
        for i, k in enumerate(p):
            total_coeffs[i] += k

    for i in range(len(total_coeffs)):
        if abs(total_coeffs[i]) < 1e-12:
            total_coeffs[i] = 0.0

    eq = format_equation(total_coeffs)

    return {
        'equation': f"f(x) = {eq}",
        'compute': lambda val, c=total_coeffs: poly_eval(c, val),
        'coefficients': total_coeffs,
        'iterations': len(parts),
        'method': f'Iterative Polynomial ({len(parts)} iterations)'
    }
