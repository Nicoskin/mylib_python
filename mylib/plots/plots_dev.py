import matplotlib.pyplot as plt
import numpy as np

def cool_scatter_dev(x, y=None, show_plot=True, name="cool_scatter"):
    fig, ax = plt.subplots(figsize=(7, 7), num=name)
    fig.subplots_adjust(left=0.07, bottom=0.05, top=0.94, right=0.94)
    ax.grid(linewidth=0.5)
    ax.tick_params(
        axis="both",
        direction="in",
        right=True,
        top=True,
        labelright=True,
        labeltop=True,
    )

    if y is None:
        y = x.imag
        x = x.real

    colors = range(len(x))
    scale = np.linspace(1, 30, len(x))
    ax.scatter(x, y, s=scale, c=colors, cmap="hsv", alpha=0.9)
    ax.axhline(y=0, color="black", linestyle="--", linewidth=1)
    ax.axvline(x=0, color="black", linestyle="--", linewidth=1)

    maxi = np.max((abs(x) ** 2 + abs(y) ** 2) ** 0.5)
    maxi *= 1.05
    
    ax.axis([-maxi, maxi, -maxi, maxi])
    ax.set_box_aspect(1)

    if show_plot is True:
        plt.show()