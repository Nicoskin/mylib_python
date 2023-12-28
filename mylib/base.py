"""
`BASE`
- str_to_bits()
- bits_to_str()
- merge_arr()
- correlation()
- corr_array()
- autocorr()

"""

import numpy as np

def str_to_bits(str: str):
    """
    Преобразовает строку в битовую последовательност(ascii)
    
    Параметры
    -------------
        `str` : строка которая кодируется

    Возвращает
    ----------
        `bit_array` : numpy array
            Закодированный массив ASCII (битовая последовательность)
    """
    encoded_bytes = str.encode('ascii')
    # Преобразование байтов в массив битов
    bit_array = []
    for byte in encoded_bytes:
        bits = bin(byte)[2:].zfill(8)  # Преобразование в биты
        bit_array.extend([int(bit) for bit in bits])

    return np.array(bit_array)

def bits_to_str(bit_array, b_start: int | None = None, b_stop: int | None = None):
    """
    Преобразует битовую последовательность в строку ASCII.

    Параметры
    ----------
        `bit_array`: Битовая последовательность.

        `b_start`: (optional) удалить в начале
        
        `b_stop`: (optional) удалить в конце

    Возвращает
    --------
        `decoded_str`: str
            Раскодированная строка ASCII.
    """
    bit_array = np.array(bit_array)
    if b_start is not None and b_stop is not None:
        # Удаляем добавленные единицы в начале и в конце
        bit_array = bit_array[b_start:-b_stop]
    elif b_start is not None:
        # Удаляем добавленные единицы в начале
        bit_array = bit_array[b_start:]

    # Разбиваем биты на байты (по 8 бит в каждом)
    bytes_list = [bit_array[i:i + 8] for i in range(0, len(bit_array), 8)]

    # Преобразуем каждый байт в десятичное число и затем в символ ASCII
    decoded_str = ''.join([chr(int(''.join(map(str, byte)), 2)) for byte in bytes_list])

    return decoded_str

def merge_arr(x,y):
    """Обьединяет 2 массива

    Параметры
    ----------
        `x`, `y`: Первый и второй массив

    Возвращает
    --------
        `x+y`: NParray
            Массив из соединённых массивов x y
    """
    x = list(x)
    y = list(y)
    c = np.array(x+y)
    return c

def correlation(x, y, norm=True):
    """
    Вычисляет взаимную корреляцию двух одномерных массивов(без смещения)
    
    Параметры
    ------------
        x, y: одномерные массивы
        
        norm: есть нормирование или нет
        
    Возвращает
    ----------  
        Корреляция
    """
    x = np.asarray(x)
    y = np.asarray(y)

    if norm:
        c = np.dot(x, y) / (np.linalg.norm(x) * np.linalg.norm(y))
        return c
    else:
        c = np.dot(x, y)
        return c

def corr_array(x, y):
    """Корреляция двух массивов 
    
    len(x) > len(y)

    Параметры
    ----------
        `x`, `y`: Первый и второй массив

    Возвращает
    --------
        `x+y`: NParray
            Массив корреляции
    """
    arr = []
    for i in range(len(x)-len(y)+1):
        xx = x[i:(i+len(y))]
        arr.append(correlation(xx, y))
    arr = np.array(arr)
    return arr

def autocorr(x, y):
    """
    Автокорреляция двух массивов 
    
    len(x) > len(y)

    Параметры
    ----------
        `x`, `y`: Первый и второй массив

    Возвращает
    --------
        `x+y`: NParray
            Массив автокорреляции
    """
    
    arr = []
    if len(x) <= len(y):
        print('Длинна X меньше длинны Y')
        return -1
    
    for i in range(len(x)-len(y)+1):
        xx = x[i:(i+len(y))]
        # match_count = 0
        # for j in range(len(y)):
        #     if xx[j] == y[j]:
        #         match_count += 1
        # p = (match_count - len(y) / 2) / (len(y) / 2)
        # arr.append(p)
        
        corr = np.dot(xx, y) / (np.linalg.norm(xx) * np.linalg.norm(y))
        arr.append(corr)
    
    arr = np.array(arr)
    return arr