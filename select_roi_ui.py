import sys
import numpy as np
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

class ROI(QDialog):
    got_roi = pyqtSignal(str)
    def __init__(self, parent=None):
        super(ROI, self).__init__(parent)
        self.title = 'Select ROI'
        self.left = 50
        self.top = 50
        # self.width = 400
        # self.height = 300
        self.initUI()

    def initUI(self):
        self.setWindowTitle(self.title)
        # self.setGeometry(self.left, self.top, self.width, self.height)
        self.lblTL = QLabel(self)
        self.lblTR = QLabel(self)
        self.lblBL = QLabel(self)
        self.lblBR = QLabel(self)
        self.lblTL.setText("Top-Left:")
        self.lblTR.setText("Top-Right:")
        self.lblBL.setText("Bottom-Left:")
        self.lblBR.setText("Bottom-Right:")

        self.txtTopLeft = QLineEdit(self)
        self.txtTopLeft.setText('473, 203')
        self.txtTopRight = QLineEdit(self)
        self.txtTopRight.setText('643, 200')
        self.txtBottomRight = QLineEdit(self)
        self.txtBottomRight.setText('850, 500')
        self.txtBottomLeft = QLineEdit(self)
        self.txtBottomLeft.setText('35, 500')

        self.applybutton = QPushButton("Apply", self)
        self.button = QPushButton("OK", self)

        self.layout = QGridLayout()
        self.layout.addWidget(self.lblTL, 0, 0)
        self.layout.addWidget(self.lblTR, 0, 1)
        self.layout.addWidget(self.txtTopLeft, 1, 0)
        self.layout.addWidget(self.txtTopRight, 1, 1)

        self.layout.addWidget(self.lblBL, 2, 0)
        self.layout.addWidget(self.lblBR, 2, 1)
        self.layout.addWidget(self.txtBottomLeft, 3, 0)
        self.layout.addWidget(self.txtBottomRight, 3, 1)

        self.layout.addWidget(self.applybutton, 4, 0)
        self.layout.addWidget(self.button, 4, 1)
        self.button.clicked.connect(self.on_click)
        self.applybutton.clicked.connect(self.send_apply_clicked)

        self.setLayout(self.layout)

    def send_apply_clicked(self):
        self.got_roi.emit('{}; {}; {}; {}'.format(
            self.txtTopLeft.text(), self.txtTopRight.text(), 
        self.txtBottomRight.text(), self.txtBottomLeft.text()))

    def on_click(self):
        self.close()