import matplotlib.pyplot as plt
import numpy as np
from typing import Literal
from pylab import gcf

from .plots_dev import _cool_scatter_dev

def cool_scatter(x, y=None, show_plot=True, name="cool_scatter"):
    """
    Создает точечную диаграмму с красивыми визуализациями.

    Параметры:
        `x`: (подобный массиву): x-координаты точек.
        `y`: (подобный массиву, необязательный): y-координаты точек. Если не указано, мнимая часть x будет использоваться в качестве y-координат.
        `show_plot`: (логическое значение, необязательный): Определяет, нужно ли отображать диаграмму. По умолчанию True.
        `name`:(строка, необязательный): Название окна диаграммы. По умолчанию "cool_scatter".
    """
    fig, ax = plt.subplots(figsize=(7, 7), num=3454)
    fig = gcf()
    fig.canvas.manager.set_window_title(name)
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

def cool_plot(x, y=None, gap: Literal["none", "snake", "jump"] = "none", show_plot=True):
    """
    Создает красивый график на основе входных данных.

    Параметры:
    - x: одномерный массив или список значений для оси x.
    - y: одномерный массив или список значений для оси y. Если не указан, будет использовано мнимая часть x.
    - gap: тип разрыва на графике. Может быть "none" (без разрыва), "snake" (змеевидный разрыв) или "jump" (скачок разрыв).
    - show_plot: флаг, указывающий, нужно ли отображать график. По умолчанию True.

    Возвращает:
    Ничего.

    Пример использования:
    cool_plot([1, 2, 3, 4], [5, 6, 7, 8], gap="snake", show_plot=True)
    """
    if not isinstance(x, np.ndarray):  # Проверка на numpy
        x = np.array(x)

    if y is None:
        y = x.imag
        x = x.real

    fig, (ax1, ax2) = plt.subplots(2, sharex=True, figsize=(9, 7), num=87954)
    fig = gcf()
    fig.canvas.manager.set_window_title("cool_plot")
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

def angle_scatter(x, y=None, gap: Literal["none", "snake", "jump"] = "none", show_plot=True, print_stats=False):
    """
    Создает scatter plot для угловых координат.
    
    Параметры:
    - x: одномерный массив или список, содержащий значения для оси x.
    - y: одномерный массив или список, содержащий значения для оси y. Если не указан, то используется мнимая часть x, а вещественная часть x становится осью x.
    - gap: строка, определяющая тип разрыва между значениями углов. Возможные значения: "none" (без разрыва), "snake" (змеевидный разрыв), "jump" (скачкообразный разрыв). По умолчанию "none".
    - show_plot: булево значение, указывающее, нужно ли отображать график. По умолчанию True.
    - print_stats: булево значение, указывающее, нужно ли выводить статистику. По умолчанию False.
    
    Возвращает:
    - None
    
    Пример использования:
    >>> angle_scatter([1, 2, 3, 4, 5], gap="snake", show_plot=True, print_stats=True)
    """
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

    _cool_scatter_dev(x, y, show_plot=False, name="angle_scatter")

    if show_plot is True:
        plt.show()

def eye_pattern(x, y=None, symbol_len = 10, show_plot=True):
    """
    Функция eye_pattern отображает глазковую диаграмму для заданного сигнала.
    
    Параметры:
    - x: одномерный массив или список, представляющий вещественную часть сигнала или комплексный сигнал.
    - y: одномерный массив или список, представляющий мнимую часть сигнала. Если не указан, будет использована мнимая часть x.
    - symbol_len: длина символа, используемая для разделения сигнала на символы. По умолчанию равна 10.
    - show_plot: флаг, указывающий, нужно ли отображать график. По умолчанию True.
    """
    if not isinstance(x, np.ndarray):  # Проверка на numpy
        x = np.array(x)

    if y is None:
        y = x.imag
        x = x.real
    
    ost = len(x) % symbol_len 
    x = np.array(x[:-ost])
    y = np.array(y[:-ost])
    arr = x + y * 1j
    
    arr = np.array(arr)

    arr = arr.reshape(-1, symbol_len)

    fig, ax = plt.subplots(figsize=(8, 6), num=3123454)
    fig = gcf()
    fig.canvas.manager.set_window_title('eye_pattern')
    fig.subplots_adjust(left=0.07, bottom=0.05, top=0.94, right=0.94)
    ax.grid(linewidth=0.5)

    axX = np.arange(1,symbol_len+1)

    for p in arr:
        ax.plot(axX, p, 'o-')
        
    plt.xticks(axX)
    
    if show_plot:
        plt.show()
