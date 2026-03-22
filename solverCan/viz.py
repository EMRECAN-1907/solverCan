"""Visualization utilities - graphs and tables."""

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt


def compare_graph(y, compute_fn, x=None, title="solverCan", save_as=None, show=False):
    """
    Plot original data vs computed function.

    Args:
        y: original data
        compute_fn: function returned by solver (result['compute'])
        x: x values (default: 1, 2, ...)
        title: graph title
        save_as: filename to save (default: auto)
        show: if True, display graph (requires interactive backend)
    """
    if x is None:
        x = list(range(1, len(y) + 1))

    predicted = [compute_fn(xi) for xi in x]
    deviations = []
    for yt, yp in zip(y, predicted):
        if abs(yt) > 1e-10:
            deviations.append(abs(yp - yt) / abs(yt) * 100)
        else:
            deviations.append(0.0)

    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 8),
                                    gridspec_kw={'height_ratios': [3, 1]})

    # Upper: data vs fit
    ax1.scatter(x, y, color='#2196F3', s=60, zorder=5, label='Data',
               edgecolors='#0D47A1', linewidths=1)

    fit_x = []
    fit_y = []
    step = (x[-1] - x[0]) / 200
    val = x[0]
    while val <= x[-1]:
        fit_x.append(val)
        try:
            fit_y.append(compute_fn(val))
        except:
            fit_y.append(0)
        val += step

    ax1.plot(fit_x, fit_y, 'r-', linewidth=2, label='Fitted', zorder=3)
    ax1.set_ylabel('y')
    ax1.set_title(title, fontsize=13, fontweight='bold')
    ax1.legend(fontsize=9)
    ax1.grid(True, alpha=0.3)

    # Lower: deviation
    colors = ['red' if d > 5 else 'orange' if d > 2.5 else 'green' for d in deviations]
    ax2.bar(x, deviations, color=colors, alpha=0.7)
    ax2.axhline(y=5, color='red', linestyle='--', linewidth=1, label='5% threshold')
    ax2.set_xlabel('x')
    ax2.set_ylabel('Deviation (%)')
    ax2.legend(fontsize=9)
    ax2.grid(True, alpha=0.3)

    plt.tight_layout()

    if save_as is None:
        save_as = f"{title.replace(' ', '_')}_compare.png"
    plt.savefig(save_as, dpi=150, bbox_inches='tight')
    plt.close()

    if show:
        import os
        os.startfile(save_as) if os.name == 'nt' else os.system(f'open {save_as}')

    return save_as


def table(y, compute_fn, x=None):
    """
    Print comparison table: original vs computed.

    Args:
        y: original data
        compute_fn: function returned by solver (result['compute'])
        x: x values (default: 1, 2, ...)
    """
    if x is None:
        x = list(range(1, len(y) + 1))

    print(f"\n  {'x':>5} | {'Original':>14} | {'Computed':>14} | {'Diff':>14} | {'Dev %':>10}")
    print(f"  {'-'*65}")

    total_dev = 0
    max_dev = 0

    for i, xi in enumerate(x):
        try:
            pred = compute_fn(xi)
        except:
            pred = 0
        diff = abs(pred - y[i])
        dev = (diff / abs(y[i]) * 100) if abs(y[i]) > 1e-10 else 0
        total_dev += dev
        if dev > max_dev:
            max_dev = dev

        flag = " <<<" if dev > 5 else ""
        print(f"  {xi:>5} | {y[i]:>14.4f} | {pred:>14.4f} | {diff:>14.6f} | {dev:>9.4f}%{flag}")

    avg_dev = total_dev / len(y)
    print(f"  {'-'*65}")
    print(f"  Avg deviation: {avg_dev:.4f}%  |  Max deviation: {max_dev:.4f}%")

    return {'avg_deviation': avg_dev, 'max_deviation': max_dev}
