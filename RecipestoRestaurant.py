from PyQt5.QtWidgets import QMainWindow,QListWidget,QPushButton
from PyQt5 import uic
from RecipeAdder import RecipeAdder_UI
import json
import os

class RecipestoRestaurant_UI(QMainWindow):
    def __init__(self,dark_mode,MainWindow):
        super(RecipestoRestaurant_UI,self).__init__()

        # Load the UI
        uic.loadUi("RecipestoRestaurant.ui",self)

        # Load the widgets
        self.AddRecipe = self.findChild(QPushButton,"pushButton")
        self.RecipesList = self.findChild(QListWidget,"listWidget")
        self.RecipeGenre = self.findChild(QListWidget,"listWidget_2")
        self.RecipePrice = self.findChild(QListWidget,"listWidget_3")
        self.SaveChangesButton = self.findChild(QPushButton,"pushButton_2")
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
        self.AddRecipe.clicked.connect(self.OpenRecipeAdder)
        self.SaveChangesButton.clicked.connect(self.SavingRecipesFunction)

        # Show the Window
        self.show()
    def OpenRecipeAdder(self):
        self.window = RecipeAdder_UI(self.trans_dark_mode,self,self.parent_Window)
        self.window.show()
    def SavingRecipesFunction(self):
        with open(f"{self.mylocaladdress}\Restaurant List\{self.parent_Window.SelectRestaurant.currentText()}.json","r") as f:
            data = json.load(f)
            for index in range(self.RecipesList.count()):
                lister = []
                lister.append(self.RecipesList.item(index).text())
                lister.append(self.RecipeGenre.item(index).text())
                lister.append(self.RecipePrice.item(index).text())
                data["Recipes"].append(lister)
        with open(f"{self.mylocaladdress}\Restaurant List\{self.parent_Window.SelectRestaurant.currentText()}.json","w") as f:
            json.dump(data,f,indent=4)
            f.write('\n')
        if not os.path.exists(f"{self.mylocaladdress}\Recipes"):
            os.makedirs(f"{self.mylocaladdress}\Recipes")
        if not os.path.exists(f"{self.mylocaladdress}\Recipes\{self.parent_Window.SelectRestaurant.currentText()}"):
            os.makedirs(f"{self.mylocaladdress}\Recipes\{self.parent_Window.SelectRestaurant.currentText()}")
        for index in range(self.RecipesList.count()):
            with open(f"{self.mylocaladdress}\Recipes\{self.parent_Window.SelectRestaurant.currentText()}\{self.RecipesList.item(index).text()}.json","w") as f:
                data = {
                    "NameofRecipe": self.RecipesList.item(index).text(),
                    "RecipeGenre": self.RecipeGenre.item(index).text(),
                    "PriceofRecipe": self.RecipePrice.item(index).text(),
                    "RawMaterials": []
                }
                json.dump(data,f,indent=4)
                f.write('\n')
        self.RecipesList.clear()
        self.RecipeGenre.clear()
        self.RecipePrice.clear()
