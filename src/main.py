import math
import sys
import time

from PySide6.QtCore import Qt, QObject, Signal, Slot, QThread
from PySide6.QtWidgets import QApplication, QMainWindow, QStyleOption, QStyle
from PySide6.QtGui import QPaintEvent, QPainter, QPen, QBrush
from kolejki import BestFirst, Fifo, PlaceFirst, WindowFirst, RowFirst, Pulse  # type: ignore
from pasazer import Pasazer
from miejsca import Miejsca


# from scipy.stats import poisson
# import random


class Worker(QObject):
    data = Signal(list)

    def __init__(self, dt: float = 0.5, interval: float = 0.005) -> None:
        super(Worker, self).__init__()
        self.dt = dt
        self.interval = interval

    def simulate(self):
        # pozycje = []
        # mozliwe stany w których jest pasazer
        stoi = "stoi"
        # czeka na swoje miejsce, pakuje sie itp
        siada = "siada"
        # juz siedzi
        siedzi = "siedzi"
        chodzi = "chodzi"

        # zmiana w czasie (krok symulacji)
        delta_t = self.dt

        # prob = poisson.pmf(k=1, mu=0.00017)

        def zdarzyl_sie_wypadek():
            # TODO: do konsultacji
            """
            Funckja decydująca o wypadku dla danego pasażera w danym czasie
            : returns bool :
            """
            return False

        def zapelnij_kolejke(ilosc, chod_sr, wstw_sr, strategia):
            """
            Funkcja zapełeniająca kolejkę według zadanej strategii przydzielania
            miejsc.
            :param int chod_sr: Średnia prędkość chodu pasażera w metrach na sekundę
            :param int wstw_sr: Średni czas wstawania pasażera w sekundach
            :param function strategia: Wybrana strategia ustawiania pasażerów
            :param int ilosc: Wybrana ilosc pasażerów
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
                if pasazer.stan != siedzi:
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
                pozycje = []
                for pasazer in kolejka:
                    if zdarzyl_sie_wypadek():
                        # losujemy czy wydarzył się wypadek
                        pasazer.stan = stoi
                        pasazer.czas_zakonczenia_akcji = time_pass + 30.0

                    if pasazer.id != kolejka[-1].id:
                        if pasazer.stan == siada and pasazer.czas_zakonczenia_akcji <= time_pass \
                                and pasazer.czas_zakonczenia_akcji != 0:
                            # usadzamy pasazera kiedy skonczy siadać
                            pasazer.stan = siedzi
                            temp = pasazer.id
                            pasazer.id = -1
                            kolejka[temp + 1].id = temp

                    # obsługa ostatniego pasażera kiedy skonczy siadać
                    if kolejka[-1].stan == siada and kolejka[-1].czas_zakonczenia_akcji <= time_pass \
                            and kolejka[-1].czas_zakonczenia_akcji != 0:
                        kolejka[-1].stan = siedzi

                    # aktualizacja pozycji pasazera co krok symulacji
                    pasazer.pozycja += delta_t * pasazer.chod_aktualna * (-1)
                    pasazer.pozycja_od_rzedu += delta_t * pasazer.chod_aktualna * (-1)

                    if pasazer.stan == stoi and pasazer.czas_zakonczenia_akcji <= time_pass \
                            and pasazer.czas_zakonczenia_akcji != 0:
                        # pasazer wraca do chodzenia kiedy skonczy sie akcja np. wypadek
                        pasazer.stan = chodzi
                        pasazer.chod_aktualna = pasazer.chod_pr
                    if pasazer.pozycja_od_rzedu <= 0 and (pasazer.stan == chodzi or pasazer.stan == stoi):
                        # pasazer zaczyna siadac
                        pasazer.chod_aktualna = 0
                        pasazer.stan = siada
                        pasazer.czas_zakonczenia_akcji = rzedy.sit_at(pasazer) + time_pass
                    if pasazer.stan == stoi:
                        print(pasazer.pozycja_od_rzedu)
                    # omijamy overflow error
                    try:
                        if pasazer.id != kolejka[-1].id:
                            if pasazer.id < kolejka[pasazer.id+1].id and (pasazer.stan == stoi or pasazer.stan == siada) and 0.2 > (pasazer.pozycja - kolejka[pasazer.id+1].pozycja):
                                # pasazer stoi jesli pasazer przed nim stoi
                                kolejka[pasazer.id+1].stan = stoi
                                kolejka[pasazer.id+1].czas_zakonczenia_akcji = pasazer.czas_zakonczenia_akcji
                                kolejka[pasazer.id+1].chod_aktualna = pasazer.chod_aktualna
                    except IndexError:
                        pass
                    pozycje.append(pasazer)
                    #
                    # print(pasazer.pozycja)
                    # print(pasazer.miejsce // 6)
                self.data.emit(pozycje)

                time_pass += delta_t
                # time.sleep(self.interval)
            return time_pass

        kolejka1 = zapelnij_kolejke(150, 9, 6, Fifo)
        _temp = korytarz(kolejka1)
        print(_temp)
        print(f'{_temp / (60 * delta_t)} minut')


class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        global app
        self.dt = 0.5
        # size = app.primaryScreen().size() * 0.6
        self.resize(600, 400)
        self.setMinimumSize(600, 338)
        self.x_positions: list[Pasazer] = []
        # symulacja
        self.thread = QThread()
        self.worker = Worker(0.5, 0.01)
        self.worker.data.connect(self.update_positions)
        self.worker.moveToThread(self.thread)
        self.thread.started.connect(self.worker.simulate)  # type: ignore
        self.thread.finished.connect(self.thread.deleteLater)  # type: ignore
        self.thread.start()
        # self.setCentralWidget(self.circle_widget)

    @Slot(list)
    def update_positions(self, data: list[Pasazer]):
        """Slot na odbieranie pozycji z wątku"""
        # print('received')
        self.x_positions: list[Pasazer] = data
        self.update()

    def paintEvent(self, event: QPaintEvent) -> None:
        """Re-implement paintEvent method"""
        # print('u')
        width, height = self.size().width(), self.size().height()
        opt = QStyleOption()
        opt.initFrom(self)
        painter = QPainter(self)
        self.style().drawPrimitive(QStyle.PrimitiveElement.PE_Widget, opt, painter, self)
        multiplier = 10
        shift = 5
        for passenger in self.x_positions:
            if passenger.stan == 'siedzi':
                continue
            if passenger.stan == 'chodzi':
                painter.setPen(QPen(Qt.green, 4, Qt.SolidLine))
                painter.setBrush(QBrush(Qt.green, Qt.SolidPattern))
            elif passenger.stan == 'stoi':
                painter.setPen(QPen(Qt.blue, 4, Qt.SolidLine))
                painter.setBrush(QBrush(Qt.blue, Qt.SolidPattern))
            else:
                # print(passenger.stan)
                painter.setPen(QPen(Qt.red, 4, Qt.SolidLine))
                painter.setBrush(QBrush(Qt.red, Qt.SolidPattern))

            x_pos = int(-1 * passenger.pozycja * multiplier)
            # x_pos = int(10 * x_pos)
            # print(x_pos)
            if x_pos < 0:
                y_pos = height * 0.5 - math.log(abs(x_pos))
                x_pos = shift * 0.5
                # print(y_pos)
            else:
                y_pos = height * 0.5
            # print(y_pos)

            painter.drawEllipse(x_pos, y_pos - 2, 4, 4)
        painter.setPen(QPen(Qt.black, 2, Qt.SolidLine))
        painter.setBrush(QBrush(Qt.black, Qt.SolidPattern))
        for i in range(25, 0, -1):
            seat_pos = 0.3 + i * 0.8
            position = int(seat_pos * multiplier + shift)
            painter.drawRect(position, height * 0.5 - 18, 3, 10)
            painter.drawRect(position, height * 0.5 + 10, 3, 10)
        painter.end()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
