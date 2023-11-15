def sdr_settings(ip = "ip:192.168.3.1", frequency=2e9, buffer_size = 1000, sample_rate = 1e6, tx_gain = 0, rx_gain=0):
    """
    Базовые настройки sdr
    
    sdr = sdr_settings("ip:192.168.3.1", 2300e6+(2e6*2), 1000, 1e6,0,30) # type: ignore
    
    Параметры
    ----------
        ip : "ip:192.168.3.1" / "ip:192.168.2.1"
        
        frequency : частота дискретизации
            от 325 [МГц] до 3.8 [ГГц]
        
        buffer_size = 1000, sample_rate = 1e6
        
        tx_gain : сила передачи
            рекомендуемое значение от 0 до -50
        
        rx_gain : чувствительность приёма
            рекомендуемое значение от 0 до -50
    """
    import adi
    sdr = adi.Pluto(ip)

    sdr.rx_lo = int(frequency)
    sdr.tx_lo = int(frequency)

    sdr.rx_buffer_size = buffer_size
    sdr.sample_rate = sample_rate
    sdr.gain_control_mode_chan0 = 'manual'
    sdr.tx_hardwaregain_chan0 = tx_gain # рекомендуемое значение от 0 до -50
    sdr.rx_hardwaregain_chan0 = rx_gain # рекомендуемое значение от 0 до -50

    return sdr

def str_to_bits(
    str: str, b_start: int | None = None, b_stop: int | None = None):
    """
    Преобразовает строку в битовую последовательность
    
    Параметры
    ----------
        b_start : количество единиц в начале
    
        b_stop : количество единиц в конце
    
        return : "битовая последовательность"
    """
    import numpy as np
    encoded_bytes = str.encode('ascii')
    # Преобразование байтов в массив битов
    bit_array = []
    for byte in encoded_bytes:
        bits = bin(byte)[2:].zfill(8)  # Преобразование в биты
        bit_array.extend([int(bit) for bit in bits])

    if b_start is not None and b_stop is None:
        bit_start = np.ones(b_start)
        
        bit_array_list = list(bit_array)
        bit_array_list = list(bit_start) + bit_array_list
        bit_array = np.array(bit_array_list)

    elif b_start is not None and b_stop is not None:
        bit_start = np.ones(b_start)
        bit_stop = np.ones(b_stop)

        bit_array_list = list(bit_array)
        bit_array_list = list(bit_start) + bit_array_list + list(bit_stop)
        bit_array = np.array(bit_array_list)

    return bit_array

def tx_sig(samples, tx_cycle: bool = True):
    """
    Функция передает samples на TX
    
    !!! Нужно sdr !!!
    
        tx_cycle : по станадрту передает в цикле
        
    не забывай сбрасывать в конце проги 
        " sdr.tx_destroy_buffer() "
    """
    try:
        sdr.tx_cyclic_buffer = tx_cycle
        sdr.tx(samples)
    except NameError:
        print("Переменная 'sdr' не определена.")
        return -1

def rx_cycles_buffer(num_cycles: int = 1):
    """
    Получает циклически сигнал с RX 
    
    !! Нужна настройка sdr !! 
    
    Параметры
    --------
        num_cycles : сколько раз получает буфер rx
        
        return : выводит rx
    
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
