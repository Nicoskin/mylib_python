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
str_to_bits()
bits_to_str()
merge_arr()
corr_no_shift()
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

### mylib.plots
```
cool_scatter()
cool_plot()
angle_scatter()
```

### mylib.test
```
check_hack()
fast_qpsk()
```

