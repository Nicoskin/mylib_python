"""
`SDR`
- sdr_settings()
- tx_sig()
- rx_cycles_buffer()
  
"""

def sdr_settings(ip = "ip:192.168.3.1",
                 frequency = 2e9,
                 buffer_size = 1e3,
                 sample_rate = 1e6,
                 tx_gain = 0, rx_gain = 0,
                 mode = 'manual'):
    """
    Базовые настройки sdr
    
    sdr = sdr_settings("ip:192.168.3.1")
    sdr = sdr_settings("ip:192.168.3.1", 2300e6+(2e6*2), 1000, 1e6,0,30) # type: ignore
    
    Параметры
    ----------
        `ip` : "ip:192.168.3.1" / "ip:192.168.2.1"
        
        `frequency` : частота дискретизации
            от 325 [МГц] до 3.8 [ГГц] | 
            hacked 70 [МГц] до 6 [ГГц]
            
        `buffer_size` = 1e3 [samples]
        
        `sample_rate` = 1e6 [samples]
        
        `tx_gain`: сила передачи [dBm]
            рекомендуемое значение от -90 до 0 [дБ]
            
        `rx_gain`: чувствительность приёма [dBm]
            рекомендуемое значение от 0 до 74,5 [дБ]
            
        `mode` : str, optional
            slow_attack, fast_attack, manual
            
    Возвращает
    ----------  
        `sdr`: настроенный класс "sdr"
    """    
    import adi
    sdr = adi.Pluto(ip)

    sdr.rx_lo = int(frequency)
    sdr.tx_lo = int(frequency)

    sdr.tx_destroy_buffer()
    sdr.rx_destroy_buffer()

    sdr.rx_buffer_size = int(buffer_size)
    sdr.sample_rate = int(sample_rate)
    sdr.gain_control_mode_chan0 = mode
    sdr.tx_hardwaregain_chan0 = tx_gain # допустимый диапазон составляет от -90 до 0 дБ
    sdr.rx_hardwaregain_chan0 = rx_gain # допустимый диапазон составляет от 0 до 74,5 дБ

    return sdr

def tx_sig(sdr, samples, tx_cycle: bool = True):
    """
    Функция передает samples на TX
    
    !!! Нужна настроенная sdr !!!
    
    Параметры
    ----------
        `sdr` : переменная sdr
        
        `samples` : значения сэмплов которые нужно передать
        
        `tx_cycle`: по стандарту передает в цикле
        
    Не забывай сбрасывать буфер в конце проги 
        " sdr.tx_destroy_buffer() "
    ^^^^
    """
    try:
        sdr.tx_cyclic_buffer = tx_cycle
        sdr.tx(samples)
    except NameError:
        print("(ERROR MyLib): Переменная 'sdr' не определена.")
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
    from numpy import array 
    
    rx = []
    try:
        for cycle in range(num_cycles):  # Считывает num_cycles циклов Rx
            new_data = sdr.rx()
            rx.extend(new_data)
        return array(rx)
    except NameError:
        print("(ERROR MyLib): Переменная 'sdr' не определена.")
        return -1

