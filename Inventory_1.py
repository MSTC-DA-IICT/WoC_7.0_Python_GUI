from PyQt5.QtWidgets import QMainWindow,QPushButton
from PyQt5 import uic
from Inventory_2 import Inventory_2UI
from Inventory_3 import Inventory_3UI
from Inventory_4 import Inventory_4UI
from Inventory_5 import Inventory_5UI
import json

class InventoryUI(QMainWindow):
    def __init__(self,dark_mode,MainWindow):
        super(InventoryUI,self).__init__()

        # Load the UI
        uic.loadUi("Inventory_1.ui",self)
        
        # Load the Widgets
        self.CurrentInventory = self.findChild(QPushButton,"pushButton")
        self.AddItemsInventory = self.findChild(QPushButton,"pushButton_2")
        self.RecipeManagement = self.findChild(QPushButton,"pushButton_3")
        self.MinimumThreshold = self.findChild(QPushButton,"pushButton_4")

        # Connect Buttons to Functions
        self.CurrentInventory.clicked.connect(self.OpenCurrentInventory)
        self.AddItemsInventory.clicked.connect(self.OpenAddItemInventory)
        self.RecipeManagement.clicked.connect(self.OpenRecipeManagement)
        self.MinimumThreshold.clicked.connect(self.OpenMinimumThreshold)

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

        # Show the window
        self.show()
    def OpenCurrentInventory(self):
        self.window = Inventory_2UI(self.trans_dark_mode,self.parent_Window)
        self.window.show()
    def OpenAddItemInventory(self):
        self.window = Inventory_3UI(self.trans_dark_mode,self.parent_Window)
        self.window.show()
    def OpenRecipeManagement(self):
        self.window = Inventory_4UI(self.trans_dark_mode,self.parent_Window)
        self.window.show()
    def OpenMinimumThreshold(self):
        self.window = Inventory_5UI(self.trans_dark_mode,self.parent_Window)
        self.window.show()