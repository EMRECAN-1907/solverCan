"""Polynomial method - forward differences + Gauss elimination."""

from .core import forward_diff, compute_cv, poly_eval, poly_fit, detect_degree, format_equation


def solve(y, x=None):
    """
    Find polynomial equation from dataset.

    Args:
        y: list of values
        x: list of x values (default: 1, 2, 3, ...)

    Returns:
        dict with keys: equation, compute, coefficients, degree, method
    """
    if x is None:
        x = list(range(1, len(y) + 1))

    degree = detect_degree(y, cv_threshold=0.02)
    coeffs = poly_fit(x, y, degree)
    eq = format_equation(coeffs)

    return {
        'equation': f"f(x) = {eq}",
        'compute': lambda val, c=coeffs: poly_eval(c, val),
        'coefficients': coeffs,
        'degree': degree,
        'method': f'Polynomial (degree {degree})'
    }
