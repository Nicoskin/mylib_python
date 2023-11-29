В папке библиотеки написать:    
`pip install -e .`


### Способы подключения 
```
import mylib as ml
from mylib.sdr import *
```


### mylib (функции стандарт)
```
corr()
str_to_bits()
bits_to_str()
merge_arr()
correlation()
corr_array()
autocorr()
```


### mylib.sdr
```
sdr_settings()
tx_sig()
rx_cycles_buffer()

bpsk()
qpsk()
qam16()

qpsk_synchro()
bpsk_sin()
```
