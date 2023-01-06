from kolejki import *
from pasazer import Pasazer
from miejsca import Miejsca
from scipy.stats import poisson
import random


# mozliwe stany w których jest pasazer
stoi = "stoi"
# czeka na swoje miejsce, pakuje sie itp
siada = "siada"
# juz siedzi
siedzi = "siedzi"
chodzi = "chodzi"

# zmiana w czasie (krok symulacji)
delta_t = 1

prob = poisson.pmf(k=1, mu=0.00017)

def zdarzyl_sie_wypadek():
    # TODO: do konsultacji
    """
    Funckja decydująca o wypadku dla danego pasażera w danym czasie
    : returns bool :
    """
    return prob >= random.random()

def zapelnij_kolejke(ilosc, chod_sr, wstw_sr, strategia):
    """
    Funkcja zapełeniająca kolejkę według zadanej strategii przydzielania 
    miejsc.
    :param int chod_sr: Średnia prędkość chodu pasażera w metrach na sekundę
    :param int wstw_sr: Średni czas wstawania pasażera w sekundach
    :param float pozycja: Pozycja podana jako dystans od początku samolotu
    :param function strategia: Wybrana strategia ustawiania pasażerów
    """
    id_start = 0
    kolejka = strategia(ilosc, chod_sr, wstw_sr)
    for pasazer in kolejka:
        # Dodajemy dwa typy id (patrz klasa Pasazer):
        # id
        # const_id
        pasazer.id = id_start
        pasazer.const_id = id_start
        id_start += 1
    return kolejka

def cz_wszyscy_siedza(kolejka: list[Pasazer]) -> bool:
    """
    Funkcja sprawdzająca czy wszyscy pasażerowie w samolocie siedzą.
    Warunek zatrzymania symulacji.
    : param list[Pasazer] kolejka: Kolejka Pasażerow
    : return bool: Zwraca wartość mówiącą czy wszyscy pasażerowie siedzą
    """
    for pasazer in kolejka:
        if pasazer._stan != siedzi:
            return False
    return True

def korytarz(kolejka_in: list[Pasazer]):
    """
    Funkcja odpowiedzialna za uruchomienie symulacji.
    : param list[Pasazer] kolejka: Kolejka Pasażerow
    : returns time_pass float: Czas posadzenia wszystkich pasażerów na ich miejscach
    """
    kolejka = kolejka_in.copy()
    # inicjacja rzędu
    rzedy = Miejsca()
    # inicjacja początu czasu
    time_pass = 0

    # liczy ilosc powtórzeń pętli while nie zależnie od delta_t
    # zmienna służyła jedynie do ustawiania breakpointów warunkowych
    # loop = 0

    # główna pętla symulacji, sprawdzająca warunek zatrzymania symulacji
    while not cz_wszyscy_siedza(kolejka):
        # loop += 1
        for pasazer in kolejka:
            if zdarzyl_sie_wypadek():
                # losujemy czy wydarzył się wypadek
                # print("Paszer stoi z powodou wypadku")
                pasazer.stan = stoi
                pasazer.czas_zakonczenia_akcji = time_pass + 30.0

            if pasazer.id != kolejka[-1].id: 
                if pasazer.stan == siada and pasazer.czas_zakonczenia_akcji <= time_pass \
                    and pasazer.czas_zakonczenia_akcji != 0:
                    # usadzamy pasazera kiedy skonczy siadać
                    pasazer.stan  = siedzi
                    temp = pasazer.id
                    # pasazer.id = -1
                    kolejka.pop(pasazer.const_id)
                    for _ in range(len(kolejka)):
                        kolejka[_].const_id = _
                    # pasazer.id = None
                    # if temp != None:
                    #     kolejka[temp+1].id = temp

            # obsługa ostatniego pasażera kiedy skonczy siadać
            if kolejka[-1].stan == siada and kolejka[-1].czas_zakonczenia_akcji <= time_pass \
                and kolejka[-1].czas_zakonczenia_akcji != 0:
                kolejka[-1].stan = siedzi

            # aktualizacja pozycji pasazera co krok symulacji
            pasazer.pozycja += delta_t*pasazer.chod_aktualna*(-1)
            pasazer.pozycja_od_rzedu += delta_t*pasazer.chod_aktualna*(-1)

            if pasazer.stan == stoi and pasazer.czas_zakonczenia_akcji <= time_pass \
                and pasazer.czas_zakonczenia_akcji != 0:
                # pasazer wraca do chodzenia kiedy skonczy sie akcja np. wypadek
                pasazer.stan  = chodzi
                pasazer.chod_aktualna = pasazer.chod_pr

            if pasazer.pozycja_od_rzedu <= 0 and pasazer.stan == chodzi:
                # pasazer zaczyna siadac
                pasazer.chod_aktualna = 0
                pasazer.stan = siada
                pasazer.czas_zakonczenia_akcji = rzedy.sit_at(pasazer) + time_pass

            # omijamy overflow error
            if pasazer.const_id != kolejka[-1].const_id:
                        if pasazer.const_id < kolejka[pasazer.const_id+1].id and (pasazer.stan == stoi or pasazer.stan == siada) and 0.2 > (pasazer.pozycja - kolejka[pasazer.const_id+1].pozycja):
                            # pasazer stoi jesli pasazer przed nim stoi
                            # print("Stoi pasazer dziedziczny")
                            kolejka[pasazer.const_id+1].stan = stoi
                            kolejka[pasazer.const_id+1].czas_zakonczenia_akcji = pasazer.czas_zakonczenia_akcji
                            kolejka[pasazer.const_id+1].chod_aktualna = pasazer.chod_aktualna
        time_pass += delta_t
    return time_pass


if __name__ == "__main__":
    # TEST
    kolejka = zapelnij_kolejke(150, 1.1, 6, Pulse)
    temp = korytarz(kolejka)
    print(temp)
    print(f'{temp/(60*delta_t)} minut')
