В папке библиотеки написать:    
`pip install -e .`


### Способы подключения 
```
import mylib as ml
ИЛИ
from mylib import *

from mylib.test import * 
```


### mylib.base (функции стандарт)
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
```

### mylib.modulation
```
bpsk()
qpsk()
qam16()
qam64()

bpsk_synchro()
```

### mylib.test
```
check_hack()
fast_qpsk()
```