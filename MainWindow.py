from PyQt5.QtWidgets import QMainWindow,QApplication,QComboBox,QPushButton
from PyQt5 import uic
from Billing import BillingUI
from Inventory_1 import InventoryUI
from AddingRestaurant import AddingRestaurant_UI
from RawMaterialtoRestaurant import RawMaterialtoRestaurant_UI
from RecipestoRestaurant import RecipestoRestaurant_UI
from EditRestaurant import EditRestaurant_UI
from Accounts import Accounts_UI
import os
import sys
import time
import json

class UI(QMainWindow):
    def __init__(self):
        super(UI,self).__init__()

        # Load the UI file
        uic.loadUi("MainWindow.ui",self)

        # Load the widgets
        self.NewRestaurant = self.findChild(QPushButton,"pushButton")
        self.EditRestaurant = self.findChild(QPushButton,"pushButton_2")
        self.StartBilling = self.findChild(QPushButton,"pushButton_3")
        self.SelectRestaurant = self.findChild(QComboBox,"comboBox")
        self.SelectTheme = self.findChild(QComboBox,"comboBox_2")
        self.KitchenInventory = self.findChild(QPushButton,"pushButton_4")
        self.AddNewRawMaterials = self.findChild(QPushButton,"pushButton_6")
        self.AddNewRecipes = self.findChild(QPushButton,"pushButton_5")
        self.DisplayAccounts = self.findChild(QPushButton,"pushButton_7")
        self.dark_mode = False
        self.mylocaladdress = os.getcwd()
        # print(self.mylocaladdress)

        self.SelectTheme.addItem("Light")
        self.SelectTheme.addItem("Dark")
        if not os.path.exists(f"{self.mylocaladdress}\Restaurant List"):
            os.makedirs(f"{self.mylocaladdress}\Restaurant List")
        if (len(os.listdir(f"{self.mylocaladdress}\Restaurant List"))!=0):
            for i in range(len(os.listdir(f"{self.mylocaladdress}\Restaurant List"))):
                with open(f"{self.mylocaladdress}\Restaurant List\{os.listdir(f"{self.mylocaladdress}\Restaurant List")[i]}","r") as f:
                    data = json.load(f)
                    self.SelectRestaurant.addItem(data["RestaurantName"])

        # Connect the Buttons
        self.StartBilling.clicked.connect(self.OpenNewWindowBilling)
        self.KitchenInventory.clicked.connect(self.OpenKitchenInventory)
        self.NewRestaurant.clicked.connect(self.OpenNewRestaurant)
        self.EditRestaurant.clicked.connect(self.OpenEditRestaurant)
        self.AddNewRawMaterials.clicked.connect(self.AddingNewRawMaterialsFunction)
        self.AddNewRecipes.clicked.connect(self.AddingNewRecipesFunction)
        self.SelectTheme.activated.connect(self.SwitchTheme)
        self.DisplayAccounts.clicked.connect(self.OpenRevenueAccounts)
        
        # Show the window
        self.show()
    def OpenRevenueAccounts(self):
        self.window = Accounts_UI(self)
        self.window.show()
    def OpenNewWindowBilling(self):
        self.window = BillingUI(self.dark_mode,self)
        self.window.show()
    def OpenKitchenInventory(self):
        self.window = InventoryUI(self.dark_mode,self)
        self.window.show()
    def OpenNewRestaurant(self):
        self.window2 = RecipestoRestaurant_UI(self.dark_mode,self)
        self.window2.show()
        self.window1 = RawMaterialtoRestaurant_UI(self.dark_mode,self)
        self.window1.show()
        time.sleep(0.8)
        self.window = AddingRestaurant_UI(self.dark_mode,self)
        self.window.show()
    def OpenEditRestaurant(self):
        self.window = EditRestaurant_UI(self.dark_mode,self)
        self.window.show()
    def AddingNewRawMaterialsFunction(self):
        self.window = RawMaterialtoRestaurant_UI(self.dark_mode,self)
        self.window.show()
    def AddingNewRecipesFunction(self):
        self.window = RecipestoRestaurant_UI(self.dark_mode,self)
        self.window.show()
    def SwitchTheme(self):
        if (self.SelectTheme.currentText()=="Light"):
            self.setStyleSheet("")
            self.dark_mode = False
        else:
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
            self.dark_mode = True

app = QApplication(sys.argv)

UIWindow = UI()

app.exec_()
