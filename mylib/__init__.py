"""
MyLib
=====

  import mylib as ml
  
Функции
--------
`BASE`
- str_to_bits()
- bits_to_str()
- merge_arr()
- correlation()
- corr_array()
- autocorr()

`SDR`
- sdr_settings()
- tx_sig()
- rx_cycles_buffer()

Модуляция:
    - bpsk()
    - qpsk()
        - qpsk_synchro()
    - qam16()
    - bpsk_synchro()
    - qam64()
   
"""

from .base import *
from .sdr import *