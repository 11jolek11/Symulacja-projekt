from __future__ import annotations
from numpy.random import normal
from miejsca import Miejsca


class Samolot:
    miejsca = Miejsca()


class Pasazer(Samolot):
    """
    Klasa pasażera
    :param int chod_sr: Średnia prędkość chodu pasażera w metrach na sekundę
    :param int wstw_sr: Średni czas wstawania pasażera w sekundach
    :param float pozycja: Pozycja podana jako dystans od początku samolotu
    :param int miejsce: Określa przydzielone miejsce w samolocie danego pasażera
    :ivar chod_pr: Prędkość danego pasażera określona z rozkładu normalnego (chod_sr, chod_od) w metrach na sekundę
    :ivar wstw_cz: Czas wstawania danego pasażera określona z rozkładu normalnego (wstw_sr, wstw_od) w sekunadch
    :ivar siad_cz: Czas siadania danego pasażera określona z rozkładu normalnego (siad_sr, siad_od) w sekunadch
    :ivar rozp_cz: Czas rozpakowywania się danego pasażera \
    określona z rozkładu normalnego (rozp_sr, rozp_od) w sekunadch
    :ivar stan: Określa aktualny stan danego pasażera
    :ivar czas_akcji: Parametr służący do okreslenia ile jeszcze czasu zajmie danemu pasażerowi określona w stanie akcja
    :type chod_pr: float
    :type wstw_cz: float
    :type siad_cz: float
    :type rozp_cz: float
    :type stan: basestring
    :type czas_akcji: float
    """
    passengers: list[Pasazer] = []

    def __init__(self, chod_sr, wstw_sr, pozycja, miejsce):
        """
        :param int chod_sr: Średnia prędkość chodu pasażera w metrach na sekundę
        :param int wstw_sr: Średni czas wstawania pasażera w sekundach
        :param float pozycja: Pozycja podana jako dystans od początku samolotu
        :param int miejsce: Określa przydzielone miejsce w samolocie danego pasażera
        """
        self.chod_sr = chod_sr
        self.chod_od = 0.3
        self.chod_pr = self.__whileNormal__(self.chod_sr, self.chod_od)

        self.wstw_sr = wstw_sr
        self.wstw_od = 2
        self.wstw_cz = self.__whileNormal__(self.wstw_sr, self.wstw_od)

        self.rozp_sr = 30
        self.rozp_od = 5
        self.rozp_cz = self.__whileNormal__(self.rozp_sr, self.rozp_od)

        self.siad_sr = 2
        self.siad_od = 1
        self.siad_cz = self.__whileNormal__(self.siad_sr, self.siad_od)

        self.pozycja = pozycja
        self.miejsce = miejsce
        self.stan = "temp"
        self.czas_akcji = 0

        # zmiany
        # x_pos - pozycja w korytarzu samolotu
        self.x_pos = -self.pozycja
        print(self.x_pos)
        self.seat_at = self.seat_pos(self.miejsce)  # x_pos na którym znajduje się miejsce pasażera

        self.passengers.append(self)
        self.idx = self.passengers.index(self)

    def move(self, dt):
        """
        Metoda odpowiedzialna za ruch pasażera
        """
        self.czas_akcji -= dt
        self.czas_akcji = max(self.czas_akcji, 0)
        if self.stan == 'siada':
            if self.czas_akcji <= 0:
                self.passengers.remove(self)
                self.stan = 'siedzi'
            return
        if self.can_sit() and self.stan != 'siada':
            self.sit()
            return

        if self.can_move(dt):
            self.x_pos += dt * self.chod_pr

    def can_sit(self) -> bool:
        return self.x_pos > self.seat_at

    def sit(self):
        self.czas_akcji = max(self.czas_akcji, 0)
        self.czas_akcji += self.miejsca.sit_at(self.miejsce, self)
        # self.x_pos = self.seat_at
        self.stan = 'siada'

    def can_move(self, dt) -> bool:
        # troche chiny, trzeba znalezc inny sposob
        if self.czas_akcji > 0:
            return False
        try:
            index = self.passengers.index(self)  # duzo czasu to zajmuje
            if index - 1 < 0:
                return self.czas_akcji <= 0 # True
            return self.passengers[index - 1].x_pos - (self.x_pos + dt * self.chod_pr) > 0.3
        except (IndexError, ValueError):
            return self.czas_akcji <= 0 # True

    def __str__(self):
        return f'{self.idx}: {self.miejsce} {self.stan}, {self.x_pos}, {self.seat_at}, {self.czas_akcji}'

    def __repr__(self):
        return f'{self.idx}: {self.miejsce} {self.stan}, {self.x_pos}, {self.seat_at}, {self.czas_akcji}\n'

    @staticmethod
    def seat_pos(num) -> int:
        return 0.3 + ((150 - num) // 6) * 0.8

    @staticmethod
    def __whileNormal__(srednia, odchylenie, zmienna=-1):
        while zmienna < 0:
            zmienna = normal(srednia, odchylenie)
        return zmienna
