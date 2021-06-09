import sys, sqlite3, os, json
import PyQt5
from geneticAlgorithm import *
from PyQt5.QtWidgets import *
from PyQt5 import uic
from PyQt5 import QtCore
from PyQt5 import QtGui
from PyQt5.QtCore import QCoreApplication
from PyQt5.QtGui import *

def jsonLoader(windowName):
    reader = open("ui/styleSheet.json",'r')
    window = json.loads(''.join(reader.readlines()))[windowName]
    for i in window.keys() : window[i] = ''.join(window[i])
    return window

def loadStyle(self,screenName):
    design = jsonLoader(screenName)
    elements = self.__dict__
    for i in elements.keys():
        if i in design:self.__dict__[i].setStyleSheet(design[i])

mainScreen = uic.loadUiType("ui/main.ui")[0]
settingName = 'default'

class MainClass(QMainWindow, mainScreen):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        loadStyle(self,"main")
        self.displayMenu.addItem('생태계 모방')
        self.load.clicked.connect(self.openLoad)
    
    def openLoad(self):
        LoadClass(self)
                
class LoadClass(QDialog):
    def __init__(self,parent):
        super(LoadClass,self).__init__(parent)
        uic.loadUi("ui/option_1.ui", self)
        loadStyle(self,"option_1")
        self.show()
        self.ok.clicked.connect(self.open)
    def open(self):
        if self.attack.isChecked():
            Option_21Class(self)
        else:
            Option_22Class(self)

class Option_21Class(QDialog):
    def __init__(self,parent):
        super(Option_21Class,self).__init__(parent)
        uic.loadUi("ui/option_21.ui", self)
        loadStyle(self,"option_21")
        self.show()
        self.ok.clicked.connect(self.openSimulation)
    def openSimulation(self):
        SimulationClass(self)

class Option_22Class(QDialog):
    def __init__(self,parent):
        super(Option_22Class,self).__init__(parent)
        uic.loadUi("ui/option_22.ui", self)
        loadStyle(self,"option_22")
        self.show()
        self.ok.clicked.connect(self.openSimulation)
    def openSimulation(self):
        SimulationClass(self)

class SimulationClass(QDialog):
    def __init__(self,parent):
        super(SimulationClass,self).__init__(parent)
        uic.loadUi("ui/simulation.ui", self)
        loadStyle(self,"simulation")
        self.show()

if __name__ == "__main__":
    app = QApplication(sys.argv) 
    app.setStyle('Fusion')

    myWindow = MainClass() 

    myWindow.show()

    app.exec_()