"""
`Модуляция`

- bpsk
    - bpsk_synchro
- qpsk
- qam16
- qam64

`Демодуляция`
- dem_qpsk
- dem_qam16

"""

import numpy as np

def bpsk(bits, amplitude = 2**14, quadrature = 0):
    """
    BPSK модуляция битовой последовательности

    Параметры
    ---------
        `bits`: array
            Битовая последовательность (кратна 4)
        
        `amplitude` : int, optional
            По умолчанию 2**14
            
        `quadrature` : 0|1, optional
            если 0 то Q=0 | если 1 то Q=I
        
    Возвращает
    ---------
        `samples` : numpy array
            Массив комплексных чисел, представляющих BPSK модулированные сэмплы.
    """
    bits = np.array(bits)
    min = np.min(bits)
    if  min == 0:               # Маппинг 0 на 1, 1 на -1
        sam = bits * -2 + 1
        sam = sam * amplitude
    else:                       # -1 на -1, 1 на 1
        sam = bits * amplitude
    
    # Векторизованное преобразование в комплексные числа
    sig = np.vectorize(complex)(sam.real, sam.imag)
    if quadrature == 0:
        sig = np.vectorize(complex)(sam.real, sam.imag)
    elif quadrature == 1:
        sig = np.vectorize(complex)(sam.real, sam.real)
    else:
        print("(ERROR MyLib): quadrature не равна 1|0\n")
        return -1
    sqrt = 1/(2**0.5)
        
    return np.array(sig)*sqrt

def qpsk(bits, amplitude = 2**14):
    """
    QPSK модуляция битовой последовательности

    Параметры
    ---------
        `bits`: array
            Битовая последовательность
        
        `amplitude` : int, optional
            По умолчанию 2**14
        
    Возвращает
    ---------
        `samples` : numpy array
            Массив комплексных чисел, представляющих QPSK модулированные сэмплы.
    """   
    # Проверьте, кратна ли длина битов 2
    if len(bits) % 2 != 0:
        raise ValueError("Длина входной битовой последовательности должна быть кратна 4")

    # Создание маппинга символов 16-QAM | 3GPP TS 38.211 V17.5.0 (2023-06)
    qam_symbols = {
        (0, 0):  1 + 1j,
        (0, 1):  1 - 1j,
        (1, 0): -1 + 1j,
        (1, 1): -1 - 1j,
    }

    # Группировка входных битов в 2-битные блоки
    symbols = [tuple(bits[i:i+2]) for i in range(0, len(bits), 2)]
    
    # Сопоставляет каждый 2-битный фрагмент со сложным символом
    sqrt = 1/(2**0.5)
    samples = np.array([qam_symbols[s]*sqrt for s in symbols])
    samples = samples * (amplitude)

    return samples

def qam16(bits, amplitude = 2**14):
    """16-QAM модуляция для битовой последовательности

    Параметры
    ---------
        `bits`: array
            Битовая последовательность (кратна 4)
        
        `amplitude` : int, optional
            По умолчанию 2**14

    Возвращает
    ---------
        `samples` : numpy array
            Массив комплексных чисел, представляющих 16-QAM модулированные сэмплы.
    """
    # Проверьте, кратна ли длина битов 4
    if len(bits) % 4 != 0:
        raise ValueError("Длина входной битовой последовательности должна быть кратна 4")

    # Создание маппинга символов 16-QAM | 3GPP TS 38.211 V17.5.0 (2023-06)
    qam_symbols = {
        (0, 0, 0, 0): 1 + 1j,
        (0, 0, 0, 1): 1 + 3j,
        (0, 0, 1, 0): 3 + 1j,
        (0, 0, 1, 1): 3 + 3j,
        (0, 1, 0, 0): 1 - 1j,
        (0, 1, 0, 1): 1 - 3j,
        (0, 1, 1, 0): 3 - 1j,
        (0, 1, 1, 1): 3 - 3j,
        (1, 0, 0, 0): -1 + 1j,
        (1, 0, 0, 1): -1 + 3j,
        (1, 0, 1, 0): -3 + 1j,
        (1, 0, 1, 1): -3 + 3j,
        (1, 1, 0, 0): -1 - 1j,
        (1, 1, 0, 1): -1 - 3j,
        (1, 1, 1, 0): -3 - 1j,
        (1, 1, 1, 1): -3 - 3j,
    }

    # Группировка входных битов в 4-битные блоки
    symbols = [tuple(bits[i:i+4]) for i in range(0, len(bits), 4)]
    
    # Сопоставляет каждый 4-битный фрагмент со сложным символом
    sqrt = 1/(10**0.5)
    samples = np.array([qam_symbols[s]*sqrt for s in symbols])
    samples = samples * (amplitude)

    return samples

def qam64(bits, amplitude = 2**14):
    """64-QAM модуляция для битовой последовательности

    Параметры
    ---------
        `bits`: array
            Битовая последовательность (кратна 6)
        
        `amplitude` : int, optional
            По умолчанию 2**14

    Возвращает
    ---------
        `samples` : numpy array
            Массив комплексных чисел, представляющих 64-QAM модулированные сэмплы.
    """
    # Проверьте, кратна ли длина битов 6
    if len(bits) % 6 != 0:
        raise ValueError("Длина входной битовой последовательности должна быть кратна 6")

    # Создание маппинга символов 16-QAM | 3GPP TS 38.211 V17.5.0 (2023-06)
    qam_symbols = {
    (0, 0, 0, 0, 0, 0):  3 + 3j,(0, 0, 0, 0, 0, 1):  3 + 1j,(0, 0, 0, 0, 1, 0):  1 + 3j,(0, 0, 0, 0, 1, 1):  1 + 1j,
    (0, 0, 0, 1, 0, 0):  3 + 5j,(0, 0, 0, 1, 0, 1):  3 + 7j,(0, 0, 0, 1, 1, 0):  1 + 5j,(0, 0, 0, 1, 1, 1):  1 + 7j,
    (0, 0, 1, 0, 0, 0):  5 + 3j,(0, 0, 1, 0, 0, 1):  5 + 1j,(0, 0, 1, 0, 1, 0):  7 + 3j,(0, 0, 1, 0, 1, 1):  7 + 1j,
    (0, 0, 1, 1, 0, 0):  5 + 5j,(0, 0, 1, 1, 0, 1):  5 + 7j,(0, 0, 1, 1, 1, 0):  7 + 5j,(0, 0, 1, 1, 1, 1):  7 + 7j,
    (0, 1, 0, 0, 0, 0):  3 - 3j,(0, 1, 0, 0, 0, 1):  3 - 1j,(0, 1, 0, 0, 1, 0):  1 - 3j,(0, 1, 0, 0, 1, 1):  1 - 1j,
    (0, 1, 0, 1, 0, 0):  3 - 5j,(0, 1, 0, 1, 0, 1):  3 - 7j,(0, 1, 0, 1, 1, 0):  1 - 5j,(0, 1, 0, 1, 1, 1):  1 - 7j,
    (0, 1, 1, 0, 0, 0):  5 - 3j,(0, 1, 1, 0, 0, 1):  5 - 1j,(0, 1, 1, 0, 1, 0):  7 - 3j,(0, 1, 1, 0, 1, 1):  7 - 1j,
    (0, 1, 1, 1, 0, 0):  5 - 5j,(0, 1, 1, 1, 0, 1):  5 - 7j,(0, 1, 1, 1, 1, 0):  7 - 5j,(0, 1, 1, 1, 1, 1):  7 - 7j,
    (1, 0, 0, 0, 0, 0): -3 + 3j,(1, 0, 0, 0, 0, 1): -3 + 1j,(1, 0, 0, 0, 1, 0): -1 + 3j,(1, 0, 0, 0, 1, 1): -1 + 1j,
    (1, 0, 0, 1, 0, 0): -3 + 5j,(1, 0, 0, 1, 0, 1): -3 + 7j,(1, 0, 0, 1, 1, 0): -1 + 5j,(1, 0, 0, 1, 1, 1): -1 + 7j,
    (1, 0, 1, 0, 0, 0): -5 + 3j,(1, 0, 1, 0, 0, 1): -5 + 1j,(1, 0, 1, 0, 1, 0): -7 + 3j,(1, 0, 1, 0, 1, 1): -7 + 1j,
    (1, 0, 1, 1, 0, 0): -5 + 5j,(1, 0, 1, 1, 0, 1): -5 + 7j,(1, 0, 1, 1, 1, 0): -7 + 5j,(1, 0, 1, 1, 1, 1): -7 + 7j,
    (1, 1, 0, 0, 0, 0): -3 - 3j,(1, 1, 0, 0, 0, 1): -3 - 1j,(1, 1, 0, 0, 1, 0): -1 - 3j,(1, 1, 0, 0, 1, 1): -1 - 1j,
    (1, 1, 0, 1, 0, 0): -3 - 5j,(1, 1, 0, 1, 0, 1): -3 - 7j,(1, 1, 0, 1, 1, 0): -1 - 5j,(1, 1, 0, 1, 1, 1): -1 - 7j,
    (1, 1, 1, 0, 0, 0): -5 - 3j,(1, 1, 1, 0, 0, 1): -5 - 1j,(1, 1, 1, 0, 1, 0): -7 - 3j,(1, 1, 1, 0, 1, 1): -7 - 1j,
    (1, 1, 1, 1, 0, 0): -5 - 5j,(1, 1, 1, 1, 0, 1): -5 - 7j,(1, 1, 1, 1, 1, 0): -7 - 5j,(1, 1, 1, 1, 1, 1): -7 - 7j
    }

    # Группировка входных битов в 6-битные блоки
    symbols = [tuple(bits[i:i+6]) for i in range(0, len(bits), 6)]
    
    # Сопоставляет каждый 6-битный фрагмент со сложным символом
    sqrt = 1/(10**0.5)
    samples = np.array([qam_symbols[s]*sqrt for s in symbols])
    samples = samples * (amplitude)

    return samples


def bpsk_synchro(rx_array, syn, synchro_angle = 0, debug = False):
    """
    Поиск синхронизации bpsk в сигнале rx
    Разворот на правильный угол, если синхронизация BPSK на угле 0.
        
    Параметры
    ----------
        `rx_array`: Массив сигнала
        
        `syn`: массив синхронизации
        
        `debag`: F|T, optional - дополнительный вывод графика и print начала и конца
    
    Возвращает
    --------
        `rx_array`: numpy array
            Развернутый сигнал ограниченный синхронизацией в начале и в конце
    """
    import mylib as ml
    cor = ml.auto_corr(rx_array.real, syn)
    # i_cor = np.argmax(abs(cor), axis=0)
    for i in range(len(cor)):
        if abs(cor[i]) >= 0.93:
            i_cor = i
            break
    # Поиск второй синхронизации
    i_cor_end = 0
    for i in range(i_cor+1, len(cor), 1): 
        if abs(cor[i]) > 0.95 and i_cor_end == 0:
            i_cor_end = i
            break 
    if i_cor_end == 0:
        rx_array = rx_array[i_cor:]
    else:
        rx_array = rx_array[i_cor:i_cor_end]
    
    if debug:
        ml.cool_plot(cor, title="Корреляция")
        print("start =",i_cor, end=" | ")
        print("end =",i_cor_end)  

    if synchro_angle == 0:
        angle = np.angle(rx_array[0]) # угол синхры если bpsk на угле 0
    elif synchro_angle == 45:
         angle = np.angle(rx_array[0]) + np.pi/4
    else:
        print("(ERR MYLIB)\n    Некорректный ввод synchro_angle\n")
    
    rx_array = rx_array * np.exp(1j * -angle) # разворот на нужный угол
    
    return rx_array


def dem_qpsk(symbols):
    """
    Дешифровка qpsk символов

    Параметры
    ---------
        `symbols`: array
            Символы qpsk

    Возвращает
    ---------
        `decoded_bits_array` : numpy array
            
    """
        
    def demodulate_qpsk_symbol(symbol):
        # Определяем QPSK символы
        qpsk_symbols = [1+1j, 1-1j, -1+1j, -1-1j]

        # Проверяем, находится ли символ в пределах 0.5 от каждого QPSK символа
        for i, qpsk_symbol in enumerate(qpsk_symbols):
            if abs(symbol - qpsk_symbol) <= 0.5:
                # Возвращаем соответствующий бит
                return np.array([i//2, i%2])

        # Если символ не соответствует ни одному из QPSK символов, возвращаем [0, 0]
        return np.array([0, 0])

    maxi = max(max(symbols.real), max(symbols.imag))
    symbols = symbols / maxi
    symbols = symbols * 1.3334
    
    # from .plots import cool_scatter 
    # cool_scatter(symbols)
    
    decoded_bits_array = np.array([demodulate_qpsk_symbol(sym) for sym in symbols])
    return decoded_bits_array.flatten()

def dem_qam16(symbols):
    """
    Дешифровка qam16 символов

    Параметры
    ---------
        `symbols`: array
            Символы qam16

    Возвращает
    ---------
        `decoded_bits_array` : numpy array
            
    """
    # Создание маппинга символов 16-QAM
    qam16_symbols = {
        1 + 1j: (0, 0, 0, 0),
        1 + 3j: (0, 0, 0, 1),
        3 + 1j: (0, 0, 1, 0),
        3 + 3j: (0, 0, 1, 1),
        1 - 1j: (0, 1, 0, 0),
        1 - 3j: (0, 1, 0, 1),
        3 - 1j: (0, 1, 1, 0),
        3 - 3j: (0, 1, 1, 1),
        -1 + 1j: (1, 0, 0, 0),
        -1 + 3j: (1, 0, 0, 1),
        -3 + 1j: (1, 0, 1, 0),
        -3 + 3j: (1, 0, 1, 1),
        -1 - 1j: (1, 1, 0, 0),
        -1 - 3j: (1, 1, 0, 1),
        -3 - 1j: (1, 1, 1, 0),
        -3 - 3j: (1, 1, 1, 1),
    }

    # Нормализация символов
    maxi = max(max(symbols.real), max(symbols.imag))
    symbols = symbols / maxi
    symbols = symbols * 1.3334 * 3
    
    # Демодуляция символов
    decoded_bits_array = []
    for sym in symbols:
        # Находим ближайший QAM16 символ
        closest_symbol = min(qam16_symbols.keys(), key=lambda x: abs(x - sym))
        # Добавляем соответствующие биты в массив
        decoded_bits_array.append(qam16_symbols[closest_symbol])

    return np.array(decoded_bits_array).flatten()