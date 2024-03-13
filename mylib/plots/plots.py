import matplotlib.pyplot as plt
import numpy as np
from typing import Literal
from pylab import gcf

call_count_scat, call_count_plot, call_count_scat_dev_, call_count_eye = 0, 0, 0, 0

def cool_scatter(x, y=None, show_plot=False, name="cool_scatter", title="", circle=False):
    """
    Создает точечную диаграмму с красивыми визуализациями.

    Параметры:
        `x`: (подобный массиву): x-координаты точек.
        `y`: (подобный массиву, необязательный): y-координаты точек. Если не указано, мнимая часть x будет использоваться в качестве y-координат.
        `show_plot`: (логическое значение, необязательный): Определяет, нужно ли отображать диаграмму. По умолчанию True.
        `name`:(строка, необязательный): Название окна диаграммы. По умолчанию "cool_scatter".
        `title`:(строка, необязательный): Заголовок диаграммы. По умолчанию пустая строка.
        `circle`:(логическое значение, необязательный): Определяет, нужно ли добавить круги на диаграмму. По умолчанию False.
    """
    global call_count_scat
    call_count_scat += 1
    if call_count_scat >= 2:
        num_ = 3454 + call_count_scat
        name = name + f'{call_count_scat}'
    else:
        num_ = 3454
        
    fig, ax = plt.subplots(figsize=(7, 7), num=num_)
    fig = gcf()
    fig.canvas.manager.set_window_title(name)
    fig.subplots_adjust(left=0.08, bottom=0.06, top=0.93, right=0.93)
    fig.suptitle(title)
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
    
    if circle is True:
        import matplotlib.patches as patches
        if (max(x) > 2.5) & (max(x) < 100):
            points = [(1, 1), (-1, -1), (-1, 1), (1, -1),
                      (1, 3), (-1, -3), (-1, 3), (1, -3),
                      (3, 1), (-3, -1), (-3, 1), (3, -1),
                      (3, 3), (-3, -3), (-3, 3), (3, -3)]
        else:
            points = [(1, 1), (-1, -1), (-1, 1), (1, -1)]
        for point in points:
            circle = patches.Circle(point, 0.5, edgecolor='b', facecolor='none', linewidth=0.5)
            ax.add_patch(circle)

    maxi = np.max((abs(x) ** 2 + abs(y) ** 2) ** 0.5)
    maxi *= 1.05
    
    ax.axis([-maxi, maxi, -maxi, maxi])
    ax.set_box_aspect(1)

    if show_plot is True:
        plt.show()


def _cool_plot_first(x, y, vid, num_ = 87954):
    fig, ax1 = plt.subplots(1, sharex=True, figsize=(10, 5), num=num_)
    fig.subplots_adjust(left=0.07, bottom=0.08, right=0.95, top=0.92, hspace=0.1)
    ax1.plot(x, vid)
    ax1.plot(y, vid)
    ax1.grid(linewidth=0.5)
    rx = np.array(x) + 1j * np.array(y)
    maximum = max(max(abs(rx.real)), max(abs(rx.imag)))
    minimum = min(min(rx.real), min(rx.imag))
    if minimum >= 0:
        ax1.axis([-len(rx) * 0.02, len(rx) * 1.02, -maximum*0.05, maximum * 1.15])
    else:
        ax1.axis([-len(rx) * 0.02, len(rx) * 1.02, -maximum * 1.15, maximum * 1.15])

    return fig

def _cool_plot_second(x, y, vid, num_ = 87954, gap: Literal["none", "snake", "jump"] = "none"):
    fig, (ax1, ax2) = plt.subplots(2, sharex=True, figsize=(9, 7), num=num_)
    fig.subplots_adjust(left=0.08, bottom=0.05, right=0.95, top=0.95, hspace=0.1)
    ax1.plot(x, vid)
    ax1.plot(y, vid)
    ax1.grid(linewidth=0.5)
    rx = np.array(x) + 1j * np.array(y)
    maximum = max(max(abs(rx.real)), max(abs(rx.imag)))
    ax1.axis([-len(rx) * 0.02, len(rx) * 1.02, -maximum * 1.15, maximum * 1.15])

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
    
    return fig
    
def cool_plot(x, y=None, vid = '-', sec_plot = False, gap: Literal["none", "snake", "jump"] = "none", title="", show_plot=False):
    """
    Создает красивый график на основе входных данных.

    Параметры:
    - x: одномерный массив или список значений для оси x.
    - y: одномерный массив или список значений для оси y. Если не указан, будет использована мнимая часть x.
    - vid: тип линии графика. По умолчанию '-'.
    - sec_plot: флаг, указывающий, нужно ли создать второй график. По умолчанию False.
    - gap: тип разрыва на графике. Может быть "none" (без разрыва), "snake" (змеевидный разрыв) или "jump" (скачок разрыв). По умолчанию "none".
    - title: заголовок графика. По умолчанию пустая строка.
    - show_plot: флаг, указывающий, нужно ли отображать график. По умолчанию False.

    Возвращает:
    Ничего.

    Пример использования:
    cool_plot([1, 2, 3, 4], [5, 6, 7, 8], gap="snake", show_plot=True)
    """
    name = 'cool_plot'
    global call_count_plot
    call_count_plot += 1
    if call_count_plot >= 2:
        num_ = 87954 + call_count_plot
        name = name + '_' +f'{call_count_plot}'
    else:
        num_ = 87954
        
    if not isinstance(x, np.ndarray):  # Проверка на numpy
        x = np.array(x)

    if y is None:
        y = x.imag
        x = x.real

    if not sec_plot:
        fig = _cool_plot_first(x, y, vid, num_)
    elif sec_plot:
        fig = _cool_plot_second(x, y, vid, num_, gap)

    fig = gcf()
    fig.canvas.manager.set_window_title(name)
    fig.suptitle(title)

    if show_plot is True:
        plt.show()


def angle_scatter(x, y=None, gap: Literal["none", "snake", "jump"] = "none", show_plot=False, print_stats=False):
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

def eye_pattern(x, y=None, symbol_len = 10, show_plot=False):
    """
    Функция eye_pattern отображает глазковую диаграмму для заданного сигнала.
    
    Параметры:
    - x: одномерный массив или список, представляющий вещественную часть сигнала или комплексный сигнал.
    - y: одномерный массив или список, представляющий мнимую часть сигнала. Если не указан, будет использована мнимая часть x.
    - symbol_len: длина символа, используемая для разделения сигнала на символы. По умолчанию равна 10.
    - show_plot: флаг, указывающий, нужно ли отображать график. По умолчанию True.
    """
    global call_count_eye
    call_count_eye += 1
    if call_count_eye >= 2:
        num_ = 12354 + call_count_eye
        name = name + f'{call_count_eye}'
    else:
        num_ = 31254
    
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

    fig, ax = plt.subplots(figsize=(8, 6), num=num_)
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



def _cool_scatter_dev(x, y=None, show_plot=False, name="cool_scatter"):
    """
    Тот же cool_scatter, но со scale точек
    """
    global call_count_scat_dev_
    call_count_scat_dev_ += 1
    if call_count_scat_dev_ >= 2:
        num_ = 123514 + call_count_scat_dev_
        name = name + f'{call_count_scat_dev_}'
    else:
        num_ = 123514
        
    fig, ax = plt.subplots(figsize=(7, 7), num=num_)
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