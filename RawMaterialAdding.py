from PyQt5.QtWidgets import QMainWindow,QLineEdit,QPushButton
from PyQt5 import uic
import os

class RawMaterialAdding_UI(QMainWindow):
    def __init__(self,dark_mode,MainWindow):
        super(RawMaterialAdding_UI,self).__init__()

        # Load the UI
        uic.loadUi("RawMaterialAdding.ui",self)

        # Load the Widgets
        self.Cancel = self.findChild(QPushButton,"pushButton")
        self.RawMaterialName = self.findChild(QLineEdit,"lineEdit")
        self.Quantity = self.findChild(QLineEdit,"lineEdit_2")
        self.Price = self.findChild(QLineEdit,"lineEdit_3")
        self.AddRawMaterial = self.findChild(QPushButton,"pushButton_2")
        self.Supplier = self.findChild(QLineEdit,"lineEdit_4")
        self.Supplier.setText("None")
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
        self.Cancel.clicked.connect(self.ClosingtheWindow)
        self.AddRawMaterial.clicked.connect(self.AddingRawMaterial)

        # Show the Window
        self.show()
    def ClosingtheWindow(self):
        self.close()
    def AddingRawMaterial(self):
        self.parent_Window.RawMaterialList.addItem(f"{self.RawMaterialName.text()}")
        self.parent_Window.RawMaterialWeight.addItem(f"{float(self.Quantity.text()):.3f}")
        self.parent_Window.RawMaterialCostperWeight.addItem(f"{float(self.Price.text()):.3f}")
        self.parent_Window.SupplierName.append(f"{self.Supplier.text()}")
        self.RawMaterialName.setText("")
        self.Quantity.setText("")
        self.Price.setText("")
        self.Supplier.setText("None")

