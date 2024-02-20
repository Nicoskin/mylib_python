from ..sdr import *

def check_hack(ip = "ip:192.168.3.1"):
    """
    Проверяет была ли SDR "взломана"
    """
    try:
        sdr = sdr_settings(ip, frequency=75e6)
        print("SDR была взломана ❤")
    except:
        print("НЕ ВЗЛОМАНО")
        print("ssh root@192.168.2.1 | analog | fw_setenv attr_name compatible | fw_setenv attr_val ad9364 | reboot")
        print("  ssh-keygen -f “/home/plutosdr/.ssh/known_hosts” -R “192.168.2.1”   ")
              
def fast_qpsk(ip: str = "ip:192.168.3.1", text: int = 100, num_cycles: int = 1):
    """
    Передаёт 100 бит и получает 1000 сэмплов (возвращает их)
    """
    
    from ..base import str_to_bits, gen_rand_bits
    from ..modulation import qpsk, qam16
    from numpy import repeat
    
    sdr = sdr_settings(ip)
    bits = gen_rand_bits(text)
    modem = qpsk(bits)
    signal = repeat(modem, 10)

    tx_sig(sdr, signal)
    rx = rx_cycles_buffer(sdr, num_cycles)

    sdr.tx_destroy_buffer()
    
    return rx
