"""
MyLib
=====

    import mylib as ml
    
    import mylib.test as mltest
  
Функции
--------
`BASE`
- str_to_bits
- bits_to_str
- merge_arr
- correlation
- corr_array
- auto_corr

`SDR`
- sdrSettings
- txSig
- rxCyclesBuffer

`Modulation`
- bpsk
- qpsk
- qam16
- qam64
* qpskDem
* bpskSynchro

`Plots`
- cool_scatter
- cool_plot
- angle_scatter
- eye_pattern

``by nicoskin``
"""

from .base import *
from .sdr import *
from .modulation import *
from .plots import *