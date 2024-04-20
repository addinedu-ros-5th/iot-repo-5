import sys
import mysql.connector
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5 import uic

from_class = uic.loadUiType("smart_farmer.ui")[0]

class WindowClass(QMainWindow, from_class) :
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.setWindowTitle("Smart Farmer")
        
        # Set Default Columns 
        self.cur,  self.remote = self.getCursor()
        names = self.getColNames()
        self.totalCol = len(names)

        for each in names:
            print(each[0])
            column_cnt = self.tableWidget.columnCount() # count total col <- index. 
            self.tableWidget.insertColumn(column_cnt)
            self.tableWidget.setHorizontalHeaderItem(column_cnt, QTableWidgetItem(each[0]))
       
        self.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)   

        # Set Default Columns 
        self.setDefaultRows()
        
       

        # 하나씩 추가로 row 추가 
        # a = self.tableWidget.rowCount()
        # self.tableWidget.insertRow(a)
    
    def setDefaultRows(self):
        self.cur.execute('SELECT count(*) from plant;')
        totalRow = self.cur.fetchall()[0][0]
        self.tableWidget.setRowCount(totalRow)

        self.cur.execute('SELECT * from plant;')
        allRows = self.cur.fetchall()
        
        for rowCnt in range (totalRow):

            rowTuple = allRows[rowCnt]
            print(rowTuple) # 4 Debugging. 

            for colCnt in range(self.totalCol):
                self.tableWidget.setItem(rowCnt, colCnt, QTableWidgetItem(f"{rowTuple[colCnt]}"))
        

    def getCursor(self):
        remote = mysql.connector.connect(
        host = "smart-farming-database.cb4y0k88ysov.ap-northeast-2.rds.amazonaws.com",
        #port = '3306',
        user = "admin",
        password = "Louis66411!",
        database = "smart_farming"
        )   
        cur = remote.cursor(buffered=True)
        return [cur, remote]

    
    def getColTotal(self):
        self.cur.execute("select COUNT(*) FROM information_schema.COLUMNS WHERE table_schema = 'smart_farming' AND table_name = 'plant';")
        result = self.cur.fetchall()
        totalCol = result[0][0] # [(6,),]

        return totalCol

    def getColNames(self):
        self.cur.execute("select COLUMN_NAME FROM information_schema.COLUMNS WHERE table_schema = 'smart_farming' AND table_name = 'plant';")
        col_names = self.cur.fetchall() # ex) [('온도',), ('습도')]
        return col_names

    def endConnection(self):
        self.remote.end()
        
  
if __name__ == "__main__":
    app = QApplication(sys.argv)
    myWindows = WindowClass()
    myWindows.show()

    sys.exit(app.exec_())

    cur.end()