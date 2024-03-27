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
    
        self.CP_len = int(self.N_fft / 4)
        if GB == 0:
            self.GB_len = self._calculate_gb_length()
        else:
            self.GB_len = GB

        if N_pilot is None:
            N_pilot = int(0.1 * N_fft)  # Default: 10% of subcarriers for pilots
    
        self.pilot_carriers = self._generate_pilot_carriers(N_pilot)
        self.pilot_symbols = self._generate_pilot_symbols(N_pilot)


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
        #ic(usable_bandwidth,pilot_spacing)
        # Можно менять значение от 0 до 1
        #                          ↓
        pilot_carriers = np.arange(0 + self.GB_len//2, self.N_fft - self.GB_len//2+1, pilot_spacing)
        #pilot_carriers = np.linspace(0 + self.GB_len//2, self.N_fft - self.GB_len//2+1, N_pil)

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
        pilot_symbols = [2+2j] * N_pilot
        return pilot_symbols

    def activ_carriers(self, pilots = False):
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

    def add_pss(self, symbols): 
        """
        Добавление PSS 
        
        Работает правильно
        """
        #len_subcarr = len(self.activ_carriers(True))
        
        pss = ml.zadoff_chu(PSS=True) * 2
        arr = np.zeros(self.N_fft, dtype=complex)

        # Массив с защитными поднесущими и 0 в центре
        arr[self.N_fft//2 - 31 : self.N_fft//2] = pss[:31]
        arr[self.N_fft//2 + 1: self.N_fft//2 + 32] = pss[31:]
        
        symbols = np.insert(symbols, 0, arr, axis=0)
        
        for i in range(6, symbols.shape[0], 6):
            symbols = np.insert(symbols, i, arr, axis=0)

        return symbols

    def modulation(self, amplitude=2**15, ravel=True):
        """
        OFDM модуляция.

        Args:
            symbols (np.ndarray): Массив символов QAM.
            ravel (bool, optional): Если True, возвращает одномерный массив OFDM-сигналов. 
                Defaults to True.

        Returns:
            np.ndarray: Массив OFDM-сигналов.
        """
        # Разделение массива symbols на матрицу(по n в строке)
        def reshape_symbols(symbols, activ):
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
            
            return symbols

        def distrib_subcarriers(symbols, activ, fft_len):
            len_symbols = np.shape(symbols)
            # Создание матрицы, в строчке по n символов QPSK
            if len(len_symbols) > 1: 
                arr_symols = np.zeros((len_symbols[0], fft_len), dtype=complex)
            else: # если данных только 1 OFDM символ
                arr_symols = np.zeros((1, fft_len), dtype=complex)
            
            # Распределение строк символов по OFDM символам(с GB и пилотами)
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
            
            return arr_symols

        fft_len = self.N_fft
        _cyclic_prefix_len = self.CP_len
        _guard_band_len = self.GB_len
        symbols = self.QAM_sym
        activ = self.activ_carriers()

        # Делим массив символов на матрицу
        #(в строке элеметнов = доступных поднесущих)
        symbols = reshape_symbols(symbols, activ)
        ic(np.shape(symbols))
        # Добавление нулевых строк для чётности "5"
        if np.shape(symbols)[0] % 5 != 0:
            zero = np.zeros((5 - np.shape(symbols)[0] % 5, len(activ)))
            symbols = np.concatenate((symbols, zero))
        
        arr_symols = distrib_subcarriers(symbols, activ, fft_len)
        ic(np.shape(arr_symols))
        #ml.cool_plot(np.ravel(arr_symols))
        arr_symols = self.add_pss(arr_symols)
        ic(np.shape(arr_symols)) 
        #ml.cool_plot(np.ravel(arr_symols))     
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

        if corr[0] > 0.97:
            max_len_cycle = len(corr)
        else:
            max_len_cycle = len(corr)-(fft_len+cp)

        arr_index = [] # Массив индексов максимальных значений corr
        for i in range(0, max_len_cycle, (fft_len+cp)):
            #print(i, i+(fft_len+cp))
            max = np.max(corr[i : i+(fft_len+cp)])
            if max > 0.9: 
                ind = i + np.argmax(corr[i : i+(fft_len+cp)])
                if ind < (len(corr)-(fft_len+cp)):
                    arr_index.append(ind)
        
        ### DEBUG
        print(arr_index)
        # print(corr)
        from mylib import cool_plot
        cool_plot(corr, title='corr', show_plot=False)
        
        return arr_index

    def corr_pss_time(self, rx):
        """
        """
        from mylib import corr_no_shift
        cp = self.CP_len
        fft_len = self.N_fft
        pss = ml.zadoff_chu(PSS = True)
        
        zeros = fft_len // 2 - 31
        pss_ifft = np.insert(pss, 32, 0)
        pss_ifft = np.insert(pss_ifft, 0, np.zeros(zeros))
        pss_ifft = np.append(pss_ifft, np.zeros(zeros-1))
        
        pss_ifft = np.fft.fftshift(pss_ifft)
        pss_ifft = np.fft.ifft(pss_ifft)
        pss_if = pss_ifft[33:96]
        
        corr = [] # Массив корреляции 
        for i in range(len(rx) - 63):
            o = corr_no_shift(rx[i : i+63], pss_if, complex=True)
            corr.append(abs(o))
        
        corr = np.array(corr) / np.max(corr)
        
        #maxi = np.argmax(corr)
        for i in range(len(corr)):
            if corr[i] > 0.95:
                maxi = i
                break
        maxi = maxi - 31 - cp-2
        print('corr_pss_time',maxi)
        from mylib import cool_plot
        cool_plot(corr, title='corr_pss_time', show_plot=False)
        
        rx = rx[maxi:maxi + (self.N_fft + self.CP_len) * 6]
        
        return rx

    def corr_pss_freq(self, rx):
        """
        """
        from mylib import corr_no_shift
        cp = self.CP_len
        fft_len = self.N_fft
        pss = ml.zadoff_chu(PSS = True)
        
        zeros = fft_len // 2 - 31
        pss_ifft = np.insert(pss, 32, 0)
        
        corr = [] # Массив корреляции 
        for i in range(len(rx) - 63):
            o = corr_no_shift(rx[i : i+63], pss_ifft, complex=True)
            corr.append(abs(o))
        
        corr = np.array(corr) / np.max(corr)
        
        #maxi = np.argmax(corr)
        for i in range(len(corr)):
            if corr[i] > 0.95:
                maxi = i
                break
        maxi = maxi - 33
        print('corr_pss_freq',maxi)
        from mylib import cool_plot
        cool_plot(corr, title='corr_pss_freq', show_plot=False)
        
        rx = rx[maxi:maxi + (self.N_fft + self.CP_len) * 6]
        
        return rx

    def correct_frequency_offset(self, signal):
        def frequency_offset_estimation(rx, index_pss, sample_rate):
            received_pss = ml.zadoff_chu(PSS=True)
            received_pss = np.insert(received_pss, 32, 0)
            expected_pss = rx[index_pss:index_pss + 63]
            phase_difference = np.angle(np.dot(received_pss, np.conj(expected_pss)))
            # Time duration for transmitting PSS, in seconds
            time_duration_pss = 63 / sample_rate # 62
            # Convert phase difference to frequency offset in Hz
            frequency_offset = (phase_difference / (2 * np.pi)) / time_duration_pss
            
            return frequency_offset
        
        sample_rate = self.N_fft * 15000
        index_pss = self.corr_pss_time(signal)
        frequency_offset = frequency_offset_estimation(signal, index_pss, sample_rate)
        ic(frequency_offset)
        signal = np.array(signal, dtype=np.complex128)
        
        time = len(signal) / sample_rate
        correction = np.exp(-1j * 2 * np.pi * frequency_offset * time)
        corrected_signal = signal * correction

        return corrected_signal


    def freq_syn(self, ofdm, indexs):
        """
        Реализует синхронизацию частоты с помощью оценки фазы на основе корреляции.

        Args:
            ofdm (numpy.ndarray): Принятый OFDM-сигнал в частотной области.
            indexs (list): Список индексов, указывающих начальные точки символов,
                        которые будут использоваться для синхронизации частоты.

        Returns:
            numpy.ndarray: OFDM-сигнал с синхронизированной частотой.
        """

        cp = self.CP_len  # Длина циклического префикса
        all_sym = self.N_fft + cp  # Общая длина символа (включая CP)

        for ind in indexs:
            # Нормализация первого и второго циклических префиксов (CP)
            fir = (ofdm[ind:ind + cp] / np.abs(ofdm[ind:ind + cp])).flatten()
            sec = (ofdm[ind + all_sym - cp:ind + all_sym] / np.abs(ofdm[ind + all_sym - cp:ind + all_sym])).flatten()

            # Расчет фазового сдвига с помощью нормированной кросс-корреляции
            eps = (1 / (2 * np.pi)) * np.sum(fir * sec.conj())  # Сопряженное для комплексной корреляции

            # Коррекция фазы для всех отсчетов в пределах символа
            for i in range(all_sym):
                ofdm[ind + i] *= np.exp(-1j * 2 * np.pi * eps * i / self.N_fft)

        return ofdm

    def indiv_symbols(self, ofdm):
        cp = self.CP_len
        all_sym = self.N_fft + cp
        
        index = self.indexs_of_CP(ofdm)
        #ofdm = self.freq_syn(ofdm, index)
        
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
                zn = zn[self.activ_carriers()]
            elif (GB is True):
                pass
            else:
                zn = zn[self.activ_carriers(True)]
                
            fft.append(zn)
                
        if ravel:
            ret = np.ravel(fft)
            return ret
        else:
            return fft  