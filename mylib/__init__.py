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

`Modulation`:
    - bpsk()
        - bpsk_synchro()
    - qpsk()
    - qam16()
    - qam64()
   
"""

from .base import *
from .sdr import *
from .modulation import *