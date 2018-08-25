import sys
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

from select_roi_ui import ROI
from open_stream import OpenStream
from TDE_usercontrol import TDEFormWidget

from tde import TDE

class App(QMainWindow):
 
    def __init__(self):
        super().__init__()
        self.title = 'Traffic Density Estimation'
        self.left = 50
        self.top = 50
        self.width = 800
        self.height = 600
        self.initUI()
 
    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        self.form_widget = TDEFormWidget(self) 
        self.setCentralWidget(self.form_widget) 

        self.get_ROI = ROI(self)
        self.get_ROI.got_roi.connect(self.got_roi)

        menubar = self.menuBar()

        fileMenu = menubar.addMenu('File')
        openAct = QAction('Open', self) 
        openAct.triggered.connect(self.openStream)     
        fileMenu.addAction(openAct)

        impAct = QAction('Select ROI', self) 
        impAct.triggered.connect(self.selectRoi)     
        fileMenu.addAction(impAct)

        self.statusBar().showMessage('')

    def got_roi(self, the_roi):
        points = the_roi.split('; ')
        pts = []
        for point in points:
            cords = point.split(',')
            x = cords[0]
            y = cords[1]
            pts.append([int(x), int(y)])
        if self.form_widget.tde is not None:
            self.form_widget.tde.setROI(pts[0], pts[1], pts[2], pts[3])

    def selectRoi(self):
        self.get_ROI.show()

    def openStream(self):
        view = OpenStream(parent=self)
        if view.exec_():
            self.form_widget.startTracking(stream_url=view.txtStreamUrl.text())

    # def resizeEvent(self, event):
    #     QMainWindow.resizeEvent(self, event)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    ex.show()
    sys.exit(app.exec_())