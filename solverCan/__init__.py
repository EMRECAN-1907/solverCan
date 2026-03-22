"""
solverCan - Mathematical Function Solver from Dataset

Find equations from data using forward differences, derivative ratios, 
and piecewise polynomial approximation.

Usage:
    import solverCan

    y = [14, 13, 14, 17, 22, 29, 38, 49, 62, 77]

    result = solverCan.plynm(y)        # Polynomial
    result = solverCan.expo(y)         # Exponential
    result = solverCan.trig(y)         # Trigonometric (piecewise)
    result = solverCan.irrational(y)   # Irrational (piecewise)
    result = solverCan.auto(y)         # Auto-select best method

    print(result['equation'])          # The equation
    print(result['compute'](15))       # Predict x=15
    print(result['method'])            # Which method was used

    solverCan.table(y, result['compute'])                # Comparison table
    solverCan.compare_graph(y, result['compute'])        # Comparison chart
"""

__version__ = "0.1.0"

from .polynomial import solve as _poly_solve
from .exponential import solve as _expo_solve
from .piecewise import solve as _piecewise_solve
from .iterative import solve as _iter_solve
from .viz import compare_graph, table
from .core import compute_deviation


def plynm(y, x=None):
    """
    Find polynomial equation from dataset.
    
    Args:
        y: list of values
        x: list of x values (default: 1, 2, 3, ...)
    
    Returns:
        dict: equation, compute, coefficients, degree, method
    """
    return _poly_solve(y, x)


def expo(y, x=None):
    """
    Find exponential equation from dataset using derivative ratios.
    
    Args:
        y: list of values
        x: list of x values (default: 1, 2, 3, ...)
    
    Returns:
        dict or None: equation, compute, parts, method
    """
    return _expo_solve(y, x)


def trig(y, x=None, threshold=5.0):
    """
    Find trigonometric approximation using piecewise polynomials.
    
    Args:
        y: list of values
        x: list of x values (default: 1, 2, 3, ...)
        threshold: max deviation % per piece (default: 5.0)
    
    Returns:
        dict: equation, compute, pieces, method
    """
    return _piecewise_solve(y, x, threshold)


def trigOneEq(y, x=None, max_iter=None):
    """
    Find trigonometric approximation as a SINGLE combined equation.
    Uses iterative polynomial correction: f1 + f2 + ... = ftotal.
    
    Args:
        y: list of values
        x: list of x values (default: 1, 2, 3, ...)
        max_iter: max iterations (default: None = auto, or set 2,3,4... for fixed)
    
    Returns:
        dict: equation, compute, coefficients, iterations, method
    """
    return _iter_solve(y, x, max_iter=max_iter)


def irrational(y, x=None, threshold=5.0):
    """
    Find irrational function approximation using piecewise polynomials.
    
    Args:
        y: list of values
        x: list of x values (default: 1, 2, 3, ...)
        threshold: max deviation % per piece (default: 5.0)
    
    Returns:
        dict: equation, compute, pieces, method
    """
    return _piecewise_solve(y, x, threshold)


def irrationalOneEq(y, x=None, max_iter=None):
    """
    Find irrational function approximation as a SINGLE combined equation.
    Uses iterative polynomial correction: f1 + f2 + ... = ftotal.
    
    Args:
        y: list of values
        x: list of x values (default: 1, 2, 3, ...)
        max_iter: max iterations (default: None = auto, or set 2,3,4... for fixed)
    
    Returns:
        dict: equation, compute, coefficients, iterations, method
    """
    return _iter_solve(y, x, max_iter=max_iter)


def auto(y, x=None, threshold=5.0):
    """
    Automatically find the best equation from dataset.
    Tries all methods, picks the one with lowest max deviation.
    
    Args:
        y: list of values
        x: list of x values (default: 1, 2, 3, ...)
        threshold: deviation threshold for piecewise (default: 5.0)
    
    Returns:
        dict: equation, compute, method, all_results
    """
    if x is None:
        x = list(range(1, len(y) + 1))

    candidates = {}

    # 1. Polynomial
    try:
        r = _poly_solve(y, x)
        if r:
            candidates['polynomial'] = r
    except:
        pass

    # 2. Exponential
    try:
        r = _expo_solve(y, x)
        if r:
            candidates['exponential'] = r
    except:
        pass

    # 3. Iterative (single equation)
    try:
        r = _iter_solve(y, x)
        if r:
            candidates['iterative'] = r
    except:
        pass

    # 4. Piecewise
    try:
        r = _piecewise_solve(y, x, threshold)
        if r:
            candidates['piecewise'] = r
    except:
        pass

    if not candidates:
        return None

    # Evaluate each on training data
    scores = {}
    for name, result in candidates.items():
        try:
            predicted = [result['compute'](xi) for xi in x]
            devs = compute_deviation(y, predicted)
            scores[name] = max(devs)
        except:
            scores[name] = float('inf')

    # Pick best (lowest max deviation)
    best_name = min(scores, key=lambda k: scores[k])
    best = candidates[best_name]

    # Add comparison info
    best['all_results'] = {
        name: {
            'method': candidates[name]['method'],
            'max_deviation': scores[name]
        }
        for name in candidates
    }

    return best
