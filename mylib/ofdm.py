"""
- ofdm_64
- get_sr_from_freq_step
- activ_carriers
- synchro_ofdm
"""

import numpy as np
from .base import corr_no_shift


def ofdm_64(symbols, amplitude=2**15, ravel=True):
    """
    OFDM модуляция, fft - 64, cp - 16, gb - 6

    Возвращает массив сигналов OFDM
    if ravel - False
        Матрица [n, 80] (16+64)
    elif ravel - True
        Массив [n*80]

    """
    fft_len = 64
    _cyclic_prefix_len = 16
    _guard_band_len = 6
    pilot_carriers = (-21, -7, 7, 21)
    pilot_symbols = (1 + 1j, 1 + 1j, 1 + 1j, -1 - 1j)

    activ = activ_carriers(64, 6, (-21, -7, 7, 21), True)  # 47 carriers

    # Разделение массива symbols на матрицу(по 47 в строке)
    len_arr = len(activ)
    symbols1 = np.array_split(
        symbols[: -(len(symbols) % len_arr)], len(symbols) / len_arr
    )
    symbols2 = np.array((symbols[-(len(symbols) % len_arr) :]))
    symbols1.append(symbols2)
    symbols = symbols1

    pilot_carriers = np.array(pilot_carriers)
    pilot_carriers[pilot_carriers < 0] += 64

    # Создание матрицы, в строчке по 47 символов QPSK
    arr_symols = np.zeros((len(symbols), fft_len), dtype=complex)
    for i, symbol in enumerate(arr_symols):
        index_pilot = 0
        index_sym = 0
        for j in range(len(symbol)):
            if j in pilot_carriers:
                arr_symols[i][j] = pilot_symbols[index_pilot]
                index_pilot += 1
            elif j in activ and index_sym < len(symbols[i]):
                arr_symols[i][j] = symbols[i][index_sym]
                index_sym += 1

    # arr_symols = np.fft.fftshift(arr_symols, axes=1) # Лишний разворот
    
    # from .plots import cool_plot
    # cool_plot(np.ravel(arr_symols))
    
    # IFFT
    ifft = np.zeros((len(symbols), fft_len), dtype=complex)
    for i in range(len(arr_symols)):
        ifft[i] = np.fft.ifft(arr_symols[i])

    # Добавление циклического префикса
    fft_cp = np.zeros((len(symbols), (fft_len + _cyclic_prefix_len)), dtype=complex)
    for i in range(len(arr_symols)):
        fft_cp[i] = np.concatenate((ifft[i][-_cyclic_prefix_len:], ifft[i]))

    fft_cp = fft_cp * amplitude
    if ravel:
        ret = np.ravel(fft_cp)
        return ret

    return fft_cp

def get_sr_from_freq_step(freq_step, fft_len):
    """Какая должна быть частота дискретизации с определенным шагом между поднесущими и длинной FFT"""
    return freq_step * fft_len

def activ_carriers(fft_len, GB, PC, zero_64=False):
    """
    ml.activ_carriers(64, 6, (-21, -7, 7, 21), True)

    GB - guard_band_len

    PC - pilot_carriers
    
    Возвращает массив поднесущих на которых имеются данные
    """
    activ = np.array([
            i
            for i in range(-fft_len // 2, fft_len // 2)
            if i in range(-fft_len // 2 + GB, fft_len // 2 - GB + 1)
            and i not in PC
            and i != 0
        ])
    if zero_64:
        activ64 = np.array(activ)
        activ64[activ64 < 0] += 64
        return activ64
    else:
        return activ

def synchro_ofdm(rx):
    """
    Циклический префикс - 16

    fft - 64
    
    Возвращает массив начала символов (вместе с CP) (чтобы только символ был нужно index + 16)
    """
    corr = [] # Массив корреляции 
    for i in range(len(rx)):
        o = corr_no_shift(rx[:16], rx[64:80], complex=True)
        corr.append(abs(o))
        rx = np.roll(rx, 1)
        
    corr = np.array(corr) / np.max(corr) # Нормирование

    arr_index = [] # Массив индексов максимальных значений corr
    for i in range(0, len(corr)-80, 80):
        max = np.max(corr[i : i+80])
        if max > 0.9: 
            arr_index.append(i + np.argmax(corr[i : i+80]))
    
    ### DEBUG
    # print(arr_index)
    # from .plots import cool_plot
    # cool_plot(corr, title='corr')
    
    return arr_index
