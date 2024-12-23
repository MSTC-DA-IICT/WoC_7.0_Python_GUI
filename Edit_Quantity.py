from PyQt5.QtWidgets import QMainWindow,QPushButton,QLineEdit
from PyQt5 import uic

class Edit_Quantity_UI(QMainWindow):
    def __init__(self,MainWindow,index):
        super(Edit_Quantity_UI,self).__init__()

        # Load the UI
        uic.loadUi("Edit_Quantity.ui",self)

        # Add the Widgets
        self.RawMaterialName = self.findChild(QLineEdit,"lineEdit")
        self.RawMaterialName.setText(f"{MainWindow.RawMaterialList.item(index).text()}")
        self.RawMaterialName.setReadOnly(True)
        self.QuantityAmt = self.findChild(QLineEdit,"lineEdit_2")
        self.QuantityAmt.setText(f"{MainWindow.QtyofRawMaterialList.item(index).text()}")
        self.SavingChangesButton = self.findChild(QPushButton,"pushButton")
        self.CancelButton = self.findChild(QPushButton,"pushButton_2")
        self.parent_Window = MainWindow
        self.parent_index = index

        # Connect the Buttons
        self.CancelButton.clicked.connect(self.CancelButtonFunction)
        self.SavingChangesButton.clicked.connect(self.SavingChangesButtonFunction)

        # Show the Window
        self.show() 
    def CancelButtonFunction(self):
        self.close()
    def SavingChangesButtonFunction(self):
        if self.QuantityAmt.text()=="":
            return 
        self.parent_Window.QtyofRawMaterialList.item(self.parent_index).setText(f"{self.QuantityAmt.text()}")
        self.close()