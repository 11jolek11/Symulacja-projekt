import numpy as np
from pasazer import Pasazer

class Miejsca:
    """
    Klasa odpowiedzialna za zdarzenia związane z rzędami w samolocie.

    :ivar seats: Macierz opisująa ułożenie miejsc w samolocie
    :type seats: np.array
    """

    def __init__(self) -> None:
        """Inicjalizacja klasy"""
        self.seats: np.array = np.array([[[None, None, None], [None, None, None]] for _ in range(150 // 6)])

    """
    def get_row(self, seat: int) -> np.array:
        row_num = (seat - 1) // 6 + 1  # numer rzędu
        seat = (seat - 1) % 6 + 1  # numer miejsca w rzędzie
        print(seat)
        position = (seat - 1) // 3
        print(position)
        row: np.ndarray = self.seats[row_num - 1][position]
        row = row if seat <= 3 else row[::-1]
        return row
    """

    @staticmethod
    def get_seat_idx(seat: int) -> tuple:
        """
        metoda zwracająca index z macierz miejsc na której znajduje się podane miejsce.
        miejsca zaczynają się od 1.
        :param seat: numer miejsca
        :return: index w macierzy na któym znajduje się podany numer miejsca [0-150]
        """
        row_num = (seat - 1) // 6 + 1  # numer rzędu
        seat = (seat - 1) % 6 + 1  # numer miejsca w rzędzie
        position = (seat - 1) // 3
        return row_num - 1, position, (seat - 1) % 3

    def sit_at(self, passenger:Pasazer) -> float:
        # TODO: Zmien tak aby pasazer siadal na swoim miejscu
        """
        Metoda odpowiedzialna za zajęcie miejsca przez pasażera
        :param passenger: instancja pasażera, który ma zająć miejsce
        :return: czas w jakim pasażer stoi na korytarzu
        """
        seat = passenger.miejsce
        action_time = 0
        row_num, position, seat_idx = self.get_seat_idx(seat)
        row: np.ndarray = self.seats[row_num][position]
        row = row if seat > 3 else row[::-1]  # odwrócenie miejsc jeżeli są po lewej stronie
        times = []
        for idx in range(seat_idx):
            _passenger = row[idx]
            if _passenger:
                # ??? bez odległości instant
                # z odległościami można analitycznie zrobić po wylosowaniu czasu
                # time = max (wstawanie pasażera który siedział+siadanie pasażera który siedział)
                times.append(_passenger.wstw_cz + _passenger.siad_cz)

        times.append(passenger.rozp_cz)
        self.seats[row_num][position][seat_idx] = passenger
        action_time = max(times)
        return action_time

    def __str__(self) -> str:
        return str(self.seats)
