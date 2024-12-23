from PyQt5.QtWidgets import QMainWindow,QPushButton,QLineEdit,QLabel,QFileDialog
from PyQt5.QtGui import QPixmap
from PyQt5 import uic
import json
import os

class EditRestaurant_UI(QMainWindow):
    def __init__(self,dark_mode,MainWindow):
        super(EditRestaurant_UI,self).__init__()

        # Load the UI
        uic.loadUi("EditRestaurant.ui",self)

        # Load the widgets
        self.myimagelabel = self.findChild(QLabel,"label")
        self.SelectImage = self.findChild(QPushButton,"pushButton")
        self.RestaurantName = self.findChild(QLineEdit,"lineEdit")
        self.GSTNumber = self.findChild(QLineEdit,"lineEdit_2")
        self.FSSAINumber = self.findChild(QLineEdit,"lineEdit_3")
        self.SaveChanges = self.findChild(QPushButton,"pushButton_2")
        self.Cancel = self.findChild(QPushButton,"pushButton_3")
        self.mylocaladdress = os.getcwd()

        self.original = self.RestaurantName.text()
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
        self.fname = "Not Found"
        self.parentWindow = MainWindow

        with open(f"{self.mylocaladdress}\Restaurant List\{MainWindow.SelectRestaurant.currentText()}.json","r") as f:
            data = json.load(f)
            self.RestaurantName.setText(f"{data["RestaurantName"]}")
            self.GSTNumber.setText(f"{data["GSTNumber"]}")
            self.FSSAINumber.setText(f"{data["FSSAINumber"]}")
            self.folder_name = data["LogoRestaurant"]
            self.pixmap = QPixmap(self.folder_name)
            self.myimagelabel.setPixmap(self.pixmap)
        self.original = self.RestaurantName.text()

        # Connect the Buttons
        self.Cancel.clicked.connect(self.CancelButton)
        self.SelectImage.clicked.connect(self.SelectingImg)
        self.SaveChanges.clicked.connect(self.SavingChanges)

        # Show the Window
        self.show()
    def CancelButton(self):
        self.close()
    def SelectingImg(self):
        self.fname = QFileDialog.getOpenFileName(self,"Open Image","","All Files(*);;PNG Files(*.png);;JPEG Files(*.jpeg);;JPG Files(*.jpg)")
        if self.fname is not None:
            self.pixmap = QPixmap(self.fname[0])
            self.myimagelabel.setPixmap(self.pixmap)
    def SavingChanges(self):
        data = {
            "RestaurantName": self.RestaurantName.text(),
            "GSTNumber": self.GSTNumber.text(),
            "FSSAINumber": self.FSSAINumber.text(),
            "LogoRestaurant": self.fname,
            "Recipes": [],
            "RawMaterials": []
        }
        # print(self.original)
        # print(f"{self.mylocaladdress}\Restaurant List\{self.original}.json")
        # print(self.parentWindow.SelectRestaurant.currentText())
        # print(self.RestaurantName.text())
        if self.original!=self.RestaurantName.text():
            # os.remove(f"{self.mylocaladdress}\Restaurant List\{self.original}.json")
            current_index = self.parentWindow.SelectRestaurant.currentIndex()
            self.parentWindow.SelectRestaurant.removeItem(current_index)
            self.parentWindow.SelectRestaurant.addItem(f"{self.RestaurantName.text()}")
            
        with open(f"{self.mylocaladdress}\Restaurant List\{self.RestaurantName.text()}.json","w") as f:
            json.dump(data,f,indent=4)
            f.write('\n')
