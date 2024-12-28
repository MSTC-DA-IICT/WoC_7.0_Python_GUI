from PyQt5.QtWidgets import QMainWindow,QLineEdit,QPushButton,QComboBox
from PyQt5 import uic
import os
import json

class RecipeAdder_UI(QMainWindow):
    def __init__(self,dark_mode,MainWindow,superMainWindow):
        super(RecipeAdder_UI,self).__init__()

        # Load the UI
        uic.loadUi("RecipeAdder.ui",self)

        # Load the Widgets
        self.mycomboBox = self.findChild(QComboBox,"comboBox")
        self.NameofRecipe = self.findChild(QLineEdit,"lineEdit")
        self.PriceofRecipe = self.findChild(QLineEdit,"lineEdit_3")
        self.AddingRecipeButton = self.findChild(QPushButton,"pushButton_2")
        self.CancelButton = self.findChild(QPushButton,"pushButton")
        self.mylocaladdress = os.getcwd()
        self.mycomboBox.addItem("Starters")
        self.mycomboBox.addItem("Fast Food")
        self.mycomboBox.addItem("Salads")
        self.mycomboBox.addItem("Soup")
        self.mycomboBox.addItem("Punjabi")
        self.mycomboBox.addItem("Pizza")
        self.mycomboBox.addItem("Gujarati")
        self.mycomboBox.addItem("Rice")
        self.mycomboBox.addItem("Dal/Curries")
        self.mycomboBox.addItem("Dessert")
        self.mycomboBox.addItem("Drinks")
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
        self.superparent_Window = superMainWindow

        # Connect the Buttons
        self.AddingRecipeButton.clicked.connect(self.AddingRecipestoRestaurantFunction)

        # Show the Window
        self.show()
    def AddingRecipestoRestaurantFunction(self):
        self.parent_Window.RecipesList.addItem(f"{self.NameofRecipe.text()}")
        self.parent_Window.RecipeGenre.addItem(f"{self.mycomboBox.currentText()}")
        self.parent_Window.RecipePrice.addItem(f"{self.PriceofRecipe.text()}")
        self.NameofRecipe.setText("")
        self.PriceofRecipe.setText("")
