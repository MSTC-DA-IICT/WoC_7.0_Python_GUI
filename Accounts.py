from PyQt5.QtWidgets import QMainWindow,QTableWidget,QLineEdit,QCalendarWidget,QTableWidgetItem
from PyQt5 import uic
from PyQt5.QtGui import QColor
import os
import json

class Accounts_UI(QMainWindow):
    def __init__(self,MainWindow):
        super(Accounts_UI,self).__init__()

        # Load the UI
        uic.loadUi("Accounts.ui",self)

        # Add the widgets
        self.MyCalendar = self.findChild(QCalendarWidget,"calendarWidget")
        self.AccountsTable = self.findChild(QTableWidget,"tableWidget")
        self.TotalRevenue = self.findChild(QLineEdit,"lineEdit")
        self.CurrentDate = ""
        self.CurrentMonth = ""
        self.CurrentYear = ""
        self.AccountsTable.setColumnWidth(0,750)
        self.AccountsTable.setColumnWidth(1,120)
        self.AccountsTable.setColumnWidth(2,121)
        self.parent_Window = MainWindow
        self.RestaurantName = self.parent_Window.SelectRestaurant.currentText()
        self.monthNames = ["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sept","Oct","Nov","Dec"]
        self.BillingDate = ""
        self.TotalRevenue.setText("₹0.00")
        self.mylocaladdress = os.getcwd()

        # Connect the Buttons
        self.MyCalendar.selectionChanged.connect(self.Grabbing_the_date)

        # Show the Window
        self.show()
    def Grabbing_the_date(self):
        self.AccountsTable.clearContents()
        dateSelected = self.MyCalendar.selectedDate()
        # print(str(dateSelected.toPyDate()))
        self.CurrentYear = (str(dateSelected.toPyDate()))[0:4]
        # print(self.CurrentYear)
        self.CurrentMonth = (str(dateSelected.toPyDate()))[5:7]
        # print(self.CurrentMonth)
        self.CurrentDate = (str(dateSelected.toPyDate()))[8:10]
        # print(self.CurrentDate)
        self.BillingDate = f"{self.CurrentDate} {self.monthNames[int(self.CurrentMonth)-1]}, {self.CurrentYear}"
        print(self.BillingDate)
        self.insertRowstoListvar = []
        self.GrandTotalAmount = 0
        if self.BillingDate!="" and ((os.path.exists(f"{self.mylocaladdress}\{self.BillingDate} {self.RestaurantName}")) or (os.path.exists(f"{self.mylocaladdress}\Bill {self.BillingDate} {self.RestaurantName}"))):
            if os.path.exists(f"{self.mylocaladdress}\{self.BillingDate} {self.RestaurantName}"):
                for file_name in os.listdir(f"{self.mylocaladdress}\{self.BillingDate} {self.RestaurantName}"):
                    with open(f"{self.mylocaladdress}\{self.BillingDate} {self.RestaurantName}\{file_name}","r") as f:
                        data = json.load(f)
                        for index in range(len(data["ItemList"])):
                            print(f"{data["ItemList"][index][0]}")
                            self.mydict = {"ItemName":f"{file_name[0:len(file_name)-5]} | {data["ItemList"][index][0]}","Quantity":f"{data["ItemList"][index][1]}","Revenue":f"+{data["ItemList"][index][4]}"}
                            self.insertRowstoListvar.append(self.mydict)
                        self.GrandTotalAmount += float(data["GrandTotal"])
            if os.path.exists(f"{self.mylocaladdress}\Bill {self.BillingDate} {self.RestaurantName}"):
                for file_name in os.listdir(f"{self.mylocaladdress}\Bill {self.BillingDate} {self.RestaurantName}"):
                    with open(f"{self.mylocaladdress}\Bill {self.BillingDate} {self.RestaurantName}\{file_name}","r") as f:
                        data = json.load(f)
                        self.mydict = {"ItemName":f"{data["NameofRawMaterial"]}","Quantity":f"{data["Quantity"]}","Revenue":f"-{data["Price"]}"}
                        self.GrandTotalAmount -= float(data["Price"])
                        self.insertRowstoListvar.append(self.mydict)
            self.AccountsTable.setRowCount(len(self.insertRowstoListvar))
            row = 0
            for person in self.insertRowstoListvar:
                self.AccountsTable.setItem(row,0,QTableWidgetItem(person["ItemName"]))
                self.AccountsTable.setItem(row,1,QTableWidgetItem(person["Quantity"]))
                self.AccountsTable.setItem(row,2,QTableWidgetItem(person["Revenue"]))
                if person["Revenue"][0]=="-":
                    red_colored_item = self.AccountsTable.item(row,2)
                    red_colored_item.setForeground(QColor("darkred"))
                else:
                    green_colored_item = self.AccountsTable.item(row,2)
                    green_colored_item.setForeground(QColor("darkgreen"))
                row+=1
            if self.GrandTotalAmount>0.0:
                self.TotalRevenue.setText(f"₹{float(self.GrandTotalAmount):.2f}")
                self.TotalRevenue.setReadOnly(True)
                self.TotalRevenue.setStyleSheet("color:darkgreen")
            else:
                self.TotalRevenue.setText(f"₹{float(self.GrandTotalAmount):.2f}")
                self.TotalRevenue.setReadOnly(True)
                self.TotalRevenue.setStyleSheet("color:darkred")
        else:
            self.TotalRevenue.setText("₹0.00")
            self.TotalRevenue.setStyleSheet("")
