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
    def __init__(self, QAM_sym = None, N_fft: int = 128, GB = 0, N_pilot = None):
        self.N_fft = N_fft
        self.QAM_sym = QAM_sym

        if N_fft not in (64, 128, 256, 512, 1024, 2048):
            raise ValueError("Invalid N_fft. Valid options are 64, 128, 256, 512, 1024, 2048.")
    
        self.CP_len = int(self.N_fft / 4)
        if GB == 0:
            self.GB_len = self._calculate_gb_length()
        else:
            self.GB_len = GB

        if (N_pilot is None) or (N_pilot == 1):
            N_pilot = int(0.1 * N_fft)  # Default: 10% of subcarriers for pilots
    
        self.pilot_carriers = self._generate_pilot_carriers(N_pilot)
        self.pilot_symbols = self._generate_pilot_symbols(N_pilot)

    def print(self):
        def add_blue(string):
            return '\033[94m' + str(string) + '\033[0m'
        
        a = '\033[42m' +  ' Параметры класса OFDM_MOD ' + '\033[0m'
        print()
        print(f"{a:^50}")
        print(f"{'Кол-во поднесущих':<30}", "│", f"{add_blue(self.N_fft)}")
        print(f"{'Циклический префикс':<30}", "│", f"{add_blue(self.CP_len)}")
        print(f"{'Защитные(нулевые) поднесущие':<30}", "│", f"{add_blue(self.GB_len)}")
        print(f"{'─'*31 + '┼' + '──'}")
        print(f"{'Кол-во символов с данными':<30}", "│", f"{add_blue(len(self.QAM_sym))}")
        from math import ceil
        print(f"{'Кол-во OFDM символов с данными':<30}", "│", f"{add_blue(ceil(len(self.QAM_sym) / len(self.activ_carriers())))}")
        print(f"{'Кол-во слотов':<30}", "│", f"{add_blue(ceil(len(self.QAM_sym) / len(self.activ_carriers()) / 6))}")
        print(f"{'─'*31 + '┼' + '──'}")
        print(f"{'Кол-во пилотов':<30}", "│", f"{add_blue(len(self.pilot_carriers))}")
        print(f"{'Индексы поднесущих с пилотами':<30}", "│", f"{add_blue(self.pilot_carriers)}")
        print()


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
        
        pilot_carriers[-1] = self.N_fft - self.GB_len//2 # Последний пилот на последней доступной поднесущей
        
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
        #ic(np.shape(symbols))
        # Добавление нулевых строк для чётности "5"
        if np.shape(symbols)[0] % 5 != 0:
            zero = np.zeros((5 - np.shape(symbols)[0] % 5, len(activ)))
            symbols = np.concatenate((symbols, zero))
        
        arr_symols = distrib_subcarriers(symbols, activ, fft_len)
        #ic(np.shape(arr_symols))
        #ml.cool_plot(np.ravel(arr_symols))
        arr_symols = self.add_pss(arr_symols)
        #ic('distrib_subcarriers | Количество OFDM символов', np.shape(arr_symols)) 
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
            rx = np.roll(rx, -1)
            
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
        #from mylib import cool_plot
        #cool_plot(corr, title='corr', show_plot=False)
        
        return arr_index

    def indexs_of_CP_after_PSS(self, rx):
        """
        Возвращает массив начала символов (вместе с CP) (чтобы только символ был нужно index + 16)
        """
        from mylib import corr_no_shift
        cp = self.CP_len
        fft_len = self.N_fft
        
        corr = [] # Массив корреляции 
        for i in range(len(rx) - fft_len):
            o = corr_no_shift(rx[:cp], rx[fft_len:fft_len+cp], complex=True)
            corr.append(abs(o))
            rx = np.roll(rx, -1)
            
        corr = np.array(corr) / np.max(corr) # Нормирование
        max_len_cycle = len(corr)
        # if corr[0] > 0.97:
        #     max_len_cycle = len(corr)
        # else:
        #     max_len_cycle = len(corr)-(fft_len+cp)

        ind = np.argmax(corr[0 : (fft_len+cp)// 2 ])
        arr_index = [] # Массив индексов максимальных значений corr
        arr_index.append(ind)
        for i in range((fft_len+cp) // 2, max_len_cycle, (fft_len+cp)):
            #print(i, i+(fft_len+cp))
            max = np.max(corr[i : i+(fft_len+cp)])
            if max > 0.9: 
                ind = i + np.argmax(corr[i : i+(fft_len+cp)])
                if ind < (len(corr)):
                    arr_index.append(ind)
        
        ### DEBUG
        print(arr_index)
        # print(corr)
        #from mylib import cool_plot
        #cool_plot(corr, title='corr afte PSS', show_plot=False)
        
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
        #ml.cool_plot(corr, show_plot=True)
        #maxi = np.argmax(corr)
        for i in range(len(corr)):
            if corr[i] > 0.98:
                maxi = i
                break
        maxi = maxi - 31 - cp-2
        #print('corr_pss_time',maxi)
        from mylib import cool_plot
        cool_plot(corr, title='corr_pss_time', show_plot=False)
        
        #rx = rx[maxi:maxi + (self.N_fft + self.CP_len) * 6]
        
        return maxi

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
        #from mylib import cool_plot
        #cool_plot(corr, title='corr_pss_freq', show_plot=False)
        
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
        #ic(frequency_offset)
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

    def indiv_symbols(self, ofdm, pss=True):
        cp = self.CP_len
        all_sym = self.N_fft + cp
        
        if pss:
            index = self.indexs_of_CP_after_PSS(ofdm)
        else:
            index = self.indexs_of_CP(ofdm)
        #ic(index)
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
    
    def interpol_pilots_test(self, ofdm_symbols):
        # Индексы пилотов, без защитных поднесущих
        ind_pilots = self.pilot_carriers - self.GB_len // 2
        for i in range(len(ind_pilots)//2, len(ind_pilots)):
            ind_pilots[i] -= 1
        print(ind_pilots)
        # Вычисление ФФТ
        rx_fft = self.fft(ofdm_symbols, GB=False)
        # Преобразование ФФТ в массив символов
        fft_symbols = np.reshape(rx_fft, (-1, self.N_fft - self.GB_len + 1))

        arr = []
        for sym in fft_symbols:
            Hls = sym[ind_pilots] / (1+1j)
            arr.append(Hls)
            
        H_pil = np.ravel(arr)
        H_pil = np.reshape(H_pil, (-1, len(self.pilot_carriers)))
        print(np.shape(H_pil))
        arr_interp = []
        x = np.arange(0, ind_pilots[-1])
        for n_pil in H_pil:
            inter = np.interp(x, ind_pilots, n_pil)
            arr_interp.append(inter)
            
        ml.cool_plot(np.ravel(arr))
        ml.cool_plot(np.ravel(arr_interp))
        #ml.cool_plot(np.ravel(arr_interp))
        rotated_symbols = []
        #phase = np.angle(np.ravel(arr_interp))
        #ic(phase)
        for sym, interp in zip(rx_fft, arr_interp):
            a = sym / (interp)
            rotated_symbols.append(a)
            # a = sym * np.exp(-1j * phase)
            # rotated_symbols.append(a)
        #rotated_symbols = ofdm_symbols * np.ravel(arr_interp)
        # import matplotlib.pyplot as plt
        # plt.figure(1)
        # plt.plot(phase)
        
        
        #ml.cool_plot(np.ravel(rotated_symbols), title="Rotated symbols")
        ml.cool_scatter(np.ravel(rotated_symbols), title="Rotated symbols")
        
    
    def interpol_pilots(self, ofdm_symbols):
        # Индексы пилотов
        ind_pilots = self.pilot_carriers - self.GB_len // 2
        for i in range(len(ind_pilots)//2, len(ind_pilots)):
            ind_pilots[i] -= 1
        # Вычисление ФФТ
        rx_fft = self.fft(ofdm_symbols, GB=False)
        ml.cool_scatter(rx_fft)
        ml.cool_plot(rx_fft)
        # Преобразование ФФТ в массив символов
        fft_symbols = np.reshape(rx_fft, (-1, self.N_fft - self.GB_len + 1))

        # Интерполяция фаз пилотов
        interpolated_phases = []
        for sym in fft_symbols:
            phase_pil = np.angle(sym[ind_pilots]) - np.angle(1 + 1j)
            interpolated_phase = []
            for i in range(len(ind_pilots) - 1):
                # Интерполяция между фазами соседних пилотов
                ad = np.linspace(phase_pil[i], phase_pil[i + 1],
                                ind_pilots[i + 1] - ind_pilots[i] + 1)
                interpolated_phase.extend(ad)
            interpolated_phases.append(interpolated_phase)

        # Интерполяция амплитуды пилотов
        interpolated_amplitudes = []
        for sym in fft_symbols:
            amp_pil = sym[ind_pilots]
            interpolated_amp = []
            for i in range(len(ind_pilots) - 1):
                # Интерполяция между фазами соседних пилотов
                ad = np.linspace(amp_pil[i], amp_pil[i + 1],
                                ind_pilots[i + 1] - ind_pilots[i] + 1)
                interpolated_amp.extend(ad)
            interpolated_amplitudes.append(interpolated_amp)
        
        for i in range(len(interpolated_phases)):
            interpolated_phases[i] = interpolated_phases[i][:len(fft_symbols[0])]
        # import matplotlib.pyplot as plt
        # plt.figure(22)
        # plt.plot(np.ravel(interpolated_amplitudes))
        # plt.figure(21)
        # plt.plot(np.ravel(interpolated_phases))
        # plt.show()
        # Развертка символов по углам пилотов
        rotated_symbols = []
        for sym, phase, amp in zip(fft_symbols, interpolated_phases, interpolated_amplitudes):
            rotated_symbol = sym * np.exp(-1j * np.array(phase))
            # Добавление коррекции по амплитуде
            amplitude_correction = amp# / np.abs(rotated_symbol[ind_pilots])
            #rotated_symbol *= amplitude_correction
            rotated_symbols.append(rotated_symbol)

        ml.cool_plot(np.ravel(rotated_symbols))
        return np.ravel(rotated_symbols)[self.N_fft - self.GB_len + 1:]



    def del_pilots(self, rotated_symbols):
        maxi = np.abs(np.max(rotated_symbols))
        rotated_symbols_maxi = np.array(rotated_symbols) / maxi * 3 
        ml.cool_scatter(rotated_symbols_maxi)
        #ml.cool_plot(abs(rotated_symbols_maxi))
        out = []
        for i in range(len(rotated_symbols_maxi)):
            if (abs(rotated_symbols_maxi[i]) < 1.5) and (abs(rotated_symbols_maxi[i]) > 0.2):# and rotated_symbols_maxi[i] > 0.1:
                out.append(rotated_symbols_maxi[i])
        return np.array(out)
    
    def calculate_correlation(pss, matrix_name, m):
        """
        Вычисляет корреляцию между pss и matrix_name с фильтрацией и задержкой.

        Args:
            pss: Опорный сигнал.
            matrix_name: Сигнал для сравнения с pss.
            m: Децимационный коэффициент.

        Returns:
            Кортеж, содержащий корреляцию и смещение несущей частоты (CFO).
        """
        L = len(pss)

        # Отраженный и комплексно-сопряженный опорный сигнал
        corr_coef = np.flip(np.conj(pss))

        # Фильтрация участков опорного сигнала
        partA = np.convolve(corr_coef[:L // 2], matrix_name, mode='same')
        xDelayed = np.concatenate((np.zeros(L // 2), matrix_name[:-L // 2]))
        partB = np.convolve(corr_coef[L // 2:], xDelayed, mode='same')

        # Вычисление корреляции и фазовой разницы
        correlation = np.abs(partA + partB)
        phaseDiff = partA * np.conj(partB)

        # Поиск максимальной корреляции и соответствующей фазовой разницы
        istart = np.argmax(correlation)
        phaseDiff_max = phaseDiff[istart]

        # Вычисление смещения несущей частоты (CFO)
        CFO = np.angle(phaseDiff_max) / (np.pi * 1 / m)

        # Временной массив для расчета смещения данных
        t = np.arange(0, len(matrix_name))
        t = t / 1920000

        # Смещение данных с учетом CFO
        data_offset = matrix_name * np.exp(-1j * 2 * np.pi * np.conjugate(CFO) * t)

        return data_offset

    
    def final_rx(self, rx, num_slots = 1):
        maxi = self.corr_pss_time(rx)
        ic(maxi)
        rx = rx[maxi:maxi + (self.N_fft + self.CP_len)*6 * num_slots]
        #rx = rx[maxi:maxi + (self.N_fft + self.CP_len)*6 * num_slots]
        rx_synс = self.indiv_symbols(rx)
        #ic(self.pilot_carriers)
        #ml.cool_plot(np.ravel(rx_synс))
        fft_rx_inter = self.interpol_pilots(rx_synс)
        self.interpol_pilots_test(rx_synс)
        fft_rx_del_pilots = self.del_pilots(fft_rx_inter)
        
        return fft_rx_del_pilots