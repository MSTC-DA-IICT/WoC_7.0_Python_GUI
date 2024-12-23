from PyQt5.QtWidgets import QMainWindow,QListWidget,QMenu,QAction,QMessageBox
from PyQt5.QtGui import QColor
from PyQt5.QtCore import Qt
from PyQt5 import uic
import os
from Edit_RawMaterials import Edit_RawMaterials_UI
import json

class Inventory_2UI(QMainWindow):
    def __init__(self,dark_mode,MainWindow):
        super(Inventory_2UI,self).__init__()

        # Load the UI
        uic.loadUi("Inventory_2.ui",self)

        # Load the Widgets
        self.ItemList = self.findChild(QListWidget,"listWidget_2")
        self.Qty = self.findChild(QListWidget,"listWidget_3")
        self.ProductSupplier = self.findChild(QListWidget,"listWidget")
        self.MinQty = self.findChild(QListWidget,"listWidget_4")
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
            lister = data["RawMaterials"]
            for index in range(len(lister)):
                self.ItemList.addItem(f"{lister[index][0]}")
                self.Qty.addItem(f"{float(lister[index][1]):.3f}")
                self.ProductSupplier.addItem(f"{lister[index][3]}")
                self.MinQty.addItem(f"{lister[index][4]}")
        
        for index in range(self.ItemList.count()):
            if float(self.Qty.item(index).text())<float(self.MinQty.item(index).text()):
                self.Qty.item(index).setForeground(QColor("red"))

        # Connect the Buttons
        self.ItemList.setContextMenuPolicy(Qt.CustomContextMenu)
        self.ItemList.customContextMenuRequested.connect(self.OpenMenuBar)

        # Show the Window
        self.show()
    def OpenMenuBar(self,position):
        menu = QMenu()

        # Create Actions
        remove_action = QAction("Toss the item",self)
        edit_action = QAction("Edit the name",self)

        # Connect actions to their handlers
        remove_action.triggered.connect(self.RemovingItemfromList)
        edit_action.triggered.connect(self.EditingNameofItem)

        # Add Actions to their menu
        menu.addAction(remove_action)
        menu.addAction(edit_action)

        # Show the context menu at the cursor position
        menu.exec_(self.ItemList.mapToGlobal(position))
    def RemovingItemfromList(self):
        currentIndex = self.ItemList.currentRow()
        currentItem = self.ItemList.item(currentIndex)
        question = QMessageBox.question(self,"Remove Raw Material",f"Are you sure of deleting item {currentItem.text()}", QMessageBox.Yes | QMessageBox.No)
        if question == QMessageBox.Yes:
            item = self.ItemList.takeItem(currentIndex)
            with open(f"{self.mylocaladdress}\Restaurant List\{self.parent_Window.SelectRestaurant.currentText()}.json","r") as f:
                data = json.load(f)
                data["RawMaterials"].pop(currentIndex)
            with open(f"{self.mylocaladdress}\Restaurant List\{self.parent_Window.SelectRestaurant.currentText()}.json","w") as f:
                json.dump(data,f,indent=4)
                f.write('\n')
            item2 = self.ProductSupplier.takeItem(currentIndex)
            item3 = self.Qty.takeItem(currentIndex)
            item4 = self.MinQty.takeItem(currentIndex)
            del item
            del item2
            del item3
            del item4
    def EditingNameofItem(self):
        self.window = Edit_RawMaterials_UI(self,self.parent_Window)
        self.window.show()
        