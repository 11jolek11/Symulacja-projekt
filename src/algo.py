from kolejki import *
from pasazer import Pasazer
from miejsca import Miejsca


stoi = "stoi"
siada = "siada"
siedzi = "siedzi"
chodzi = "chodzi"
delta_t = 1

# def dyst_do_rzedu(nr_siedzenia, siedzen_w_rzedzie=6):
#     """
#     Funkcja obliczająca odległość rzędu dla danego miejsca od wejścia
#     do samolotu.
#     """
#     a = 0.3
#     b = 0.5

#     nr_rzedu = (nr_siedzenia//siedzen_w_rzedzie) + 1
#     return nr_rzedu*(a+b)

def zapelnij_kolejke(ilosc, chod_sr, wstw_sr, strategia):
    """
    Funkcja zapełeniająca kolejkę według zadanej strategii przydzielania 
    miejsc.
    """
    id_start = 0
    kolejka = strategia(ilosc, chod_sr, wstw_sr)
    for pasazer in kolejka:
        pasazer.id = id_start
        pasazer.const_id = id_start
        id_start += 1
    return kolejka

def cz_wszyscy_siedza(kolejka: list[Pasazer]) -> bool:
    """
    Funkcja sprawdzająca czy wszyscy pasażerowie w samolocie siedzą.
    Warunek stopu symulacji.
    """
    # miejsca = []
    # for pasazer in kolejka:
    #     if pasazer._stan == siedzi:
    #         miejsca.append(True)
    # if all(miejsca):
    #     return True
    # else:
    #     return False

    for pasazer in kolejka:
        if pasazer._stan != siedzi:
            return False
    return True


def korytarz(kolejka_in: list[Pasazer]):
    kolejka = kolejka_in.copy()
    a = 0.3
    b = 0.5

    rzedy = Miejsca()

    time_pass = 0

    loop = 0

    while not cz_wszyscy_siedza(kolejka):
        # print(cz_wszyscy_siedza(kolejka))
        loop += 1
        for pasazer in kolejka:
            pasazer.pozycja += delta_t*pasazer.chod_aktualna*(-1)
            pasazer.pozycja_od_rzedu += delta_t*pasazer.chod_aktualna*(-1)

            if pasazer.id != kolejka[-1].id: 
                if pasazer.stan == siada and pasazer.czas_zakonczenia_akcji <= time_pass \
                    and pasazer.czas_zakonczenia_akcji != 0:
                    pasazer.stan  = siedzi
                    # print("Siedzi - " + str(pasazer.const_id))
                    temp = pasazer.id
                    pasazer.id = -1
                    kolejka[temp+1].id = temp

            # obsługa ostatniego pasażera
            if kolejka[-1].stan == siada and kolejka[-1].czas_zakonczenia_akcji <= time_pass \
                and kolejka[-1].czas_zakonczenia_akcji != 0:
                kolejka[-1].stan = siedzi

            if pasazer.stan == stoi and pasazer.czas_zakonczenia_akcji <= time_pass \
                and pasazer.czas_zakonczenia_akcji != 0:
                pasazer.stan  = chodzi
                pasazer.chod_aktualna = pasazer.chod_pr

            if pasazer.pozycja_od_rzedu <= 0 and pasazer.stan == chodzi:
                pasazer.chod_aktualna = 0
                pasazer.stan = siada
                pasazer.czas_zakonczenia_akcji = rzedy.sit_at(pasazer) + time_pass

            if pasazer.id != kolejka[-1].id:
                if pasazer.id < kolejka[pasazer.id+1].id and (pasazer.stan == stoi or pasazer.stan == siada):
                    kolejka[pasazer.id+1].stan = stoi
                    kolejka[pasazer.id+1].czas_zakonczenia_akcji = pasazer.czas_zakonczenia_akcji
                    kolejka[pasazer.id+1].chod_aktualna = pasazer.chod_aktualna
            # if pasazer.stan ==5 or pasazer.const_id == 6:
            #     print(f"{pasazer.pozycja_od_rzedu}<>>>>>>>>>>>{pasazer.const_id}>>>>{pasazer.stan}>>>{pasazer.chod_aktualna}")
            # TODO: implementacja wypadkow
        # FIXME: ostatni pasażer zawsze jest w stanie "siada"
        time_pass += delta_t





















    return time_pass






















if __name__ == "__main__":

    kolejka = zapelnij_kolejke(150, 9, 6, Fifo)
    # print(cz_wszyscy_siedza(kolejka))
    temp = korytarz(kolejka)
    print(temp)
    print(f'{temp/(60*delta_t)} minut')