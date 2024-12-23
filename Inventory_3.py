from PyQt5.QtWidgets import QMainWindow,QPushButton,QLineEdit,QComboBox,QLabel
from PyQt5 import uic
import json
import os
import time

class Inventory_3UI(QMainWindow):
    def __init__(self,dark_mode,MainWindow):
        super(Inventory_3UI,self).__init__()

        # Load the UI
        uic.loadUi("Inventory_3.ui",self)

        # Load the widgets
        self.RawMaterialName = self.findChild(QComboBox,"comboBox")
        self.QtytobeAdded = self.findChild(QLineEdit,"lineEdit")
        self.PriceperWeight = self.findChild(QLineEdit,"lineEdit_2")
        self.AddingStockButton = self.findChild(QPushButton,"pushButton")
        self.QuitWindow = self.findChild(QPushButton,"pushButton_2")
        self.CurrentStock = self.findChild(QLabel,"label_4")
        self.MinimumStock = self.findChild(QLabel,"label_5")
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
        self.trans_dark_mode = True
        self.parent_Window = MainWindow

        with open(f"{self.mylocaladdress}\Restaurant List\{self.parent_Window.SelectRestaurant.currentText()}.json","r") as f:
            data = json.load(f)
            lister = data["RawMaterials"]
            self.CurrentStock.setText(f"Current Stock:{float(lister[0][1]):.3f}")
            self.MinimumStock.setText(f"Minimum Required:{lister[0][4]}")
            if (float(lister[0][1])<float(lister[0][4])):
                self.CurrentStock.setStyleSheet("color:red")
            for index in range(len(lister)):
                self.RawMaterialName.addItem(lister[index][0])

        # Connect the Buttons
        self.RawMaterialName.currentIndexChanged.connect(self.ChangingComboBoxIndexFunction)
        self.AddingStockButton.clicked.connect(self.PurchasingRawMaterial)

        # Show the window
        self.show()
    def ChangingComboBoxIndexFunction(self):
        index = self.RawMaterialName.currentIndex()
        self.CurrentStock.setStyleSheet("")
        with open(f"{self.mylocaladdress}\Restaurant List\{self.parent_Window.SelectRestaurant.currentText()}.json","r") as f:
            data = json.load(f)
            lister = data["RawMaterials"]
            for index in range(len(lister)):
                if (lister[index][0]==self.RawMaterialName.currentText()):
                    self.CurrentStock.setText(f"Current Stock:{float(lister[index][1]):.3f}")
                    self.MinimumStock.setText(f"Minimum Required:{lister[index][4]}")
                    if (float(lister[index][1])<float(lister[index][4])):
                        self.CurrentStock.setStyleSheet("color:red")
                    break
    def PurchasingRawMaterial(self):
        if not os.path.exists(f"{self.mylocaladdress}\Purchase Receipts"):
            os.makedirs(f"{self.mylocaladdress}\Purchase Receipts")
        if not os.path.exists(f"{self.mylocaladdress}\Purchase Receipts\{self.parent_Window.SelectRestaurant.currentText()}"):
            os.makedirs(f"{self.mylocaladdress}\Purchase Receipts\{self.parent_Window.SelectRestaurant.currentText()}")
        self.currentDate = time.strftime("%d")
        monthNames = ["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sept","Oct","Nov","Dec"]
        self.currentMonth = time.strftime("%m")
        self.currentYear = time.strftime("%Y")
        self.currentHour = time.strftime("%H")
        self.currentMinute = time.strftime("%M")
        self.Billingdate = f"{self.currentDate} {(monthNames[int(self.currentMonth)-1])}, {self.currentYear}"
        self.CurrentStockDataUnupdated = 0
        self.MinimumStockDatatobeUsed = 0
        data = {
            "NameofRawMaterial": self.RawMaterialName.currentText(),
            "DateofPurchase": f"{self.currentDate} {monthNames[int(self.currentMonth)-1]}, {self.currentYear}",
            "TimeofPurchase": f"{self.currentHour}:{self.currentMinute}",
            "Quantity": f"{float(self.QtytobeAdded.text()):.3f}",
            "CostperWeight": f"{self.PriceperWeight.text()}",
            "Price": f"{float(self.QtytobeAdded.text())*float(self.PriceperWeight.text())}" 
        }
        with open(f"{self.mylocaladdress}\Purchase Receipts\{self.parent_Window.SelectRestaurant.currentText()}\Bill_{len(os.listdir(f"{self.mylocaladdress}\Purchase Receipts\{self.parent_Window.SelectRestaurant.currentText()}"))+1}.json","w") as f:
            json.dump(data,f,indent=4)
            f.write('\n')
        if not os.path.exists(f"{self.mylocaladdress}\Bill {self.Billingdate} {self.parent_Window.SelectRestaurant.currentText()}"):
            os.makedirs(f"{self.mylocaladdress}\Bill {self.Billingdate} {self.parent_Window.SelectRestaurant.currentText()}")
        with open(f"{self.mylocaladdress}\Bill {self.Billingdate} {self.parent_Window.SelectRestaurant.currentText()}\Bill_{len(os.listdir(f"{self.mylocaladdress}\Purchase Receipts\{self.parent_Window.SelectRestaurant.currentText()}"))+1}.json","w") as f:
            json.dump(data,f,indent=4)
            f.write('\n')
        with open(f"{self.mylocaladdress}\Restaurant List\{self.parent_Window.SelectRestaurant.currentText()}.json","r") as f:
            data = json.load(f)
            lister = data["RawMaterials"]
            for index in range(len(lister)):
                if (lister[index][0]==self.RawMaterialName.currentText()):
                    self.CurrentStockDataUnupdated = data["RawMaterials"][index][1]
                    self.MinimumStockDatatobeUsed = data["RawMaterials"][index][4]
                    data["RawMaterials"][index][1] = str(float(data["RawMaterials"][index][1])+float(self.QtytobeAdded.text()))
                    data["RawMaterials"][index][2] = str(float(data["RawMaterials"][index][2])+(float(self.QtytobeAdded.text())*float(self.PriceperWeight.text())))
                    break
        with open(f"{self.mylocaladdress}\Restaurant List\{self.parent_Window.SelectRestaurant.currentText()}.json","w") as f:
            json.dump(data,f,indent=4)
            f.write('\n')
        self.CurrentStock.setText(f"Current Stock:{float(self.QtytobeAdded.text())+float(self.CurrentStockDataUnupdated)}")
        if (float(self.MinimumStockDatatobeUsed)<=float(self.CurrentStockDataUnupdated)+float(self.QtytobeAdded.text())):
            self.CurrentStock.setStyleSheet("")