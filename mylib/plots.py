"""
`Графики`

- cool_scatter()
- cool_plot()
- angle_scatter()

"""

import matplotlib.pyplot as plt
import numpy as np
from typing import Literal


def cool_scatter(x, y=None, show_plot=True, name="cool_scatter"):
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
    ax.scatter(x, y, s=10, c=colors, cmap="hsv", alpha=0.9)
    ax.axhline(y=0, color="black", linestyle="--", linewidth=1)
    ax.axvline(x=0, color="black", linestyle="--", linewidth=1)

    maxi = np.max((abs(x) ** 2 + abs(y) ** 2) ** 0.5)
    maxi *= 1.05
    
    ax.axis([-maxi, maxi, -maxi, maxi])
    ax.set_box_aspect(1)

    if show_plot is True:
        plt.show()

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

def cool_plot(x, y=None, gap: Literal["none", "snake", "jump"] = "none", show_plot=True):
    if not isinstance(x, np.ndarray):  # Проверка на numpy
        x = np.array(x)

    if y is None:
        y = x.imag
        x = x.real

    fig, (ax1, ax2) = plt.subplots(2, sharex=True, figsize=(9, 7), num="cool_plot")
    fig.subplots_adjust(left=0.05, bottom=0.05, right=0.95, top=0.95, hspace=0.1)
    ax1.plot(x)
    ax1.plot(y)
    ax1.grid(linewidth=0.5)
    rx = np.array(x) + 1j * np.array(y)
    ax1.axis([-10, len(rx) + 10, -max(abs(rx)) * 1.05, max(abs(rx)) * 1.05])

    ax2.grid(linewidth=0.5)
    an = []
    for i in range(len(rx)):
        an.append(np.angle(rx[i]))

    if gap == "snake":
        for i in range(len(an)):
            if an[i] > 0:
                if an[i] >= np.pi / 2:
                    an[i] = np.pi / 2 - (an[i] - (np.pi / 2))
            else:
                an[i] += np.pi
                if an[i] >= np.pi / 2:
                    an[i] = np.pi / 2 - (an[i] - (np.pi / 2))
    elif gap == "jump":
        for i in range(len(an)):
            if an[i] < 0:
                an[i] += np.pi
            while an[i] > np.pi / 2:
                an[i] -= np.pi / 2
                
    an = np.array(an)

    ax2.plot(an)
    ax2.set_xlim(-10, len(an) + 10)

    if show_plot is True:
        plt.show()

# добавить изменение радиуса точек по мере отдаления от начала кfординат
def angle_scatter(x, y=None, gap: Literal["none", "snake", "jump"] = "none", show_plot=True, print_stats=False):
    if not isinstance(x, np.ndarray):  # Проверка на numpy
        x = np.array(x)
    
    if y is None:
        y = x.imag * 1j
        x = x.real
    an = []
    for i in range(len(x)):
        an.append(np.angle(x[i] + y[i]))
    an = np.array(an)
    
    if gap == "snake":
        for i in range(len(an)):
            if an[i] > 0:
                if an[i] >= np.pi / 2:
                    an[i] = np.pi / 2 - (an[i] - (np.pi / 2))
            else:
                an[i] += np.pi
                if an[i] >= np.pi / 2:
                    an[i] = np.pi / 2 - (an[i] - (np.pi / 2))
    elif gap == "jump":
        for i in range(len(an)):
            if an[i] < 0:
                an[i] += np.pi
            while an[i] > np.pi / 2:
                an[i] -= np.pi / 2
    
    if print_stats is True:
        an_last = an[0]
        aaa = []
        for i in range(len(an)):
            if ((abs(an_last - an[i]) < np.pi / 4)
                or ((an_last < (-np.pi * 9 / 10)) and (an[i] == np.pi)) 
                or ((an_last > (np.pi * 9 / 10)) and (an[i] == np.pi))):
                an_last = an[i]
                k = i
                aaa.append(an[i])
        
        print('За ',an[0], an_last, an[0] - an_last, k)
        print('1 ',an[0])
    
    r = np.linspace(0.0, 0.8, len(an))
    x = r * np.cos(an)
    y = r * np.sin(an)
    arr = x + y * 1j
    
    # for i in range(len(an)):
    #     arr[i] = arr[i] * np.exp(1j * (0.0051*i))
    
    #cool_scatter(arr, show_plot=False, name="angle_scatter")
    
    # r = np.linspace(0.0, 0.8, len(aaa))
    # x = r * np.cos(aaa)
    # y = r * np.sin(aaa)
    cool_scatter_dev(x, y, show_plot=False, name="angle_scatter")

    if show_plot is True:
        plt.show()
