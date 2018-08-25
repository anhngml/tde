import sys
import time

from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

from tde import TDE

class TDEFormWidget(QWidget):
    def __init__(self, parent):
        super(TDEFormWidget, self).__init__(parent)
        self.tde = None
        self.th = Thread(self)
        self.layout = QGridLayout()

        self.label = QLabel(self)
        self.label.setAlignment(Qt.AlignCenter)
        # pixmap = QPixmap('0.jpg')
        # self.label.setPixmap(pixmap)

        self.layout.addWidget(self.label, 0, 0)

        self.pbar = QProgressBar(self)
        self.pbar.height = 45
        self.layout.addWidget(self.pbar, 1, 0)

        self.setDensityVal(0)
        self.setLayout(self.layout)

    def startTracking(self, stream_url='data/vlc-output_19.mp4'):
        if self.th is not None:
            self.th.stop()
        self.tde = TDE(stream_name=stream_url)
        self.th = Thread(self.tde, self)
        self.th.changePixmap.connect(self.label.setPixmap)
        self.th.changeLabel.connect(self.setDensityVal)
        self.th.start()

    def setDensityVal(self, val):
        # val = 80
        color = 'green'
        if 50 <= val <= 75:
            color = 'yellow'
        elif val > 75:
            color = 'red'
        self.pbar.setStyleSheet("QProgressBar {color: black; text-align: center;} QProgressBar::chunk {background-color: " + color + "; }")
        self.pbar.setValue(val)

    def closeEvent(self, event):
        self.th.stop()
        QWidget.closeEvent(self, event)

class Thread(QThread):
    changePixmap = pyqtSignal(QPixmap)
    changeLabel = pyqtSignal(int)

    def __init__(self, tde, parent=None):
        QThread.__init__(self, parent=parent)
        self.isRunning = True
        # self.stream_url = stream_url
        self.tde = tde

    def run(self):
        # self.tde = TDE(stream_name=self.stream_url)
        while self.isRunning:
            img, density = self.tde.get_next_frame()
            image = QImage(img, img.shape[1],\
                            img.shape[0], img.shape[1] * 3, QImage.Format_RGB888)
            pixmap = QPixmap(image)
            self.changePixmap.emit(pixmap)
            self.changeLabel.emit(density)
            
        # cap = cv2.VideoCapture(0)
        # while self.isRunning:
        #     ret, frame = cap.read()
        #     rgbImage = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        #     convertToQtFormat = QImage(rgbImage.data, rgbImage.shape[1], rgbImage.shape[0], QImage.Format_RGB888)
        #     convertToQtFormat = QPixmap.fromImage(convertToQtFormat)
        #     p = convertToQtFormat.scaled(640, 480, Qt.KeepAspectRatio)
        #     self.changePixmap.emit(p)
        #     now = datetime.datetime.now()
        #     sec = now.second
        #     self.changeLabel.emit(str(sec))

    def stop(self):
        self.isRunning = False
        self.quit()
        self.wait()