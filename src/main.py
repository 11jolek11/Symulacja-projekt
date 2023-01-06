import sys
import time

from PySide6.QtCore import Qt, QObject, Signal, Slot, QThread
from PySide6.QtWidgets import QApplication, QMainWindow, QStyleOption, QStyle
from PySide6.QtGui import QPaintEvent, QPainter, QPen, QBrush

from kolejki import *  # type: ignore
from pasazer import Pasazer

from scipy.stats import poisson
from random import random


def zdarzyl_sie_wypadek(prob):
    """
    Funckja decydująca o wypadku dla danego pasażera w danym czasie
    : returns bool :
    """
    return prob >= random()

class Worker(QObject):
    data = Signal(list)

    def __init__(self, dt: float = 0.5, interval: float = 0.005, strategy=Fifo) -> None:
        super(Worker, self).__init__()
        self.dt = dt
        self.interval = interval
        self.strategy = strategy

    def simulate(self) -> None:
        prob = poisson.pmf(k=1, mu=0.00017)

        time_elapsed = 0
        passengers: list[Pasazer] = self.strategy(150, 1, 6, prob)
        # np.random.shuffle(Pasazer.passengers)
        # print(passengers)
        while passengers:
            time_elapsed += self.dt  # jezeli tutaj to reakcja pasazerow jest instant
            # jezli w for loop to pasazer ma swoj czas reakcji
            time.sleep(self.interval)
            x_positions = []
            for passenger in passengers:
                if zdarzyl_sie_wypadek(prob):
                    passenger.stan = 'stoi'
                    passenger.czas_akcji += 30
                passenger.move(self.dt)
                if passenger.stan == "siedzi":
                    passengers.remove(passenger)
                x_positions.append([passenger.x_pos, 0])
            self.data.emit(passengers)
            # print(time_elapsed)
        self.data.emit(passengers)
        return time_elapsed


class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        # Create the circle widget and add it to the layout
        global app
        self.dt = 0.5
        # size = app.primaryScreen().size() * 0.6
        self.resize(600, 400)
        self.setMinimumSize(600, 338)
        self.x_positions = []
        # symulacja
        self.thread = QThread()
        self.worker = Worker(0.5, 0.01, strategy=Fifo)
        self.worker.data.connect(self.update_positions)
        self.worker.moveToThread(self.thread)
        self.thread.started.connect(self.worker.simulate)  # type: ignore
        self.thread.finished.connect(self.thread.deleteLater)  # type: ignore
        self.thread.start()
        # self.setCentralWidget(self.circle_widget)

    @Slot(list)
    def update_positions(self, data: list):
        """Slot na odbieranie pozycji z wątku"""
        # print('received')
        self.x_positions = data
        self.update()

    def paintEvent(self, event: QPaintEvent) -> None:
        """Re-implement paintEvent method"""
        # print('u')
        width, height = self.size().width(), self.size().height()
        opt = QStyleOption()
        opt.initFrom(self)
        painter = QPainter(self)
        self.style().drawPrimitive(QStyle.PrimitiveElement.PE_Widget, opt, painter, self)
        multiplier = 20
        shift = 5
        for passenger in self.x_positions:
            if passenger.stan == 'temp':
                painter.setPen(QPen(Qt.green, 4, Qt.SolidLine))
                painter.setBrush(QBrush(Qt.green, Qt.SolidPattern))
            else:
                painter.setPen(QPen(Qt.red, 4, Qt.SolidLine))
                painter.setBrush(QBrush(Qt.red, Qt.SolidPattern))
            x_pos = passenger.x_pos
            # 30m = width
            # # max x_pos = 30
            #
            # 0.1m = 1 px, 1m = 10px
            x_pos = multiplier * x_pos
            # print(x_pos)
            if x_pos < 0:
                y_pos = height * 0.5 - abs(x_pos)
                x_pos = shift * 0.5
                # print(y_pos)
            else:
                y_pos = height * 0.5

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
    test = Worker(0.5, 0.005, Pulse)
    test.simulate()
    # app = QApplication(sys.argv)
    # window = MainWindow()
    # window.show()
    # sys.exit(app.exec())
