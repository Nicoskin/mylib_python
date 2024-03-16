"""
MyLib
=====

import mylib as ml  
    
from mylib import ic  
        
import mylib.test as mltest     
  
Функции
--------
`BASE`
- str_to_bits
- bits_to_str
- gen_rand_bits
- correlation
- corr_array
- auto_corr
- zadoff_chu

`SDR`
- sdr_settings
- tx_sig
- rx_cycles_buffer

`Modulation`
- bpsk
- qpsk
- qam16
- qam64
- qam256
* dem_qpsk
* dem_qam16
* bpsk_synchro

`Class_OFDM`
- OFDM_MOD
    - modulation
    - fft
    - get_sr_from_freq_step
    - activ_carriers
    - indiv_symbols
        - indexs_of_CP

`Plots`
- cool_scatter
- cool_plot
- angle_scatter
- eye_pattern
- heat_map

``by nicoskin``
"""

from .base import *
from .sdr import *
from .modulation import *
from .plots import *
from .ofdm import *
from .class_ofdm import *

from icecream import ic
__all__ = ['ic']