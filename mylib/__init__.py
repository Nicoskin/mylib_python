"""
MyLib
=====

  >>> import mylib as ml
  >>> from mylib.sdr import *
  
Функции
--------
`MAIN`
- corr()

`SDR`
- sdr_settings()
- str_to_bits()
- bits_to_str()
- tx_sig()
- rx_cycles_buffer()

Модуляция:
    - bpsk()
    - qpsk()
        - qpsk_synchro()
    - qam16()
"""

def corr(x, y, norm=True):
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
    import numpy as np
    x = np.asarray(x)
    y = np.asarray(y)

    if norm:
        c = np.dot(x, y) / (np.linalg.norm(x) * np.linalg.norm(y))
        return c
    else:
        c = np.dot(x, y)
        return c