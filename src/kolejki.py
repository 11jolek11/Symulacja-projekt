from pasazer import Pasazer
from numpy import arange
from numpy.random import shuffle
from random import uniform

const_miejsca = 150
# 
const_dystans = 70.0

def Fifo(ilosc, chod_sr, wstw_sr):
    """
    Kolejka FIFO zwracająca tablicę z pasażerami o wielkości ilosc
    :param int ilosc: Ilość pasażerów
    :param int chod_sr: Średnia prędkość chodu pasażera w metrach na sekundę
    :param int wstw_sr: Średni czas wstawania pasażera w sekundach
    :return: Tablica pasażerów
    :rtype: list
    """
    global const_miejsca, const_dystans
    miejsca = arange(1, const_miejsca + 1, 1, dtype=int)
    shuffle(miejsca)
    pasazerowie = []
    dystans = const_dystans

    for i in range(ilosc):
        odstep = uniform(0.3, 0.8)

        if i==0:
            dystans += odstep
            pasazerowie.append(Pasazer(chod_sr, wstw_sr, dystans, miejsca[i]))
        # dystans += odstep
        dystans = 0
        dystans += pasazerowie[-1].pozycja + odstep
        pasazerowie.append(Pasazer(chod_sr, wstw_sr, dystans, miejsca[i]))
    return pasazerowie

def PlaceFirst(ilosc, chod_sr, wstw_sr):
    """
    Kolejka zwracająca tablicę z pasażerami o wielkości ilosc w kolejności miejsca zajętego w samolocie
    :param int ilosc: Ilość pasażerów
    :param int chod_sr: Średnia prędkość chodu pasażera w metrach na sekundę
    :param int wstw_sr: Średni czas wstawania pasażera w sekundach
    :return: Tablica pasażerów
    :rtype: list
    """
    global const_dystans, const_miejsca
    miejsca = arange(1, const_miejsca + 1, 1, dtype=int)
    shuffle(miejsca)
    miejsca = sorted(miejsca[:ilosc])
    pasazerowie = []
    dystans = const_dystans

    for i in range(ilosc):
        odstep = uniform(0.3, 0.8)
        # dystans += odstep
        if i==0:
            dystans += odstep
            pasazerowie.append(Pasazer(chod_sr, wstw_sr, dystans, miejsca[i]))
        dystans = 0
        dystans += pasazerowie[-1].pozycja + odstep
        pasazerowie.append(Pasazer(chod_sr, wstw_sr, dystans, miejsca[i]))
    return pasazerowie

def WindowFirst(ilosc, chod_sr, wstw_sr):
    """
    Kolejka zwracająca tablicę z pasażerami o wielkości ilosc w kolejności miejsc od okna
    :param int ilosc: Ilość pasażerów
    :param int chod_sr: Średnia prędkość chodu pasażera w metrach na sekundę
    :param int wstw_sr: Średni czas wstawania pasażera w sekundach
    :return: Tablica pasażerów
    :rtype: list
    """
    global const_miejsca, const_dystans
    miejsca = arange(1, const_miejsca + 1, 1, dtype=int)
    shuffle(miejsca)
    miejsca = miejsca[:ilosc]
    pasazerowie = []
    dystans = const_dystans

    m1, m2, m3 = [], [], []
    for m in miejsca:
        if m % 6 == 0 or m % 6 == 1: m1.append(m)
        elif m % 6 == 2 or m % 6 == 5: m2.append(m)
        else: m3.append(m)
    sortowane_miejsca = [*m1, *m2, *m3]

    for i in range(ilosc):
        odstep = uniform(0.3, 0.8)
        # dystans += odstep
        if i==0:
            dystans += odstep
            pasazerowie.append(Pasazer(chod_sr, wstw_sr, dystans, miejsca[i]))
        dystans = 0
        dystans += pasazerowie[-1].pozycja + odstep
        pasazerowie.append(Pasazer(chod_sr, wstw_sr, dystans, sortowane_miejsca[i]))
    return pasazerowie

def RowFirst(ilosc, chod_sr, wstw_sr):
    """
    Kolejka zwracająca tablicę z pasażerami o wielkości ilosc w kolejności rzędu
    :param int ilosc: Ilość pasażerów
    :param int chod_sr: Średnia prędkość chodu pasażera w metrach na sekundę
    :param int wstw_sr: Średni czas wstawania pasażera w sekundach
    :return: Tablica pasażerów
    :rtype: list
    """
    global const_miejsca, const_dystans
    miejsca = arange(1, const_miejsca + 1, 1, dtype=int)
    shuffle(miejsca)
    miejsca = miejsca[:ilosc]
    pasazerowie = []
    dystans = const_dystans

    m_temp, sortowane_miejsca = [ [] for i in range(25)], []
    for m in miejsca: m_temp[(m-1)//6].append(m)
    for i in m_temp: sortowane_miejsca.extend(i)

    for i in range(ilosc):
        odstep = uniform(0.3, 0.8)
        # dystans += odstep
        if i==0:
            dystans += odstep
            pasazerowie.append(Pasazer(chod_sr, wstw_sr, dystans, miejsca[i]))
        dystans = 0
        dystans += pasazerowie[-1].pozycja + odstep
        pasazerowie.append(Pasazer(chod_sr, wstw_sr, dystans, sortowane_miejsca[i]))
    return pasazerowie

def BestFirst(ilosc, chod_sr, wstw_sr):
    """
    Kolejka zwracająca tablicę z pasażerami o wielkości ilosc w kolejności rzędu i miejsca od okna
    :param int ilosc: Ilość pasażerów
    :param int chod_sr: Średnia prędkość chodu pasażera w metrach na sekundę
    :param int wstw_sr: Średni czas wstawania pasażera w sekundach
    :return: Tablica pasażerów
    :rtype: list
    """
    global const_miejsca, const_dystans
    miejsca = arange(1, const_miejsca + 1, 1, dtype=int)
    shuffle(miejsca)
    miejsca = miejsca[:ilosc]
    pasazerowie = []
    dystans = const_dystans

    m_temp, sortowane_miejsca = [ [] for i in range(25)], []
    for m in miejsca: m_temp[(m-1)//6].append(m)
    for r in m_temp:
        r.sort(key=lambda x: abs((x % 6) - 3.5), reverse=True)
        sortowane_miejsca.extend(r)

    for i in range(ilosc):
        odstep = uniform(0.3, 0.8)
        # dystans += odstep
        if i==0:
            dystans += odstep
            pasazerowie.append(Pasazer(chod_sr, wstw_sr, dystans, miejsca[i]))
        dystans = 0
        dystans += pasazerowie[-1].pozycja + odstep
        pasazerowie.append(Pasazer(chod_sr, wstw_sr, dystans, sortowane_miejsca[i]))
    return pasazerowie

def Pulse(ilosc, chod_sr, wstw_sr):
    """
    Kolejka zwracająca tablicę z pasażerami o wielkości ilosc w kolejności rzędu i miejsca od okna
    :param int ilosc: Ilość pasażerów
    :param int chod_sr: Średnia prędkość chodu pasażera w metrach na sekundę
    :param int wstw_sr: Średni czas wstawania pasażera w sekundach
    :return: Tablica pasażerów
    :rtype: list
    """
    global const_miejsca, const_dystans
    miejsca = arange(1, const_miejsca + 1, 1, dtype=int)
    shuffle(miejsca)
    miejsca = miejsca[:ilosc]
    pasazerowie = []
    dystans = const_dystans

    m_temp, sortowane_miejsca = [[] for i in range(25)], []
    for m in miejsca: m_temp[(m - 1) // 6].append(m)
    temp_val = ilosc
    while temp_val:
        for i in range(25):
            if len(m_temp[i]):
                sortowane_miejsca.append(m_temp[i][0])
                m_temp[i].pop(0)
                temp_val -= 1

    for i in range(ilosc):
        odstep = uniform(0.3, 0.8)
        dystans += odstep
        pasazerowie.append(Pasazer(chod_sr, wstw_sr, dystans, sortowane_miejsca[i]))
    return pasazerowie

if __name__ == "__main__":
    temp = Fifo(150, 9, 6)