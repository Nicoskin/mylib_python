"""
`BASE`
- str_to_bits
- bits_to_str
- gen_rand_bits
- corr_no_shift
- corr_array
- auto_corr
- zadoff_chu

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

def bits_to_str(bit_array):
    """
    Преобразует битовую последовательность в строку ASCII.

    Параметры
    ----------
        `bit_array`: Битовая последовательность.
        
    Возвращает
    --------
        `decoded_str`: str
            Раскодированная строка ASCII.
    """
    bit_array = np.array(bit_array)
    

    # Разбиваем биты на байты (по 8 бит в каждом)
    bytes_list = [bit_array[i:i + 8] for i in range(0, len(bit_array), 8)]

    # Преобразуем каждый байт в десятичное число и затем в символ ASCII
    decoded_str = ''.join([chr(int(''.join(map(str, byte)), 2)) for byte in bytes_list])
    decoded_str = decoded_str.rstrip('\x00')
    
    return decoded_str

def corr_no_shift(x, y, norm=True, complex = False):
    """
    Вычисляет взаимную корреляцию двух одномерных массивов(без смещения)
    
    Параметры
    ------------
        x, y: одномерные массивы
        
        norm: есть нормирование или нет
        
        complex: есть ли комплексные переменные в массивах
        
    Возвращает
    ----------  
        Корреляция
    """
    x = np.asarray(x)
    y = np.asarray(y)

    if norm and complex:
        c_real = np.dot(x.real, y.real) / (np.linalg.norm(x.real) * np.linalg.norm(y.real))
        c_imag = np.dot(x.imag, y.imag) / (np.linalg.norm(x.imag) * np.linalg.norm(y.imag))
        return c_real+1j*c_imag
    elif norm:
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
        arr.append(corr_no_shift(xx, y))
    arr = np.array(arr)
    return arr

def auto_corr(x, y):
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
        corr = np.dot(xx, y) / (np.linalg.norm(xx) * np.linalg.norm(y))
        arr.append(corr)
    
    arr = np.array(arr)
    return arr

def gen_rand_bits(n: int, seed = 100):
    """
    Генерирует случайную битовую последовательность

    Параметры
    ----------
        `n`: длинна битовой последовательности
        
        `seed`: сид рандом функции


    Возвращает
    --------
        `bit_array`: NParray
            Массив случайных битов
    """
    if seed != 0:
        np.random.seed(seed)
    bit_array = np.random.randint(0, 2, n)
    return bit_array

def zadoff_chu(N=1, u=25, PSS=False):
    """
    Zadoff-Chu sequence
        N - length
        
        u - root index 25 29 34
        
        PSS [optional] - Primary synchronization signal
            N - 63 
            Len - 62
    """
    if PSS:
        N = 63
        n = np.arange(0, 31)
        ex1 = np.exp(-1j * np.pi * u * n * (n + 1) / N)
        n = np.arange(31, 62)
        ex2 = np.exp(-1j * np.pi * u * (n + 1) * (n + 2) / N)
        return np.concatenate([ex1, ex2])
    else:  
        n = np.arange(0, N)
        return np.exp(-1j * np.pi * u * n * (n + 1) / N)