import socket
import sys
from PyQt5.QtWidgets import QApplication, QWidget, QHBoxLayout, QLabel
from PyQt5.QtGui import QPalette, QColor
from PyQt5.QtCore import QObject, pyqtSignal
from threading import Thread
import config

class LedStripWidget(QWidget):
    labels = []

    def __init__(self, numLed):
        super().__init__()
        self.initUI(numLed)

    def initUI(self, numLed):
        self.numLed = numLed
        strip = QHBoxLayout()
        strip.setSpacing(0)
        for i in range(numLed):
            label = QLabel()
            pal = QPalette()
            pal.setColor(QPalette.Background, QColor(0, 0, 0))
            label.setAutoFillBackground(True)
            label.setPalette(pal)
            strip.addWidget(label)
            self.labels.append(label)
        self.setLayout(strip)

    def changeColors(self, colors):
        if (len(colors) == self.numLed):
            for i, color in enumerate(colors):
                pal = QPalette()
                pal.setColor(QPalette.Background, color)
                self.labels[i].setPalette(pal)
        else:
            print("Invalid number of Colors. Expected " + str(self.numLed) + ", got " + str(len(colors)))


class Networker(QObject):
    def __init__(self, port=4210, addr="127.0.0.1"):
        super().__init__()
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.bind((addr, port))

    dataArrived = pyqtSignal(list)

    def sim(self):
        while True:
            data, addr = self.sock.recvfrom(1024)
            colors = []
            length = 3
            for i in range(0, len(data), length):  # -2 to prevent buffer overread
                colors.append(QColor(data[i], data[i + 1], data[i + 2]))
            self.dataArrived.emit(colors)


if __name__ == '__main__':
    ndict = dict()
    ndict["port"] = 4210
    ndict["addr"] = "127.0.0.1"

    app = QApplication(sys.argv)

    w = LedStripWidget(config.LENGTH)
    w.resize(250, 50)
    w.move(300, 300)
    w.setWindowTitle('Simple')
    w.show()

    n = Networker(**ndict)
    n.dataArrived.connect(w.changeColors)

    t = Thread(target=n.sim)
    t.daemon = True
    t.start()

    app.exec()
