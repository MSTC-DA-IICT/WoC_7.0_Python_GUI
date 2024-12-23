from PyQt5.QtWidgets import QMainWindow,QLineEdit,QPushButton
from PyQt5 import uic
from PyQt5.QtGui import QColor
import json
import os

class Edit_RawMaterials_UI(QMainWindow):
    def __init__(self,MainWindow,SuperMainWindow):
        super(Edit_RawMaterials_UI,self).__init__()

        # Load the UI file
        uic.loadUi("Edit_RawMaterials.ui",self)

        # Load the widgets
        self.ProductSupplierName = self.findChild(QLineEdit,"lineEdit")
        self.RawMaterialName = self.findChild(QLineEdit,"lineEdit_2")
        self.QtyAmount = self.findChild(QLineEdit,"lineEdit_3")
        self.TotalPrice = self.findChild(QLineEdit,"lineEdit_4")
        self.SavingChangesButton = self.findChild(QPushButton,"pushButton")
        self.parent_Window = MainWindow
        self.superparent_window = SuperMainWindow
        self.mylocaladdress = os.getcwd()

        index = self.parent_Window.ItemList.currentRow()
        self.ProductSupplierName.setText(f"{self.parent_Window.ProductSupplier.item(index).text()}")
        self.RawMaterialName.setText(f"{self.parent_Window.ItemList.item(index).text()}")
        self.QtyAmount.setText(f"{self.parent_Window.Qty.item(index).text()}")
        self.previousRawMaterialName = self.RawMaterialName.text()
        
        with open(f"{self.mylocaladdress}\Restaurant List\{self.superparent_window.SelectRestaurant.currentText()}.json","r") as f:
            data = json.load(f)
            self.TotalPrice.setText(f"{data["RawMaterials"][index][2]}")
        
        # Connect the Buttons
        self.SavingChangesButton.clicked.connect(self.SavingChangesFunction)

        # Show the window
        self.show()
    def SavingChangesFunction(self):
        index = self.parent_Window.ItemList.currentRow()
        item1 = self.parent_Window.ProductSupplier.item(index)
        item2 = self.parent_Window.ItemList.item(index)
        item3 = self.parent_Window.Qty.item(index)
        item1.setText(f"{self.ProductSupplierName.text()}")
        item2.setText(f"{self.RawMaterialName.text()}")
        item3.setText(f"{float(self.QtyAmount.text()):.3f}")
        if float(item3.text())<float(self.parent_Window.MinQty.item(index).text()):
            self.parent_Window.Qty.item(index).setForeground(QColor("red"))
        else:
            self.parent_Window.Qty.item(index).setForeground(QColor())
        with open(f"{self.mylocaladdress}\Restaurant List\{self.superparent_window.SelectRestaurant.currentText()}.json","r") as f:
            data = json.load(f)
            data["RawMaterials"][index][0] = self.RawMaterialName.text()
            data["RawMaterials"][index][1] = f"{float(self.QtyAmount.text()):.3f}"
            data["RawMaterials"][index][3] = self.ProductSupplierName.text()
            data["RawMaterials"][index][2] = self.TotalPrice.text()
        with open(f"{self.mylocaladdress}\Restaurant List\{self.superparent_window.SelectRestaurant.currentText()}.json","w") as f:
            json.dump(data,f,indent=4)
            f.write('\n')
        folder_path = f"{self.mylocaladdress}\Recipes\{self.superparent_window.SelectRestaurant.currentText()}"
        for file in (os.listdir(folder_path)):
            with open(f"{folder_path}\{file}","r") as f:
                print(f"{folder_path}\{file}")
                data = json.load(f)
                lister = data["RawMaterials"]
                for index in range(len(lister)):
                    print(f"{self.previousRawMaterialName}")
                    if lister[index][0]==self.previousRawMaterialName:
                        data["RawMaterials"][index][0] = self.RawMaterialName.text()
            with open(f"{folder_path}\{file}","w") as f:
                json.dump(data,f,indent=4)
                f.write('\n')
        self.close()