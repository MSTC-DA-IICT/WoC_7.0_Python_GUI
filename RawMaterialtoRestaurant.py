from PyQt5.QtWidgets import QMainWindow,QListWidget,QPushButton
from RawMaterialAdding import RawMaterialAdding_UI
from PyQt5 import uic
import json
import os

class RawMaterialtoRestaurant_UI(QMainWindow):
    def __init__(self,dark_mode,MainWindow):
        super(RawMaterialtoRestaurant_UI,self).__init__()

        # Load the UI
        uic.loadUi("RawMaterialtoRestaurant.ui",self)

        # Load the widgets
        self.AddRawMaterial = self.findChild(QPushButton,"pushButton")
        self.RawMaterialList = self.findChild(QListWidget,"listWidget")
        self.RawMaterialWeight = self.findChild(QListWidget,"listWidget_2")
        self.RawMaterialCostperWeight = self.findChild(QListWidget,"listWidget_3")
        self.SaveChanges = self.findChild(QPushButton,"pushButton_2")
        self.Cancel = self.findChild(QPushButton,"pushButton_3")
        self.SupplierName = []
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

        # Connect the Buttons
        self.AddRawMaterial.clicked.connect(self.OpenRawMaterialAdder)
        self.SaveChanges.clicked.connect(self.AddingtoRestaurant)

        # Show the Window
        self.show()
    def OpenRawMaterialAdder(self):
        self.window = RawMaterialAdding_UI(self.trans_dark_mode,self)
        self.window.show()
    def AddingtoRestaurant(self):
        with open(f"{self.mylocaladdress}\Restaurant List\{self.parent_Window.SelectRestaurant.currentText()}.json","r") as f:
            data = json.load(f)
        for index in range(self.RawMaterialList.count()):
            lister = []
            lister.append(f"{self.RawMaterialList.item(index).text()}")
            lister.append(f"{self.RawMaterialWeight.item(index).text()}")
            lister.append(f"{float(float(self.RawMaterialCostperWeight.item(index).text())*float(self.RawMaterialWeight.item(index).text())):.3f}")
            lister.append(f"{self.SupplierName[index]}")
            lister.append("0")
            data["RawMaterials"].append(lister)
        with open(f"{self.mylocaladdress}\Restaurant List\{self.parent_Window.SelectRestaurant.currentText()}.json","w") as f:
            json.dump(data,f,indent=4)
        self.RawMaterialCostperWeight.clear()
        self.RawMaterialWeight.clear()
        self.RawMaterialList.clear()