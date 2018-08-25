import sys
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

class OpenStream(QDialog):
    def __init__(self, parent=None):
        super(OpenStream, self).__init__(parent)
        self.title = 'Open video stream'
        self.left = 10
        self.top = 10
        self.width = 300
        self.height = 140
        self.initUI()

    def initUI(self):
        self.setWindowTitle(self.title)
        # self.setGeometry(self.left, self.top, self.width, self.height)
        self.lblTL = QLabel(self)
        self.lblTL.setText("Stream url:")

        self.txtStreamUrl = QLineEdit(self)
        self.txtStreamUrl.setText('vlc-output_19.mp4')
        self.txtStreamUrl.resize(280,30)

        self.okbutton = QPushButton("OK", self)
        self.cancelbutton = QPushButton("Cancel", self)

        self.layout = QGridLayout()
        self.layout.addWidget(self.lblTL, 0, 0)
        self.layout.addWidget(self.txtStreamUrl, 1, 0, 1, 2)

        self.layout.addWidget(self.okbutton, 2, 0)
        self.layout.addWidget(self.cancelbutton, 2, 1)
        self.okbutton.clicked.connect(self.accept)
        self.cancelbutton.clicked.connect(self.reject)

        self.setLayout(self.layout)

    def on_click(self):
        self.close()