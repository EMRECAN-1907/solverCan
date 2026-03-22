"""Core mathematical utilities for solverCan."""

import math


def forward_diff(values):
    """Compute forward differences."""
    return [values[i + 1] - values[i] for i in range(len(values) - 1)]


def compute_cv(values):
    """Compute Coefficient of Variation (CV = sigma/mu * 100)."""
    n = len(values)
    if n == 0:
        return None, None, None
    mu = sum(abs(v) for v in values) / n
    if mu < 1e-15:
        return mu, 0.0, 0.0
    sigma = (sum((abs(v) - mu) ** 2 for v in values) / n) ** 0.5
    cv = (sigma / mu) * 100
    return mu, sigma, cv


def consecutive_ratios(values):
    """Compute consecutive ratios f(i+1)/f(i)."""
    ratios = []
    for i in range(len(values) - 1):
        if abs(values[i]) > 1e-15:
            ratios.append(values[i + 1] / values[i])
        else:
            ratios.append(None)
    return ratios


def gauss_elimination(A, b):
    """Solve Ax = b using Gaussian elimination."""
    n = len(b)
    mat = [A[i][:] + [b[i]] for i in range(n)]

    for col in range(n):
        max_row = col
        for row in range(col + 1, n):
            if abs(mat[row][col]) > abs(mat[max_row][col]):
                max_row = row
        mat[col], mat[max_row] = mat[max_row], mat[col]

        pivot = mat[col][col]
        if abs(pivot) < 1e-15:
            raise ValueError(f"Singular matrix at row {col}")

        for row in range(col + 1, n):
            factor = mat[row][col] / pivot
            for j in range(col, n + 1):
                mat[row][j] -= factor * mat[col][j]

    x = [0.0] * n
    for i in range(n - 1, -1, -1):
        total = mat[i][n]
        for j in range(i + 1, n):
            total -= mat[i][j] * x[j]
        x[i] = total / mat[i][i]
    return x


def poly_eval(coeffs, x):
    """Evaluate polynomial: coeffs = [a0, a1, a2, ...] -> a0 + a1*x + a2*x^2 + ..."""
    return sum(k * (x ** i) for i, k in enumerate(coeffs))


def poly_fit(x_vals, y_vals, degree):
    """Fit polynomial of given degree to data points."""
    n = degree + 1
    if len(x_vals) < n:
        n = len(x_vals)
    A = [[x_vals[i] ** j for j in range(n)] for i in range(n)]
    b = [y_vals[i] for i in range(n)]
    coeffs = gauss_elimination(A, b)
    for i in range(len(coeffs)):
        if abs(coeffs[i]) < 1e-12:
            coeffs[i] = 0.0
    return coeffs


def detect_degree(values, cv_threshold=2.0):
    """Detect polynomial degree using forward differences and CV analysis."""
    current = list(values)
    max_deg = len(values) - 4
    if max_deg < 1:
        max_deg = 1

    best_cv = float('inf')
    best_deg = 1
    deg = 0

    while True:
        current = forward_diff(current)
        deg += 1
        mu, sigma, cv = compute_cv(current)
        if mu is None:
            break
        if cv < best_cv and len(current) >= 3:
            best_cv = cv
            best_deg = deg
        if cv < cv_threshold and len(current) >= 3:
            return deg
        if len(current) <= 3 or deg >= max_deg:
            break

    return best_deg


def format_equation(coeffs):
    """Format polynomial coefficients into readable equation string."""
    terms = []
    for i in range(len(coeffs) - 1, -1, -1):
        k = coeffs[i]
        if abs(k) < 1e-12:
            continue

        neg = k < 0
        ak = abs(k)

        # Try fraction representation
        k_str = _simplify_coeff(ak)

        if i == 0:
            term = k_str
        elif i == 1:
            term = "x" if k_str == "1" else f"{k_str}*x"
        else:
            term = f"x^{i}" if k_str == "1" else f"{k_str}*x^{i}"

        if not terms:
            terms.append(f"-{term}" if neg else term)
        else:
            terms.append(f"- {term}" if neg else f"+ {term}")

    return " ".join(terms) if terms else "0"


def _simplify_coeff(k):
    """Simplify coefficient to integer or fraction if possible."""
    if abs(k - round(k)) < 1e-10:
        return str(int(round(k)))
    for denom in range(2, 10001):
        num = k * denom
        if abs(num - round(num)) < 1e-8:
            return f"{int(round(num))}/{denom}"
    return f"{k:.10f}".rstrip('0').rstrip('.')


def compute_deviation(y_true, y_pred):
    """Compute percentage deviation between true and predicted values."""
    deviations = []
    for yt, yp in zip(y_true, y_pred):
        if abs(yt) > 1e-10:
            deviations.append(abs(yp - yt) / abs(yt) * 100)
        else:
            deviations.append(0.0)
    return deviations
