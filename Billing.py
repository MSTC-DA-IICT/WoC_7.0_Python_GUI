from PyQt5.QtWidgets import QMainWindow,QPushButton,QLineEdit,QLabel,QInputDialog,QListWidget,QMenu,QAction,QMessageBox,QFileDialog
from AddingItem import AddingUI
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt
from PyQt5 import uic
from AddingItem import AddingUI
import time
import json
import os

class BillingUI(QMainWindow):
    def __init__(self,dark_mode,MainWindow):
        super(BillingUI,self).__init__()

        # Load the UI
        uic.loadUi("Billing.ui",self)

        # Load the widgets
        self.AddFood = self.findChild(QPushButton,"pushButton")
        self.currenttime = self.findChild(QLabel,"label_4")
        self.currentdate = self.findChild(QLabel,"label_3")
        self.RestaurantName = self.findChild(QLabel,"label_6")
        self.GSTNumber = self.findChild(QLabel,"label_7")
        self.FSSAINumber = self.findChild(QLabel,"label_8")
        self.tokenNumber = self.findChild(QLabel,"label_2")
        self.myimagelabel = self.findChild(QLabel,"label")
        self.GenerateBillButton = self.findChild(QPushButton,"pushButton_2")
        self.LoadABill = self.findChild(QPushButton,"pushButton_3")
        self.OrderList = self.findChild(QListWidget,"listWidget")
        self.OrderQty = self.findChild(QListWidget,"listWidget_2")
        self.DiscountQty = self.findChild(QListWidget,"listWidget_3")
        self.PriceList = self.findChild(QListWidget,"listWidget_4")
        self.AmountList = self.findChild(QListWidget,"listWidget_5")
        self.SubTotal = self.findChild(QLineEdit,"lineEdit")
        self.DiscountAmount = self.findChild(QLineEdit,"lineEdit_2")
        self.GrandTotal = self.findChild(QLineEdit,"lineEdit_3")
        self.isLoaded = False
        self.mylocaladdress = os.getcwd()

        self.parentWindow = MainWindow
        self.folder_name = "Not available"
        with open(f"{self.mylocaladdress}\Restaurant List\{self.parentWindow.SelectRestaurant.currentText()}.json","r") as f:
            data = json.load(f)
            self.RestaurantName.setText(f"{data["RestaurantName"]}")
            self.GSTNumber.setText(f"{data["GSTNumber"]}")
            self.FSSAINumber.setText(f"{data["FSSAINumber"]}")
            self.folder_name = data["LogoRestaurant"]
            self.pixmap = QPixmap(self.folder_name)
            self.myimagelabel.setPixmap(self.pixmap)

        self.AddFood.clicked.connect(self.OpenWindowAddingFood)
        self.timing = time.strftime("%H:%M")
        self.monthdict = ["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sept","Oct","Nov","Dec"]
        self.date = time.strftime("%d")
        self.year = time.strftime("%Y")
        self.month = time.strftime("%m")
        self.currenttime.setText(self.timing)
        self.currentdate.setText(f"{self.date} {self.monthdict[int(self.month)-1]}, {self.year}")

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
        self.file_name = "Not Found"

        self.CustomerName = "Null"

        if not os.path.exists(f"{self.mylocaladdress}\Billings\{self.RestaurantName.text()}"):
            os.makedirs(f"{self.mylocaladdress}\Billings\{self.RestaurantName.text()}")
        
        if self.OrderList.count() == 0:
            self.SubTotal.setText("0.0")
            self.DiscountAmount.setText("0.0")
            self.GrandTotal.setText("0.0")
        self.tokenNumber.setText(f"Token No.{len(os.listdir(f"{self.mylocaladdress}\Billings\{self.parentWindow.SelectRestaurant.currentText()}"))+1}")
        self.masterList = []
        self.SuperLister = []
        self.PreviousSubTotal = "0"
        self.PreviousDiscountAmount = "0"
        self.PreviousGrandTotal = "0"

        # Connect the Buttons
        self.AddFood.clicked.connect(self.OpenWindowAddingFood)
        self.OrderList.setContextMenuPolicy(Qt.CustomContextMenu)
        self.OrderList.customContextMenuRequested.connect(self.OpenMenuBar)
        self.GenerateBillButton.clicked.connect(self.GenerateBillFunction)
        self.LoadABill.clicked.connect(self.LoadingABillFunction)

        # Show the window
        self.show()
    
    def OpenWindowAddingFood(self):
        self.window = AddingUI(self.trans_dark_mode,self,self.parentWindow)
        self.window.show()
    def OpenMenuBar(self,position):
        menu = QMenu()

        # Create Actions
        remove_action = QAction("Remove an item",self)

        # Connect to Handlers
        remove_action.triggered.connect(self.RemovinganItemfromBill)

        # Add actions to their menu
        menu.addAction(remove_action)

        # Show the context menu at the cursor position
        menu.exec_(self.OrderList.mapToGlobal(position))
    def RemovinganItemfromBill(self):
        currentIndex = self.OrderList.currentRow()
        question = QMessageBox.warning(self,"Remove an Item",f"Are you sure of deleting item {self.OrderList.item(currentIndex).text()}?", QMessageBox.Yes | QMessageBox.No)
        if question == QMessageBox.Yes:
            item = self.OrderList.takeItem(currentIndex)
            item2 = self.OrderQty.takeItem(currentIndex)
            item3 = self.DiscountQty.takeItem(currentIndex)
            item4 = self.PriceList.takeItem(currentIndex)
            item5 = self.AmountList.takeItem(currentIndex)
            self.SubTotal.setText(f"{float(self.SubTotal.text())-float(item5.text())}")
            self.DiscountAmount.setText(f"{float(self.DiscountAmount.text())-(float(item5.text())*float(item3.text())/100)}")
            self.GrandTotal.setText(f"{float(self.SubTotal.text())-float(self.DiscountAmount.text())}")
            del item
            del item2
            del item3
            del item4
            del item5
    def LoadingABillFunction(self):
        self.OrderList.clear()
        self.OrderQty.clear()
        self.DiscountQty.clear()
        self.PriceList.clear()
        self.AmountList.clear()
        self.file_name = QFileDialog.getOpenFileName(self,"Open JSON File",f"{self.mylocaladdress}\Billings\{self.RestaurantName.text()}","JSON Files(*.json)")
        templist = self.file_name[0].split('/')
        self.file_name = templist[-1]
        self.isLoaded = True
        if self.file_name is not None:
            with open(f"{self.mylocaladdress}\Billings\{self.RestaurantName.text()}\{self.file_name}","r") as f:
                data = json.load(f)
                lister = data["ItemList"]
                self.SuperLister = lister
                for index in range(len(lister)):
                    self.OrderList.addItem(f"{lister[index][0]}")
                    self.OrderQty.addItem(f"{lister[index][1]}")
                    self.DiscountQty.addItem(f"{lister[index][2]}")
                    self.PriceList.addItem(f"{lister[index][3]}")
                    self.AmountList.addItem(f"{lister[index][4]}")
                self.SubTotal.setText(f"{data["PriceTotal"]}")
                self.DiscountAmount.setText(f"{data["DiscountTotal"]}")
                self.GrandTotal.setText(f"{data["GrandTotal"]}")
                self.PreviousSubTotal  = self.SubTotal.text()
                self.PreviousDiscountAmount = self.DiscountAmount.text()
                self.PreviousGrandTotal = self.GrandTotal.text()
                for index in range(self.OrderList.count()):
                    with open(f"{self.mylocaladdress}\Recipes\{self.RestaurantName.text()}\{self.OrderList.item(index).text()}.json","r") as f:
                        data = json.load(f)
                        for index2 in range(len(data["RawMaterials"])):
                            lister = data["RawMaterials"][index2]
                            lister.append(self.OrderQty.item(index).text())
                            self.masterList.append(lister)
        else:
            return
    def GenerateBillFunction(self):
        if self.isLoaded==True or self.file_name!="Not Found":
            with open(f"{self.mylocaladdress}\Billings\{self.RestaurantName.text()}\{self.file_name}","r") as f:
                data = json.load(f)
                self.Billingdate = f"{data["BillingDate"]}"
            with open(f"{self.mylocaladdress}\Restaurant List\{self.RestaurantName.text()}.json","r") as f:
                data = json.load(f)
                for index in range(len(data["RawMaterials"])):
                    for index2 in range(len(self.masterList)):
                        if self.masterList[index2][0]==data["RawMaterials"][index][0]:
                            data["RawMaterials"][index][1] = f"{float(float(data["RawMaterials"][index][1])+(float(self.masterList[index2][1])*float(self.masterList[index2][2]))):.3f}"
                print("First data printed:",data)
            with open(f"{self.mylocaladdress}\Restaurant List\{self.RestaurantName.text()}.json","w") as f:
                json.dump(data,f,indent=4)
                f.write('\n')
            masterlister = []
            for index in range(self.OrderList.count()):
                lister = []
                lister.append(f"{self.OrderList.item(index).text()}")
                lister.append(f"{self.OrderQty.item(index).text()}")
                lister.append(f"{self.DiscountQty.item(index).text()}")
                lister.append(f"{self.PriceList.item(index).text()}")
                lister.append(f"{self.AmountList.item(index).text()}")
                masterlister.append(lister)
            with open(f"{self.mylocaladdress}\Billings\{self.RestaurantName.text()}\{self.file_name}","r") as f:
                data = json.load(f)
                data["ItemList"] = masterlister
                data["PriceTotal"] = f"{self.SubTotal.text()}"
                data["DiscountTotal"] = f"{self.DiscountAmount.text()}"
                data["GrandTotal"] = f"{self.GrandTotal.text()}"
            with open(f"{self.mylocaladdress}\Billings\{self.RestaurantName.text()}\{self.file_name}","w") as f:
                json.dump(data,f,indent=4)
                f.write('\n')
            self.isLoaded = False
            with open(f"{self.mylocaladdress}\Billings\{self.RestaurantName.text()}\{self.file_name}","w") as f:
                json.dump(data,f,indent=4)
                f.write('\n')
            # self.Billingdate = f"{self.date} {self.monthdict[int(self.month)-1]}, {self.year}"
            # if not os.path.exists(f"{self.mylocaladdress}\{self.Billingdate} {self.RestaurantName.text()}"):
            #     os.makedirs(f"{self.mylocaladdress}\{self.Billingdate} {self.RestaurantName.text()}")
            with open(f"{self.mylocaladdress}\{self.Billingdate} {self.RestaurantName.text()}\{self.CustomerName}_{len(os.listdir(f"{self.mylocaladdress}\Billings\{self.RestaurantName.text()}"))}.json","w") as f:
                json.dump(data,f,indent=4)
                f.write('\n')
            masterList = []
            for index in range(self.OrderList.count()):
                with open(f"{self.mylocaladdress}\Recipes\{self.RestaurantName.text()}\{self.OrderList.item(index).text()}.json","r") as f:
                    data = json.load(f)
                    for index2 in range(len(data["RawMaterials"])):
                        lister = data["RawMaterials"][index2]
                        lister.append(self.OrderQty.item(index).text())
                        masterList.append(lister)
            self.Unplaceable = False
            with open(f"{self.mylocaladdress}\Restaurant List\{self.RestaurantName.text()}.json","r") as f:
                data = json.load(f)
                for index in range(len(data["RawMaterials"])):
                    for index2 in range(len(masterList)):
                        if masterList[index2][0] == data["RawMaterials"][index][0]:
                            data["RawMaterials"][index][1] = f"{float(float(data["RawMaterials"][index][1])-(float(masterList[index2][1])*float(masterList[index2][2]))):.3f}"
                            if (float(data["RawMaterials"][index][1])<0.0):
                                self.Unplaceable = True
                # print(data)
                # print(self.Unplaceable)    
            with open(f"{self.mylocaladdress}\Restaurant List\{self.RestaurantName.text()}.json","w") as f:
                json.dump(data,f,indent=4)
                f.write('\n')
            # print("This is self.masterList:",self.masterList)
            # print("This is masterlister:",masterlister)
            # print("This is masterList:",masterList)
            # print("This is self.SuperLister:",self.SuperLister)
            if (self.Unplaceable==True):
                with open(f"{self.mylocaladdress}\Restaurant List\{self.RestaurantName.text()}.json","r") as f:
                    data = json.load(f)
                    for index in range(len(data["RawMaterials"])):
                        for index2 in range(len(masterList)):
                            if masterList[index2][0]==data["RawMaterials"][index][0]:
                                data["RawMaterials"][index][1] = f"{float(float(data["RawMaterials"][index][1])+float(float(masterList[index2][1])*float(masterList[index2][2]))):.3f}"
                self.msg_box = QMessageBox()
                self.msg_box.setIcon(QMessageBox.Warning)
                self.msg_box.setText("Order is not placed, insufficient Raw Materials Available")
                self.msg_box.setWindowTitle("Order Not Placed")
                self.msg_box.setStandardButtons(QMessageBox.Ok)
                retval = self.msg_box.exec_()
                with open(f"{self.mylocaladdress}\Restaurant List\{self.RestaurantName.text()}.json","w") as f:
                    json.dump(data,f,indent=4)
                    f.write('\n')
                with open(f"{self.mylocaladdress}\Billings\{self.RestaurantName.text()}\{self.file_name}","r") as f:
                    data = json.load(f)
                    data["ItemList"] = self.SuperLister
                    data["PriceTotal"] = self.PreviousSubTotal
                    data["DiscountTotal"] = self.PreviousDiscountAmount
                    data["GrandTotal"] = self.PreviousGrandTotal
                    print(data)
                with open(f"{self.mylocaladdress}\Billings\{self.RestaurantName.text()}\{self.file_name}","w") as f:
                    json.dump(data,f,indent=4)
                    f.write('\n')
                with open(f"{self.mylocaladdress}\{self.Billingdate} {self.RestaurantName.text()}\{self.file_name}","w") as f:
                    json.dump(data,f,indent=4)
                    f.write('\n')
                with open(f"{self.mylocaladdress}\Restaurant List\{self.RestaurantName.text()}.json","r") as f:
                    data = json.load(f)
                    for index in range(len(data["RawMaterials"])):
                        for index2 in range(len(self.masterList)):
                            if self.masterList[index2][0]==data["RawMaterials"][index][0]:
                                data["RawMaterials"][index][1] = f"{float(float(data["RawMaterials"][index][1])-(float(self.masterList[index2][1])*float(self.masterList[index2][2]))):.3f}"
                with open(f"{self.mylocaladdress}\Restaurant List\{self.RestaurantName.text()}.json","w") as f:
                    json.dump(data,f,indent=4)
                    f.write('\n')
                    print(data)
            self.close()
            return 
        text,ok = QInputDialog.getText(self,"Customer Bill","Enter the name of Customer:")
        if text and ok is not None:
            self.CustomerName = text
        data = {
            "CustomerName": self.CustomerName,
            "BillingDate": self.currentdate.text(),
            "BillingTime": self.currenttime.text(),
            "RestaurantName": self.RestaurantName.text(),
            "GSTNumber": self.GSTNumber.text(),
            "FSSAINumber": self.FSSAINumber.text(),
            "RestaurantLogo": self.folder_name,
            "TokenNumber": f"{len(os.listdir(f"{self.mylocaladdress}\Billings\{self.parentWindow.SelectRestaurant.currentText()}"))+1}",
            "ItemList": [],
            "PriceTotal": "0",
            "DiscountTotal": "0",
            "GrandTotal": "0" 
        }
        with open(f"{self.mylocaladdress}\Billings\{self.RestaurantName.text()}\{self.CustomerName}_{len(os.listdir(f"{self.mylocaladdress}\Billings\{self.RestaurantName.text()}"))+1}.json","w") as f:
            json.dump(data,f,indent=4)
            f.write('\n')
        with open(f"{self.mylocaladdress}\Billings\{self.RestaurantName.text()}\{self.CustomerName}_{len(os.listdir(f"{self.mylocaladdress}\Billings\{self.RestaurantName.text()}"))}.json","r") as f:
            data = json.load(f)
            for index in range(self.OrderList.count()):
                lister = []
                lister.append(self.OrderList.item(index).text())
                lister.append(self.OrderQty.item(index).text())
                lister.append(self.DiscountQty.item(index).text())
                lister.append(self.PriceList.item(index).text())
                lister.append(str(float(self.OrderQty.item(index).text())*float(self.PriceList.item(index).text())))
                data["ItemList"].append(lister)
        with open(f"{self.mylocaladdress}\Billings\{self.RestaurantName.text()}\{self.CustomerName}_{len(os.listdir(f"{self.mylocaladdress}\Billings\{self.RestaurantName.text()}"))}.json","w") as f:
            json.dump(data,f,indent=4)
            f.write('\n')
        with open(f"{self.mylocaladdress}\Billings\{self.RestaurantName.text()}\{self.CustomerName}_{len(os.listdir(f"{self.mylocaladdress}\Billings\{self.RestaurantName.text()}"))}.json","r") as f:
            data = json.load(f)
            data["PriceTotal"] = f"{self.SubTotal.text()}"
            data["DiscountTotal"] = f"{self.DiscountAmount.text()}"
            data["GrandTotal"] = f"{self.GrandTotal.text()}"
        with open(f"{self.mylocaladdress}\Billings\{self.RestaurantName.text()}\{self.CustomerName}_{len(os.listdir(f"{self.mylocaladdress}\Billings\{self.RestaurantName.text()}"))}.json","w") as f:
            json.dump(data,f,indent=4)
            f.write('\n')
        self.Billingdate = f"{self.date} {self.monthdict[int(self.month)-1]}, {self.year}"
        if not os.path.exists(f"{self.mylocaladdress}\{self.Billingdate} {self.RestaurantName.text()}"):
            os.makedirs(f"{self.mylocaladdress}\{self.Billingdate} {self.RestaurantName.text()}")
        with open(f"{self.mylocaladdress}\{self.Billingdate} {self.RestaurantName.text()}\{self.CustomerName}_{len(os.listdir(f"{self.mylocaladdress}\Billings\{self.RestaurantName.text()}"))}.json","w") as f:
            json.dump(data,f,indent=4)
            f.write('\n')
        masterList = []
        for index in range(self.OrderList.count()):
            with open(f"{self.mylocaladdress}\Recipes\{self.RestaurantName.text()}\{self.OrderList.item(index).text()}.json","r") as f:
                data = json.load(f)
                for index2 in range(len(data["RawMaterials"])):
                    lister = data["RawMaterials"][index2]
                    lister.append(self.OrderQty.item(index).text())
                    masterList.append(lister)
        self.Unplaceable = False
        with open(f"{self.mylocaladdress}\Restaurant List\{self.RestaurantName.text()}.json","r") as f:
            data = json.load(f)
            for index in range(len(data["RawMaterials"])):
                for index2 in range(len(masterList)):
                    if masterList[index2][0]==data["RawMaterials"][index][0]:
                        data["RawMaterials"][index][1] = f"{float(data["RawMaterials"][index][1])-float(masterList[index2][1])*float(masterList[index2][2]):.3f}"
                        if (float(data["RawMaterials"][index][1])<0.0):
                            self.Unplaceable = True
        with open(f"{self.mylocaladdress}\Restaurant List\{self.RestaurantName.text()}.json","w") as f:
            json.dump(data,f,indent=4)
            f.write('\n')
        if (self.Unplaceable==True):
            with open(f"{self.mylocaladdress}\Restaurant List\{self.RestaurantName.text()}.json","r") as f:
                data = json.load(f)
                for index in range(len(data["RawMaterials"])):
                    for index2 in range(len(masterList)):
                        if masterList[index2][0]==data["RawMaterials"][index][0]:
                            data["RawMaterials"][index][1] = f"{float(data["RawMaterials"][index][1])+float(masterList[index2][1])*float(masterList[index2][2]):.3f}"
            self.msg_box = QMessageBox()
            self.msg_box.setIcon(QMessageBox.Warning)
            self.msg_box.setText("Order is not placed, insufficient Raw Materials Available")
            self.msg_box.setWindowTitle("Order Not Placed")
            self.msg_box.setStandardButtons(QMessageBox.Ok)
            retval = self.msg_box.exec_()
            with open(f"{self.mylocaladdress}\Restaurant List\{self.RestaurantName.text()}.json","w") as f:
                json.dump(data,f,indent=4)
                f.write('\n')
            os.remove(f"{self.mylocaladdress}\{self.Billingdate} {self.RestaurantName.text()}\{self.CustomerName}_{len(os.listdir(f"{self.mylocaladdress}\Billings\{self.RestaurantName.text()}"))}.json")
            os.remove(f"{self.mylocaladdress}\Billings\{self.RestaurantName.text()}\{self.CustomerName}_{len(os.listdir(f"{self.mylocaladdress}\Billings\{self.RestaurantName.text()}"))}.json")
        self.close()
