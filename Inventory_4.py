from PyQt5.QtWidgets import QMainWindow,QListWidget,QPushButton,QLineEdit,QComboBox,QMenu,QAction,QMessageBox,QFileDialog
from PyQt5 import uic
from PyQt5.QtCore import Qt
from Edit_Quantity import Edit_Quantity_UI
import json
import os

class Inventory_4UI(QMainWindow):
    def __init__(self,dark_mode,MainWindow):
        super(Inventory_4UI,self).__init__()

        # Load the UI
        uic.loadUi("Inventory_4.ui",self)

        # Load the widgets
        self.SelectRecipeName = self.findChild(QComboBox,"comboBox")
        self.SelectRawMaterial = self.findChild(QComboBox,"comboBox_2")
        self.AddingRawMaterialtoList = self.findChild(QPushButton,"pushButton")
        self.QtyofRawMaterial = self.findChild(QLineEdit,"lineEdit")
        self.RawMaterialList = self.findChild(QListWidget,"listWidget")
        self.QtyofRawMaterialList = self.findChild(QListWidget,"listWidget_2")
        self.SavingChangesButton = self.findChild(QPushButton,"pushButton_2")
        self.LoadARecipe = self.findChild(QPushButton,"pushButton_3")
        self.currentIndexofList = 0
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
            lister1 = data["RawMaterials"]
            lister2 = data["Recipes"]
            for index in range(len(lister1)):
                self.SelectRawMaterial.addItem(lister1[index][0])
            for index in range(len(lister2)):
                self.SelectRecipeName.addItem(lister2[index][0])

        with open(f"{self.mylocaladdress}\Recipes\{self.parent_Window.SelectRestaurant.currentText()}\{self.SelectRecipeName.currentText()}.json","r") as f:
            data = json.load(f)
            lister = data["RawMaterials"]
            if len(lister)!=0:
                for index in range(len(lister)):
                    self.RawMaterialList.addItem(f"{data["RawMaterials"][index][0]}")
                    self.QtyofRawMaterialList.addItem(f"{data["RawMaterials"][index][1]}")
                self.currentIndexofList = len(lister)

        # Connect the Buttons
        self.RawMaterialList.setContextMenuPolicy(Qt.CustomContextMenu)
        self.RawMaterialList.customContextMenuRequested.connect(self.OpenMenuBarFunction)
        self.AddingRawMaterialtoList.clicked.connect(self.AddingRawMaterialtoRecipeFunction)
        self.SavingChangesButton.clicked.connect(self.SavingRawMaterialsFunction)
        self.SelectRecipeName.currentIndexChanged.connect(self.IndexisChangedFunction)
        self.LoadARecipe.clicked.connect(self.LoadARecipeFunction)

        # Show the window
        self.show()

    def AddingRawMaterialtoRecipeFunction(self):
        if self.QtyofRawMaterial.text()=="":
            return
        for index in range(self.RawMaterialList.count()):
            if (self.RawMaterialList.item(index).text()==self.SelectRawMaterial.currentText()):
                return
        self.RawMaterialList.addItem(f"{self.SelectRawMaterial.currentText()}")
        self.QtyofRawMaterialList.addItem(f"{self.QtyofRawMaterial.text()}")
        self.QtyofRawMaterial.setText("")
    def LoadARecipeFunction(self):
        self.file_name = QFileDialog.getOpenFileName(self,"Open JSON File",f"{self.mylocaladdress}\Recipes\{self.parent_Window.SelectRestaurant.currentText()}","JSON Files(*.json)")
        if self.file_name!=('',''):
            with open(f"{self.file_name[0]}") as f:
                data = json.load(f)
                lister = data["RawMaterials"]
                for index in range(len(lister)):
                    self.RawMaterialList.addItem(f"{lister[index][0]}")
                    self.QtyofRawMaterialList.addItem(f"{lister[index][1]}")
    def SavingRawMaterialsFunction(self):
        if self.RawMaterialList.count()==0:
            return
        with open(f"{self.mylocaladdress}\Recipes\{self.parent_Window.SelectRestaurant.currentText()}\{self.SelectRecipeName.currentText()}.json","r") as f:
            data = json.load(f)
            data["RawMaterials"] = []
            for index in range(self.RawMaterialList.count()):
                lister = []
                item = self.RawMaterialList.item(index)
                item2 = self.QtyofRawMaterialList.item(index)
                lister.append(item.text())
                lister.append(item2.text())
                data["RawMaterials"].append(lister)
        with open(f"{self.mylocaladdress}\Recipes\{self.parent_Window.SelectRestaurant.currentText()}\{self.SelectRecipeName.currentText()}.json","w") as f:
            json.dump(data,f,indent=4)
            f.write('\n')
    def IndexisChangedFunction(self):
        self.RawMaterialList.clear()
        self.QtyofRawMaterialList.clear()
        with open(f"{self.mylocaladdress}\Recipes\{self.parent_Window.SelectRestaurant.currentText()}\{self.SelectRecipeName.currentText()}.json","r") as f:
            data = json.load(f)
            lister = data["RawMaterials"]
            if len(lister)!=0:
                for index in range(len(lister)):
                    self.RawMaterialList.addItem(f"{data["RawMaterials"][index][0]}")
                    self.QtyofRawMaterialList.addItem(f"{float(data["RawMaterials"][index][1]):.3f}")
                self.currentIndexofList = len(lister)
            else:
                self.RawMaterialList.clear()
                self.QtyofRawMaterialList.clear()
                self.currentIndexofList = 0
    def OpenMenuBarFunction(self,position):
        menu = QMenu()

        # Create Actions
        remove_action = QAction("Toss the Recipe",self)
        edit_action = QAction("Edit Recipe name",self)

        # Connect to Handlers
        remove_action.triggered.connect(self.RemovingRawMaterialfromList)
        edit_action.triggered.connect(self.EditingRawMaterialName)

        # Add Actions to their Menu
        menu.addAction(remove_action)
        menu.addAction(edit_action)

        # Show the context menu at the cursor position
        menu.exec_(self.RawMaterialList.mapToGlobal(position))
    def RemovingRawMaterialfromList(self):
        currentIndex = self.RawMaterialList.currentRow()
        currentItem = self.RawMaterialList.item(currentIndex)
        question = QMessageBox.warning(self,"Remove Raw Material",f"Are of sure of Removing item {currentItem.text()} ?", QMessageBox.Yes | QMessageBox.No)
        if question == QMessageBox.Yes:
            item = self.RawMaterialList.takeItem(currentIndex)
            item2 = self.QtyofRawMaterialList.takeItem(currentIndex)
            del item
            del item2
    def EditingRawMaterialName(self):
        currentIndex = self.RawMaterialList.currentRow()
        self.window = Edit_Quantity_UI(self,currentIndex)
        self.window.show()
