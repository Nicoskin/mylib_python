"""
"""

import numpy as np
from icecream import ic
import mylib as ml

class OFDM_MOD:
    """
    N_FFT: 64 128 256 512 1024 1536 2048
    
    Oc Sc: 39 73 181 301 601 901 1201
    
    G Sc: 25 55 75 211 423 635 847
    """
    def __init__(self, QAM_sym, N_fft: int = 64, GB = 0, N_pilot = None):
        self.N_fft = N_fft
        self.QAM_sym = QAM_sym

        if N_fft not in (64, 128, 256, 512, 1024, 2048):
            raise ValueError("Invalid N_fft. Valid options are 64, 128, 256, 512, 1024, 2048.")
    
        self.CP_len = self._calculate_cp_length()
        if GB == 0:
            self.GB_len = self._calculate_gb_length()
        else:
            self.GB_len = GB

        if N_pilot is None:
            N_pilot = int(0.1 * N_fft)  # Default: 10% of subcarriers for pilots
    
        self.pilot_carriers = self._generate_pilot_carriers(N_pilot)
        self.pilot_symbols = self._generate_pilot_symbols(N_pilot)

    def _calculate_cp_length(self):
        return int(self.N_fft / 4)  

    def _calculate_gb_length(self):
        match self.N_fft:
            case 64:
                return 27
            case 128:
                return 55
            case 256:
                return 75
            case 512:
                return 211
            case 1024:
                return 423
            case 2048:
                return 847
            case _:
                return 27
            
        return int(0.1 * N_fft)  # Example: GB length = 10% of N_fft

    def _generate_pilot_carriers(self, N_pil):
        """
        Generates indices representing pilot subcarriers.

        Args:
            N_pilot (int): Number of pilot subcarriers.

        Returns:
            np.ndarray: Array of pilot subcarrier indices within the usable bandwidth.
        """
        usable_bandwidth = self.N_fft - self.GB_len
        pilot_spacing = int(usable_bandwidth / (N_pil - 1))  # Spacing between pilots

        # Можно менять значение от 0 до 1
        #                          ↓
        pilot_carriers = np.arange(0 + self.GB_len//2, self.N_fft - self.GB_len//2+1, pilot_spacing)

        for i in range(len(pilot_carriers)):
            if pilot_carriers[i] == 32:
                pilot_carriers[i] += 1
            
        # Handle potential rounding errors or edge cases
        if len(pilot_carriers) < N_pil:
            pilot_carriers = np.concatenate((pilot_carriers, [self.N_fft // 2 + 1]))  # Add center carrier if needed
        elif len(pilot_carriers) > N_pil:
            pilot_carriers = pilot_carriers[:N_pil]  # Truncate if there are too many

        return pilot_carriers
    
    def _generate_pilot_symbols(self, N_pilot):
        """
        Generates complex symbols to be assigned to pilot subcarriers.

        Args:
            N_pilot (int): Number of pilot subcarriers.

        Returns:
            np.ndarray: Array of complex pilot symbols based on the chosen constellation.
        """
        # Example using QPSK constellation:
        #pilot_symbols = np.exp(1j * np.pi * np.random.randint(0, 4, size=N_pilot))
        pilot_symbols = [1+1j] * N_pilot
        return pilot_symbols

    def get_sr_from_freq_step(self):
        """Какая должна быть частота дискретизации с определенным шагом между поднесущими и длинной FFT"""
        return self.N_fft * 15000

    def activ_carriers(self, pilots = True):
        """
        ml.activ_carriers(64, 6, (-21, -7, 7, 21), True)

        GB - guard_band_len

        PC - pilot_carriers
        
        Возвращает массив поднесущих на которых имеются данные
        """
        fft_len = self.N_fft
        GB = self.GB_len // 2
        PilCar = self.pilot_carriers

        if pilots:
            activ = np.array([
                    i
                    for i in range(0, fft_len)
                    if (i in range(GB, fft_len - GB + 1))
                    and (i != fft_len/2)
                ])
        else:
            activ = np.array([
                    i
                    for i in range(0, fft_len)
                    if (i in range(GB, fft_len - GB + 1))
                    and (i not in PilCar)
                    and (i != fft_len/2)
                ])
        
        #activ = activ + (self.N_fft / 2)
        
        return activ

    def modulation(self, amplitude=2**16, ravel=True):
        """
        OFDM модуляция.

        Args:
            symbols (np.ndarray): Массив символов QAM.
            ravel (bool, optional): Если True, возвращает одномерный массив OFDM-сигналов. 
                Defaults to True.

        Returns:
            np.ndarray: Массив OFDM-сигналов.
        """

        fft_len = self.N_fft
        _cyclic_prefix_len = self.CP_len
        _guard_band_len = self.GB_len
        symbols =  self.QAM_sym

        activ = self.activ_carriers()

        # Разделение массива symbols на матрицу(по n в строке)
        len_arr = len(activ)
        try:
            if (len(symbols) % len_arr) != 0:
                symbols1 = np.array_split(
                    symbols[: -(len(symbols) % len_arr)], len(symbols) / len_arr)
                symbols2 = np.array((symbols[-(len(symbols) % len_arr) :]))
                zeros_last = np.zeros(len_arr - len(symbols2))
                symbols2 = np.concatenate((symbols2, zeros_last))
                symbols1.append(symbols2)
                symbols = symbols1
            else:
                symbols = np.array_split(symbols, len(symbols) / len_arr)
        except ValueError:
            zero = np.zeros(len_arr - len(symbols))
            symbols = np.concatenate((symbols, zero))
        
        len_symbols = np.shape(symbols)
        
        
        # Создание матрицы, в строчке по n символов QPSK
        if len(len_symbols) > 1: 
            arr_symols = np.zeros((len_symbols[0], fft_len), dtype=complex)
        else: # если данных только 1 OFDM символ
            arr_symols = np.zeros((1, fft_len), dtype=complex)
            
        for i, symbol in enumerate(arr_symols):
            index_pilot = 0
            index_sym = 0
            for j in range(len(symbol)):
                if j in self.pilot_carriers:
                    arr_symols[i][j] = self.pilot_symbols[index_pilot]
                    index_pilot += 1
                elif (j in activ) and (index_sym < len_symbols[-1]):
                    if len(len_symbols) > 1:
                        arr_symols[i][j] = symbols[i][index_sym]
                    else:
                        arr_symols[i][j] = symbols[index_sym]
                    index_sym += 1
   
        arr_symols = np.fft.fftshift(arr_symols, axes=1)

        # IFFT
        ifft = np.zeros((np.shape(arr_symols)[0], fft_len), dtype=complex)
        for i in range(len(arr_symols)):
            ifft[i] = np.fft.ifft(arr_symols[i])

        # Добавление циклического префикса
        fft_cp = np.zeros((np.shape(arr_symols)[0], (fft_len + _cyclic_prefix_len)), dtype=complex)
        for i in range(np.shape(arr_symols)[0]):
            fft_cp[i] = np.concatenate((ifft[i][-_cyclic_prefix_len:], ifft[i]))
        
        fft_cp = fft_cp * amplitude
        
        if ravel:
            return np.ravel(fft_cp)
        return fft_cp

    def indexs_of_CP(self, rx):
        """
        Возвращает массив начала символов (вместе с CP) (чтобы только символ был нужно index + 16)
        """
        from mylib import corr_no_shift
        cp = self.CP_len
        fft_len = self.N_fft
        
        corr = [] # Массив корреляции 
        for i in range(len(rx)):
            o = corr_no_shift(rx[:cp], rx[fft_len:fft_len+cp], complex=True)
            corr.append(abs(o))
            rx = np.roll(rx, 1)
            
        corr = np.array(corr) / np.max(corr) # Нормирование

        if corr[0] > 0.98:
            max_len_cycle = len(corr)
        else:
            max_len_cycle = len(corr)-(fft_len+cp)

        arr_index = [] # Массив индексов максимальных значений corr
        for i in range(0, max_len_cycle, (fft_len+cp)):
            max = np.max(corr[i : i+(fft_len+cp)])
            if max > 0.9: 
                ind = i + np.argmax(corr[i : i+(fft_len+cp)])
                if ind < (len(corr)-(fft_len+cp)):
                    arr_index.append(ind)
        
        ### DEBUG
        # print(arr_index)
        # print(corr)
        # from mylib import cool_plot
        # cool_plot(corr, title='corr', show_plot=False)
        
        return arr_index

    def indiv_symbols(self, ofdm):
        cp = self.CP_len
        all_sym = self.N_fft + cp
        
        index = self.indexs_of_CP(ofdm)
        symbols = []
        for ind in index:
            symbols.append(ofdm[ind+cp : ind+all_sym])
            
        return symbols

    def fft(self, ofdm_symbols, ravel = True, GB = False, pilots = True):
        fft = []
        len_c = np.shape(ofdm_symbols)[0]
        for i in range(len_c):
            if len_c == 1:
                zn = np.fft.fftshift(np.fft.fft(ofdm_symbols))
            else:
                zn = np.fft.fftshift(np.fft.fft(ofdm_symbols[i]))
                
            if (GB is False) and (pilots is False):
                zn = zn[self.activ_carriers(False)]
            elif (GB is True):
                pass
            else:
                zn = zn[self.activ_carriers()]
                
            fft.append(zn)
                
        if ravel:
            ret = np.ravel(fft)
            return ret
        else:
            return fft