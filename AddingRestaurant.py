from PyQt5.QtWidgets import QMainWindow,QPushButton,QLineEdit,QLabel,QFileDialog
from PyQt5.QtGui import QPixmap
from PyQt5 import uic
import os
import json

class AddingRestaurant_UI(QMainWindow):
    def __init__(self,dark_mode,MainWindow):
        super(AddingRestaurant_UI,self).__init__()

        # Load the UI
        uic.loadUi("AddingRestaurant.ui",self)

        # Load the widgets
        self.myimagelabel = self.findChild(QLabel,"label")
        self.SelectImage = self.findChild(QPushButton,"pushButton")
        self.RestaurantName = self.findChild(QLineEdit,"lineEdit")
        self.GSTNumber = self.findChild(QLineEdit,"lineEdit_2")
        self.FSSAINumber = self.findChild(QLineEdit,"lineEdit_3")
        self.AddRestauranttoList = self.findChild(QPushButton,"pushButton_2")
        self.Cancel = self.findChild(QPushButton,"pushButton_3")
        self.mylocaladdress = os.getcwd()

        folder_path = f"{self.mylocaladdress}\Restaurant List"
        try:
            if not os.path.exists(folder_path):
                os.makedirs(folder_path)
            else:
                print("Folder already exists\n")
        except Exception as e:
            print(f"An error occured {e}")

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
        self.ParentWindow = MainWindow
        self.mylocaladdress = os.getcwd()

        # Connect the Buttons
        self.Cancel.clicked.connect(self.CancelButton)
        self.SelectImage.clicked.connect(self.SelectingImg)
        self.AddRestauranttoList.clicked.connect(self.CreateRestaurantFolder)

        self.fname = "Not Found"

        # Show the Window
        self.show()
    def CancelButton(self):
        self.close()
    def SelectingImg(self):
        self.fname = QFileDialog.getOpenFileName(self,"Open Image","","All Files(*);;PNG Files(*.png);;JPEG Files(*.jpeg);;JPG Files(*.jpg)")
        if self.fname is not None:
            self.pixmap = QPixmap(self.fname[0])
            self.myimagelabel.setPixmap(self.pixmap)
    def CreateRestaurantFolder(self):
        data = {
            "RestaurantName": self.RestaurantName.text(),
            "GSTNumber": self.GSTNumber.text(),
            "FSSAINumber": self.FSSAINumber.text(),
            "LogoRestaurant": self.fname[0],
            "Recipes": [],
            "RawMaterials": []
        }
        with open(f"{self.mylocaladdress}\Restaurant List\{self.RestaurantName.text()}.json","a") as f:
            json.dump(data,f,indent=4)
            f.write('\n')
        self.ParentWindow.SelectRestaurant.addItem(f"{self.RestaurantName.text()}")
        self.ParentWindow.SelectRestaurant.setInsertPolicy(self.ParentWindow.SelectRestaurant.InsertAtBottom)
        self.ParentWindow.SelectRestaurant.setCurrentIndex(self.ParentWindow.SelectRestaurant.count()-1)
        self.close()
