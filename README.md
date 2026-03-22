# solverCan
Mathematical Function Solver from Dataset by Emrecan Bayhan.
Find equations from raw data using forward differences and derivative ratio analysis.

# solverCan

**Mathematical Function Solver from Dataset**
*by Emrecan Bayhan*

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.19167599.svg)](https://doi.org/10.5281/zenodo.19167599)

Find equations from raw data using forward differences, derivative ratio analysis, and piecewise polynomial approximation.

## Installation
```
pip install solverCan
```

## Quick Start
```python
import solverCan

y = [14, 13, 14, 17, 22, 29, 38, 49, 62, 77]
result = solverCan.auto(y)
print(result['equation'])       # f(x) = x^2 - 4*x + 17
print(result['compute'](15))    # 182.0
```

## Methods

### 1. Polynomial
```python
r = solverCan.plynm(y)
print(r['equation'])        # f(x) = x^2 - 4*x + 17
print(r['degree'])          # 2
print(r['coefficients'])    # [17, -4, 1]
```

### 2. Exponential
```python
y = [50000.0, 51522.73, 53091.83, 54708.71, 56374.84,
     58091.71, 59860.87, 61683.9, 63562.46, 65498.22]
r = solverCan.expo(y)
print(r['equation'])        # f(x) = 48512.25*exp(0.03*x) + 10.36
```

### 3. Trigonometric (Piecewise)
```python
y = [200, 217.02, 232.95, 247.47, 260.31, 271.19, 279.9, 286.26,
     290.12, 291.42, 290.12, 286.26, 279.9, 271.19, 260.31, 247.47,
     232.95, 217.02, 200]
x = list(range(0, 95, 5))
r = solverCan.trig(y, x=x)
print(r['equation'])        # Two pieces
```

### 4. Trigonometric (Single Equation)
```python
r = solverCan.trigOneEq(y, x=x)              # auto iterations
r = solverCan.trigOneEq(y, x=x, max_iter=2)  # fixed 2 iterations
print(r['equation'])
print(r['iterations'])
```

### 5. Irrational (Piecewise)
```python
y = [24.0, 26.5858, 31.2679, 38.0, 46.7639,
     57.5505, 70.3542, 85.1716, 102.0, 120.8377]
r = solverCan.irrational(y)
print(r['equation'])
```

### 6. Irrational (Single Equation)
```python
r = solverCan.irrationalOneEq(y)
r = solverCan.irrationalOneEq(y, max_iter=3)  # fixed iterations
```

### 7. Auto (Best Method)
```python
r = solverCan.auto(y)
print(r['method'])          # Polynomial (degree 2)
print(r['equation'])
for name, info in r['all_results'].items():
    print(f"  {name}: {info['method']} (max dev: {info['max_deviation']:.4f}%)")
```

## Visualization

### Comparison Table
```python
solverCan.table(y, r['compute'])
```

### Comparison Graph
```python
solverCan.compare_graph(y, r['compute'])
solverCan.compare_graph(y, r['compute'], title="My Analysis")
solverCan.compare_graph(y, r['compute'], save_as="output.png")
```

## Custom X Values
```python
x = [0, 5, 10, 15, 20]
y = [100, 250, 380, 470, 520]
r = solverCan.auto(y, x=x)
```

## Prediction
```python
r = solverCan.auto(y)
print(r['compute'](15))     # Predict at x=15
for x in range(11, 21):
    print(f"  x={x}: {r['compute'](x):.4f}")
```

## Result Fields

All methods return a dict:

| Field | Description |
|-------|------------|
| `r['equation']` | Equation string |
| `r['compute'](x)` | Predict value at x |
| `r['method']` | Method name |
| `r['coefficients']` | Polynomial coefficients (plynm, OneEq) |
| `r['degree']` | Polynomial degree (plynm) |
| `r['parts']` | Exponential parts (expo) |
| `r['pieces']` | Piecewise segments (trig, irrational) |
| `r['iterations']` | Iteration count (OneEq) |
| `r['all_results']` | All methods comparison (auto) |

## How It Works

1. **Forward Differences** — Detects polynomial degree via CV analysis
2. **Gauss Elimination** — Solves linear system for polynomial coefficients
3. **Derivative Ratios** — Constant ratio = exponential function (e^ax)
4. **Iterative Correction** — Find f1, compute residual, find f2, sum together
5. **Piecewise Splitting** — Split at deviation breakpoints, fit each segment

## Citation

If you use solverCan in your research, please cite:

```
Bayhan, E. (2026). solverCan: A Mathematical Function Solver from Dataset Using 
Forward Differences, Derivative Ratio Analysis, and Iterative Residual Correction. 
Zenodo. https://doi.org/10.5281/zenodo.19167599
```

## Author

**Emrecan Bayhan**
Email: bayhan.emrecan1@gmail.com