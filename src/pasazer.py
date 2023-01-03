from numpy.random import normal
class Pasazer:
    """
    Klasa pasażera
    :param int chod_sr: Średnia prędkość chodu pasażera w metrach na sekundę
    :param int wstw_sr: Średni czas wstawania pasażera w sekundach
    :param float pozycja: Pozycja podana jako dystans od początku samolotu
    :param int miejsce: Określa przydzielone miejsce w samolocie danego pasażera
    :ivar chod_pr: Prędkość danego pasażera określona z rozkładu normalnego (chod_sr, chod_od) w metrach na sekundę
    :ivar wstw_cz: Czas wstawania danego pasażera określona z rozkładu normalnego (wstw_sr, wstw_od) w sekunadch
    :ivar siad_cz: Czas siadania danego pasażera określona z rozkładu normalnego (siad_sr, siad_od) w sekunadch
    :ivar rozp_cz: Czas rozpakowywania się danego pasażera określona z rozkładu normalnego (rozp_sr, rozp_od) w sekunadch
    :ivar stan: Określa aktualny stan danego pasażera
    :ivar czas_akcji: Parametr służący do okreslenia ile jeszcze czasu zajmie danemu pasażerowi określona w stanie akcja
    :type chod_pr: float
    :type wstw_cz: float
    :type siad_cz: float
    :type rozp_cz: float
    :type stan: basestring
    :type czas_akcji: float
    """

    def __init__(self, chod_sr, wstw_sr, pozycja, miejsce):
        """
        :param int chod_sr: Średnia prędkość chodu pasażera w metrach na sekundę
        :param int wstw_sr: Średni czas wstawania pasażera w sekundach
        :param float pozycja: Pozycja podana jako dystans od początku samolotu
        :param int miejsce: Określa przydzielone miejsce w samolocie danego pasażera
        """
        # TODO: dodać oddziaływanie na warunki pogodowe
        self.id = 0
        self.const_id = 0
        self.chod_sr = chod_sr
        self.chod_od = 0.3
        self.chod_pr = self.__whileNormal__(self.chod_sr, self.chod_od)
        self.chod_aktualna = self.chod_pr

        self.wstw_sr = wstw_sr
        self.wstw_od = 2
        self.wstw_cz = self.__whileNormal__(self.wstw_sr, self.wstw_od)

        self.rozp_sr = 30
        self.rozp_od = 5
        self.rozp_cz = self.__whileNormal__(self.rozp_sr, self.rozp_od)

        self.siad_sr = 2
        self.siad_od = 1
        self.siad_cz = self.__whileNormal__(self.siad_sr, self.siad_od)

        # pozycj po wejściu do samolotu pozycja staje się ujemna
        self.pozycja = pozycja
        self.pozycja_od_rzedu = 0


        self._stan = "chodzi"

        self.miejsce = miejsce
        self.czas_akcji = 0
        # TODO: doc
        self.czas_zakonczenia_akcji = 0

        self.dyst_do_rzedu()

    # TODO: doc
    @property
    def stan(self):
        return self._stan

    @stan.setter
    def stan(self, new_stan):
        # print(f'Zmaiana stanu pasazera {self.const_id} na wartosc {new_stan}')
        self._stan = new_stan

    def __whileNormal__(self, srednia, odchylenie, zmienna=-1):
        while zmienna < 0:
            zmienna = normal(srednia, odchylenie)
        return zmienna

    def dyst_do_rzedu(self, siedzen_w_rzedzie=6):
        """
        Funkcja obliczająca odległość rzędu dla danego miejsca od wejścia
        do samolotu.
        """
        # TODO: przystosować do ułożeniam iejsc w samolocie
        a = 0.3
        b = 0.5

        nr_rzedu = (self.miejsce//siedzen_w_rzedzie) + 1
        # return 70-(nr_rzedu*(a+b)) + self.pozycja
        self.pozycja_od_rzedu = 70-(nr_rzedu*(a+b)) + self.pozycja
