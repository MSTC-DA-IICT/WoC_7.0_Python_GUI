from PyQt5.QtWidgets import QMainWindow,QPushButton,QSpinBox,QComboBox,QLineEdit,QMessageBox
from PyQt5 import uic
import os
import json

class AddingUI(QMainWindow):
    def __init__(self,dark_mode,MainWindow,superMainWindow):
        super(AddingUI,self).__init__()

        # Load the UI
        uic.loadUi("AddingItem.ui",self)

        # Load the Widgets
        self.SelectRecipeGenre = self.findChild(QComboBox,"comboBox")
        self.SelectRecipeName = self.findChild(QComboBox,"comboBox_2")
        self.DiscountPer = self.findChild(QLineEdit,"lineEdit")
        self.Quantity = self.findChild(QSpinBox,"spinBox")
        self.AddItemButton = self.findChild(QPushButton,"pushButton")
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
        self.parent_Window = MainWindow
        self.DiscountPer.setText("0")
        self.superparent_Window = superMainWindow
        self.SelectRecipeGenre.addItem("Starters")
        self.SelectRecipeGenre.addItem("Fast Food")
        self.SelectRecipeGenre.addItem("Salads")
        self.SelectRecipeGenre.addItem("Soup")
        self.SelectRecipeGenre.addItem("Punjabi")
        self.SelectRecipeGenre.addItem("Pizza")
        self.SelectRecipeGenre.addItem("Gujarati")
        self.SelectRecipeGenre.addItem("Rice")
        self.SelectRecipeGenre.addItem("Dal/Curries")
        self.SelectRecipeGenre.addItem("Dessert")
        self.SelectRecipeGenre.addItem("Drinks")
        
        folder_path = f"{self.mylocaladdress}\Recipes\{self.superparent_Window.SelectRestaurant.currentText()}"
        for file in os.listdir(f"{folder_path}"):
            with open(f"{folder_path}\{file}") as f:
                data = json.load(f)
                if data["RecipeGenre"]==f"{self.SelectRecipeGenre.currentText()}":
                    self.SelectRecipeName.addItem(f"{data["NameofRecipe"]}")

        # Connect the Buttons
        
        self.SelectRecipeGenre.currentIndexChanged.connect(self.ShowingAvailableRecipes)
        self.AddItemButton.clicked.connect(self.AddingRecipetoBill)
        self.folder_path = f"{self.mylocaladdress}\Recipes\{self.superparent_Window.SelectRestaurant.currentText()}"

        # Showing the Window
        self.show()
    def ShowingAvailableRecipes(self):
        for file in os.listdir(f"{self.folder_path}"):
            with open(f"{self.folder_path}\{file}") as f:
                data = json.load(f)
                if data["RecipeGenre"]==f"{self.SelectRecipeGenre.currentText()}":
                    self.SelectRecipeName.addItem(f"{data["NameofRecipe"]}")
    def AddingRecipetoBill(self):
        if self.Quantity.text()=="0" or self.SelectRecipeName.currentText()=="" or float(self.DiscountPer.text())>100 or float(self.DiscountPer.text())<0:
            return 
        self.masterList = []
        self.unplaceable = False
        with open(f"{self.mylocaladdress}\Recipes\{self.parent_Window.RestaurantName.text()}\{self.SelectRecipeName.currentText()}.json","r") as f:
            data = json.load(f)
            for index in range(len(data["RawMaterials"])):
                data["RawMaterials"][index].append(f"{self.Quantity.text()}")
                self.masterList.append(data["RawMaterials"][index])
        print(self.masterList)
        with open(f"{self.mylocaladdress}\Restaurant List\{self.parent_Window.RestaurantName.text()}.json","r") as f:
            data = json.load(f)
            for index in range(len(data["RawMaterials"])):
                for index2 in range(len(self.masterList)):
                    if self.masterList[index2][0]==data["RawMaterials"][index][0]:
                        data["RawMaterials"][index][1] = f"{float(float(data["RawMaterials"][index][1])-(float(self.masterList[index2][1])*float(self.masterList[index2][2]))):.3f}"   
                        if (float(data["RawMaterials"][index][1])<0.0):
                            self.unplaceable = True 
        # print(self.unplaceable)
        # print(data)
        if self.unplaceable == True:
            self.msg_box = QMessageBox()
            self.msg_box.setIcon(QMessageBox.Warning)
            self.msg_box.setText("Item couldn't be added to Bill, as insufficient raw material availability")
            self.msg_box.setWindowTitle("Order is not placed")
            self.msg_box.setStandardButtons(QMessageBox.Ok)
            retval = self.msg_box.exec_()
            return        
        currentItemName = self.SelectRecipeName.currentText()
        if self.parent_Window.OrderList.count()>0:
            for index in range(self.parent_Window.OrderList.count()):
                if self.parent_Window.OrderList.item(index).text()==currentItemName:
                    self.parent_Window.SubTotal.setText(f"{float(self.parent_Window.SubTotal.text())-float(self.parent_Window.AmountList.item(index).text())}")
                    self.parent_Window.DiscountAmount.setText(f"{float(self.parent_Window.DiscountAmount.text())-(float(self.parent_Window.DiscountQty.item(index).text())*float(self.parent_Window.AmountList.item(index).text())*0.01)}")
                    self.parent_Window.GrandTotal.setText(f"{float(self.parent_Window.SubTotal.text())-float(self.parent_Window.DiscountAmount.text())}")
                    self.parent_Window.OrderQty.item(index).setText(f"{self.Quantity.text()}")
                    self.parent_Window.DiscountQty.item(index).setText(f"{self.DiscountPer.text()}")
                    self.parent_Window.AmountList.item(index).setText(f"{float(self.Quantity.text())*float(self.parent_Window.PriceList.item(index).text())}")
                    with open(f"{self.folder_path}\{self.parent_Window.OrderList.item(index).text()}.json","r") as f:
                        data = json.load(f)
                        self.priceofRecipe = data["PriceofRecipe"]
                        self.totalAmount = float(self.Quantity.text())*float(data["PriceofRecipe"])
                        self.DiscountAmountPrice = float(self.Quantity.text())*float(data["PriceofRecipe"])*float(self.DiscountPer.text())*0.01
                        self.parent_Window.SubTotal.setText(f"{float(self.parent_Window.SubTotal.text())+float(self.totalAmount)}")
                        self.parent_Window.DiscountAmount.setText(f"{float(self.parent_Window.DiscountAmount.text())+float(self.DiscountAmountPrice)}")
                        self.parent_Window.GrandTotal.setText(f"{float(self.parent_Window.SubTotal.text())-float(self.parent_Window.DiscountAmount.text())}")
                    return
                else:
                    continue
        self.parent_Window.OrderList.addItem(f"{currentItemName}")
        self.parent_Window.OrderQty.addItem(f"{self.Quantity.text()}")
        self.parent_Window.DiscountQty.addItem(f"{self.DiscountPer.text()}")
        self.totalAmount = 0
        self.DiscountAmountPrice = 0
        with open(f"{self.mylocaladdress}\Recipes\{self.superparent_Window.SelectRestaurant.currentText()}\{self.SelectRecipeName.currentText()}.json","r") as f:
            data = json.load(f)
            self.parent_Window.PriceList.addItem(f"{data["PriceofRecipe"]}")
            self.parent_Window.AmountList.addItem(f"{float(self.Quantity.text())*float(data["PriceofRecipe"])}")
            self.totalAmount = float(self.Quantity.text())*float(data["PriceofRecipe"])
            self.DiscountAmountPrice = float(self.Quantity.text())*float(data["PriceofRecipe"])*float(self.DiscountPer.text())*0.01
        self.parent_Window.SubTotal.setText(f"{float(self.parent_Window.SubTotal.text())+self.totalAmount}")
        self.parent_Window.DiscountAmount.setText(f"{float(self.parent_Window.DiscountAmount.text())+self.DiscountAmountPrice}")
        self.parent_Window.GrandTotal.setText(f"{float(self.parent_Window.SubTotal.text())-float(self.parent_Window.DiscountAmount.text())}")
