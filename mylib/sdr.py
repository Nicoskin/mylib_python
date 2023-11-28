"""
`SDR`
- sdr_settings()
- tx_sig()
- rx_cycles_buffer()

Модуляция:
    - bpsk()
    - qpsk()
        - qpsk_synchro()
    - qam16()

"""

import numpy as np

def sdr_settings(ip = "ip:192.168.3.1", frequency = 2e9, buffer_size = 1000, sample_rate = 1e6, tx_gain = 0, rx_gain = 0, mode = 'manual'):
    """
    Базовые настройки sdr
    
    sdr = sdr_settings("ip:192.168.3.1")
    sdr = sdr_settings("ip:192.168.3.1", 2300e6+(2e6*2), 1000, 1e6,0,30) # type: ignore
    
    Параметры
    ----------
        `ip` : "ip:192.168.3.1" / "ip:192.168.2.1"
        
        `frequency` : частота дискретизации
            от 325 [МГц] до 3.8 [ГГц]
            
        `buffer_size` = 1000 [samples]
        
        `sample_rate` = 1e6 [samples]
        
        `tx_gain`: сила передачи [dBm]
            рекомендуемое значение от 0 до -50
            
        `rx_gain`: чувствительность приёма [dBm]
            рекомендуемое значение от 0 до -50
            
        `mode` : str, optional
            slow_attack, fast_attack, manual
            
    Возвращает
    ----------  
        `sdr`: настроенная переменная sdr
    """    
    import adi
    sdr = adi.Pluto(ip)

    sdr.rx_lo = int(frequency)
    sdr.tx_lo = int(frequency)

    sdr.tx_destroy_buffer()
    sdr.rx_destroy_buffer()

    sdr.rx_buffer_size = buffer_size
    sdr.sample_rate = sample_rate
    sdr.gain_control_mode_chan0 = mode
    sdr.tx_hardwaregain_chan0 = tx_gain # рекомендуемое значение от 0 до -50
    sdr.rx_hardwaregain_chan0 = rx_gain # рекомендуемое значение от 0 до -50

    return sdr

def tx_sig(sdr, samples, tx_cycle: bool = True):
    """
    Функция передает samples на TX
    
    !!! Нужна настроенная sdr !!!
    
    Параметры
    ----------
        `sdr` : переменная sdr
        
        `tx_cycle`: по стандарту передает в цикле
        
    Не забывай сбрасывать буфер в конце проги 
        " sdr.tx_destroy_buffer() "
    ^^^^
    """
    try:
        sdr.tx_cyclic_buffer = tx_cycle
        sdr.tx(samples)
    except NameError:
        print("Переменная 'sdr' не определена.")
        return -1

def rx_cycles_buffer(sdr, num_cycles: int = 1):
    """
    Циклически получает сигнал с RX 
    
    !!! Нужна настроенная sdr !!!
    
    Параметры
    --------
        `sdr` : переменная sdr
        
        `num_cycles`: сколько раз получает буфер rx
    
    Возвращает
    ----------
        `rx`: выводит [num_cycles] циклов RX
    
    """
    rx = []
    try:
        for cycle in range(num_cycles):  # Считывает num_cycles циклов Rx
            new_data = sdr.rx()
            rx.extend(new_data)
        return rx
    except NameError:
        print("Переменная 'sdr' не определена.")
        return -1


def bpsk(bits, amplitude = 2**14, repeat: int | None = None):
    """
    BPSK модуляция битовой последовательности

    Параметры
    ---------
        `bits`: array
            Битовая последовательность (кратна 4)
        
        `amplitude` : int, optional
            По умолчанию 2**14
            
        `repeat` : int, optional
            Число повторений бит (np.repeat)
        
    Возвращает
    ---------
        `samples` : numpy array
            Массив комплексных чисел, представляющих BPSK модулированные сэмплы.
    """
    bits = np.array(bits)
    sam = bits * -2 + 1 # Маппинг 0 на 1, 1 на -1
    sam = sam * amplitude
    
    # Векторизованное преобразование в комплексные числа
    sam = np.vectorize(complex)(sam.real, sam.imag)
    
    if repeat is not None:
        sam = np.repeat(sam, repeat)
        
    return sam

def qpsk(bits, amplitude = 2**14, repeat: int | None = None):
    """
    QPSK модуляция битовой последовательности

    Параметры
    ---------
        `bits`: array
            Битовая последовательность
        
        `amplitude` : int, optional
            По умолчанию 2**14
        
        `repeat` : int, optional
            Число повторений бит (np.repeat)

    Возвращает
    ---------
        `samples` : numpy array
            Массив комплексных чисел, представляющих QPSK модулированные сэмплы.
    """   
    # Проверка, является ли bits массивом NumPy, если нет, преобразование в массив
    if not isinstance(bits, np.ndarray):
        bits = np.array(bits)

    # Убедитесь, что длина битовой последовательности кратна 2
    if len(bits) % 2 != 0:
        raise ValueError("Длина входной битовой последовательности должна быть четной для модуляции QPSK")
    
    # Разделение битов на действительную и мнимую части
    # Маппинг 0 на 1, 1 на -1
    in_phase = bits[::2] * -2 + 1
    quadrature = bits[1::2] * -2 + 1

    # Комбинирование в комплексные числа (QPSK modulation)
    samples = in_phase + 1j * quadrature
    
    samples = samples * amplitude # умножаем на амплитуду
    samples = np.array(samples)
    
    if repeat is not None:
        samples = np.repeat(samples, repeat)
    
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

    # Создание маппинга символов 16-QAM | 3GPP TS 38.211 V17.5.0 (2023-06
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

def qpsk_synchro(rx_array, threshold, length=490, angle=225, symbol_length: int | None = None):
    """
    Находит синхру и перекручивает сигнал на нужный угол    
    
    Если добавить длинну символа, то вернёт массив с одиночными символами

    Параметры
    ---------
        `rx_array` : array_like
            Входной комплексный массив.
        `threshold` : int
            Порог для определения синхронизации(± расхождение синхры)
        `length` : int, optional
            Длина последовательности для обнаружения синхронизации, по умолчанию 490("символы синхры" * "их длительность")
        `angle`: int, optional
            Угол на котором находится синхра
        `symbol_length`: int, optional
            Если задать число то оставит от RX только одиночные символы

    Возвращает
    ----------
        `synchronized_array` : np array
            Синхронизированный массив.
    """
    # Находим индексы элементов, близких к 1+1j
    k = 0
    for i in range(1, len(rx_array)):
        if abs(rx_array[i] - rx_array[i-1]) < threshold:
            k += 1
        else:
            k = 0

        if k == length:  # Порог для обнаружения синхронизации
            sync_index = i
            break
    
    if k == 0:
        print("Синхронизация не найдена")
        return rx_array  # Возвращаем исходный массив, если синхронизация не найдена
    
    # Находим средний угол для найденных элементов
    mean_angle = np.angle(rx_array[sync_index - length + 1:sync_index + 1]).mean()
    
    # Вычисляем угол fi_standart (225 градусов в радианах)
    fi_standart = np.deg2rad(angle)
    
    # Вычисляем коррекцию угла
    angle_correction = -(mean_angle - fi_standart)
    
    rx_array = np.array(rx_array)
    
    # Применяем коррекцию к массиву
    rx_array = rx_array * np.exp(1j * angle_correction)
    
    # Разбиение на символы
    if symbol_length is not None:
        symbols = rx_array.reshape(-1, symbol_length)
        extracted_symbols = symbols[:, 0]
        return extracted_symbols
    
    return rx_array

def bpsk_sin(rx_array, sin):
    """
    Поиск синхронизации bpsk в сигнале rx
    
    sin = -1,1
    
    Параметры
    ----------
        `rx_array`: Массив сигнала
        `sin`: массив синхронизации
    
    Возвращает
    --------
        `rx_array`: NParray
            Развернутый сигнал ограниченный синхронизацией вначалеи и в конце
    """
    import mylib as ml
    cor = ml.autocorr(rx_array.real, sin)
    
    i_cor = np.argmax(abs(cor), axis=0)
    
    # Поиск второй синхронизации
    i_cor_end = 0
    for i in range(len(cor)-1, 0, -1): 
        if abs(cor[i]) > 0.99:
            i_cor_end = i
            break
            
    if i_cor_end == 0:
        rx_array = rx_array[i_cor:]
    else:
        rx_array = rx_array[i_cor:i_cor_end]
    
    angle = np.angle(rx_array[0]) # угол синхры
    rx_array = rx_array * np.exp(1j * -angle) # разворот на нужный угол
    
    return rx_array