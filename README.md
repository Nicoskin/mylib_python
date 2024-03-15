В папке библиотеки написать:    
`pip install -e .`

<details >
<summary>Версии библиотек</summary>

matplotlib        3.8.2     
numpy             1.26.2        
typing_extensions 4.9.0     
pyadi-iio         0.0.16     
pylibiio          0.25

</details>

### Способы подключения 
```
import mylib as ml
ИЛИ
from mylib import *

import mylib.test as mltest
```


### mylib.base (функции стандарт)
```
str_to_bits
bits_to_str
gen_rand_bits
corr_no_shift
corr_array
autocorr
zadoff_chu
```


### mylib.sdr
```
sdr_settings
tx_sig
rx_cycles_buffer
```

### mylib.modulation
```
bpsk
qpsk
qam16
qam64
qam256

bpsk_synchro
dem_qpsk
dem_qam16
```

### mylib.ofdm
```
ofdm_64
get_sr_from_freq_step
activ_carriers
synchro_ofdm
```

### mylib.plots
```
cool_scatter
cool_plot
angle_scatter
eye_pattern
```

### mylib.test
```
check_hack
fast_qpsk
```

