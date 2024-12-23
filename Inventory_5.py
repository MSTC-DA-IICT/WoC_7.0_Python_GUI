from PyQt5.QtWidgets import QMainWindow,QPushButton,QLineEdit,QComboBox
import json
from PyQt5 import uic
import os

class Inventory_5UI(QMainWindow):
    def __init__(self,dark_mode,MainWindow):
        super(Inventory_5UI,self).__init__()

        # Load the UI
        uic.loadUi("Inventory_5.ui",self)

        # Load the widgets
        self.ExitWindow = self.findChild(QPushButton,"pushButton_2")
        self.SelectRawMaterial = self.findChild(QComboBox,"comboBox")
        self.MinimumWeight = self.findChild(QLineEdit,"lineEdit")
        self.SavingChange = self.findChild(QPushButton,"pushButton")
        self.mylocaladdress = os.getcwd()
        if (dark_mode==True):
            self.dark_style = """
            QMainWindow {
                background-color: #2d2d2d;
                color: #ffffff;
            }
            QPushButton {
                background-color: #5c5c5c;
                color: #ffffff;
                border: 1px solid #3c3c3c;
            }
            QPushButton::hover{
                background-color: #6c6c6c;
            }
            QLabel {
                color: #ffffff;
            }
            QTextEdit {
                background-color: #3c3c3c;
                color: #ffffff;
            }
            QComboBox {
                background-color: #3c3c3c;
                color: #ffffff;
                border: 1px solid #5c5c5c;
            }
            QComboBox QAbstractItemView {
                background-color: #3c3c3c;
                color: #ffffff;
                border: 1px solid #5c5c5c;
            }
            QComboBox::drop_down {
                background-color: #3c3c3c;
                border: 1px solid #5c5c5c;
            }
            QListWidget {
                background-color: #3c3c3c;
                color: #ffffff;
                border: 1px solid #5c5c5c;
            }
            QCheckBox {
                color: #ffffff;
            }
            QCheckBox::indicator:checked {
                background-color: #5c5c5c;
                border: 1px solid #3c3c3c;
            }
            QCheckBox::indicator {
                width: 18px;
                height: 18px;
                border: 1px solid #5c5c5c;
                background-color: #3c3c3c;
            }
            QSpinBox {
                background-color: #3c3c3c;
                color: #ffffff;
                border: 1px solid #5c5c5c;
                padding: 2px;
            }
            QSpinBox::up-button, QSpinBox::down-button {
                background-color: #5c5c5c;
                border: 1px solid #3c3c3c;
                width: 16px;
            }
            QSpinBox::up-button:hover, QSpinBox::down-button:hover {
                background-color: #6c6c6c;
            }
            QSpinBox::up-arrow, QSpinBox::down-arrow {
                width: 8px;
                height: 8px;
            }
            """
            self.setStyleSheet(self.dark_style)
        self.trans_dark_mode = dark_mode
        self.parent_Window = MainWindow

        with open(f"{self.mylocaladdress}\Restaurant List\{self.parent_Window.SelectRestaurant.currentText()}.json","r") as f:
            data = json.load(f)
            self.MinimumWeight.setText(f"{data["RawMaterials"][0][4]}")
            for index in range(len(data["RawMaterials"])):
                self.mytext = data["RawMaterials"][index][0]
                self.SelectRawMaterial.addItem(self.mytext)

        # Connect the Buttons
        self.ExitWindow.clicked.connect(self.ExitingtheWindow)
        self.SavingChange.clicked.connect(self.SavingChangeFunction)
        self.SelectRawMaterial.currentIndexChanged.connect(self.ChangingCurrentIndexFunction)

        # Show the window
        self.show()
    def ExitingtheWindow(self):
        self.close()
    def SavingChangeFunction(self):
        with open(f"{self.mylocaladdress}\Restaurant List\{self.parent_Window.SelectRestaurant.currentText()}.json","r") as f:
            data = json.load(f)
            lister = data["RawMaterials"]
            for index in range(len(lister)):
                # print(f"{self.SelectRawMaterial.currentText()} and {self.MinimumWeight.text()}")
                if (self.SelectRawMaterial.currentText()==lister[index][0]):
                    data["RawMaterials"][index][4] = self.MinimumWeight.text()
                    break
        with open(f"{self.mylocaladdress}\Restaurant List\{self.parent_Window.SelectRestaurant.currentText()}.json","w") as f:
            json.dump(data,f,indent=4)
    def ChangingCurrentIndexFunction(self):
        currentIndex = self.SelectRawMaterial.currentIndex()
        with open(f"{self.mylocaladdress}\Restaurant List\{self.parent_Window.SelectRestaurant.currentText()}.json","r") as f:
            data = json.load(f)
            self.MinimumWeight.setText(f"{data["RawMaterials"][currentIndex][4]}")