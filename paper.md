---
title: 'solverCan: A Mathematical Function Solver from Dataset Using Forward Differences, Derivative Ratio Analysis, and Iterative Residual Correction'
tags:
  - Python
  - numerical analysis
  - function approximation
  - forward differences
  - polynomial fitting
authors:
  - name: Emrecan Bayhan
    affiliation: 1
affiliations:
  - name: Independent Researcher
    index: 1
date: 22 March 2026
bibliography: paper.bib
---

# Summary

`solverCan` is a Python library that automatically identifies the underlying mathematical function from raw numerical data, without requiring prior knowledge of the function type. Given a small dataset of 7–10 points, the library detects whether the data follows a polynomial, exponential, trigonometric, or irrational pattern and returns an explicit, human-readable equation.

# Statement of Need

Determining the underlying mathematical function from observed data is a fundamental problem in numerical analysis, engineering, and data science. Existing tools such as `scipy.optimize.curve_fit` require the user to specify the function form in advance, while machine learning approaches produce black-box models that require large datasets. `solverCan` addresses these limitations by providing a fully automated pipeline that requires no prior knowledge of the function type and works with as few as 7–10 data points.

# Methods

The library implements four core methods:

**Forward Difference Analysis**: For a polynomial of degree $n$, the $n$-th forward difference yields a constant. The Coefficient of Variation (CV) is computed at each difference level to detect the polynomial degree automatically.

**Gaussian Elimination**: Once the degree is determined, an $(n+1) \times (n+1)$ linear system is constructed and solved via Gaussian elimination with partial pivoting to extract polynomial coefficients.

**Derivative Ratio Analysis**: For exponential functions $f(x) = A \cdot e^{ax} + c$, the ratio of consecutive forward differences is constant ($e^a$). When the CV of these ratios falls below 0.1%, an exponential structure is confirmed and the parameter $a = \ln(\text{ratio})$ is extracted.

**Iterative Residual Correction**: For complex functions, the library finds a polynomial approximation $f_1(x)$, computes the residual $r(x) = y - f_1(x)$, fits another polynomial to the residual, and sums the results. This process repeats until convergence.

The `auto()` function tries all methods and returns the one with the lowest maximum deviation on the training data.

# Results

Table 1 summarizes the performance of `solverCan` on various function types using 10 data points:

| Function Type | Example | Method | Max Deviation |
|---|---|---|---|
| Polynomial | $x^2 - 4x + 17$ | Polynomial (deg 2) | 0.00% |
| Exponential | $100 - 100e^{-0.06x}$ | Derivative Ratios | 0.003% |
| Trigonometric | $(10+10\cos a)(10+10\sin a)$ | Piecewise (2 pieces) | 2.11% |
| Mixed | $24x^3 + \sin(x)$ | Iterative (2 iter) | 0.0002% |

# Availability

`solverCan` is open source under the MIT License and available on PyPI:

```
pip install solverCan
```

Source code: https://github.com/EMRECAN-1907/solverCan

# References
