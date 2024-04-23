import sys
import mysql.connector
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5 import uic
from PyQt5.uic import loadUi

from PyQt5.QtCore import *
import serial
import time

import serial
import struct

from_class = uic.loadUiType("smart_farmer.ui")[0]

class Receiver(QThread):
    detected = pyqtSignal(str)

    def __init__(self,connector,parent=None): #?
        super(Receiver, self).__init__(parent) #?

        self.is_running = False
        self.connector = connector

    def run(self):
        self.is_running = True
        while(self.is_running == True):
            if self.connector.readable():
                response = self.connector.read_until('\n').decode().strip('\r\n') #?
                if (len(response) > 0):
                    #print(response)
                    self.detected.emit(response)

    def stop(self):
        print("receiving stop")
        self.is_running = False 

class DialogClass(QDialog): #?``
    def __init__(self,  parent=None): #? parent
        super().__init__(parent) 
        loadUi("dialog.ui", self)
        #---------------------------------------------------------------------
        #UE
        self.parentWindow = self.parent() #?  
        self.addBtn.clicked.connect(self.addRow) #? 왜여기서만 clicked 확인 가능?


    def addRow(self):
        userInputs = [self.nameLe.text(), self.tempLe.text(), self.humLe.text(), self.redLe.text(),
                      self.blueLe.text(), self.moistLe.text()]
                      
        colCnt = self.parentWindow.totalCol
        rowCnt = self.parentWindow.tableWidget.rowCount()
        self.parentWindow.tableWidget.insertRow(rowCnt)

        for each in range(colCnt):
            self.parentWindow.tableWidget.setItem(rowCnt, each, QTableWidgetItem(f"{userInputs[each]}"))
        # ------------------------------------------------------------------------------------------------
        colNames = self.parentWindow.names 
        cur, remote = self.parentWindow.getCursor()
        cur.execute(f"""INSERT INTO plant  ({colNames[0][0]},{colNames[1][0]}, {colNames[2][0]}, {colNames[3][0]}, 
                {colNames[4][0]}, {colNames[5][0]}) 
                VALUES ('{userInputs[0]}','{userInputs[1]}', '{userInputs[2]}','{userInputs[3]}',
                '{userInputs[4]}', '{userInputs[5]}') """ )
        remote.commit()

        # print(f"""INSERT INTO plant  ({colNames[0][0]},{colNames[1][0]}, {colNames[2][0]}, {colNames[3][0]}, 
        #         {colNames[4][0]}, {colNames[5][0]}) 
        #         VALUES ('{userInputs[0]}','{userInputs[1]}', '{userInputs[2]}','{userInputs[3]}',
        #         '{userInputs[4]}', '{userInputs[5]}') """ ) <- DEBUGGING
        
        
class WindowClass(QMainWindow, from_class) :
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.setWindowTitle("Smart Farmer")

        self.cur,  self.remote = self.getCursor() #DB
        self.clicked_name = ""
        
        self.connector = self.connect() #Arduino

        # for monitoring
        self.bestTemp = ""
        self.bestHum = ""
        self.moist = ""

        self.receiver = Receiver(self.connector)
        self.receiver.detected.connect(self.getStatus)
        self.receiver.start()

        self.endBtn.hide()

        #---------------------------------------------------------------------
        # Set Default Columns 
        
        self.names = self.getColNames()
        self.totalCol = len(self.names)
        
        for each in self.names:
            column_cnt = self.tableWidget.columnCount() # count total col <- index. 
            self.tableWidget.insertColumn(column_cnt)
            self.tableWidget.setHorizontalHeaderItem(column_cnt, QTableWidgetItem(each[0]))
       
        self.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)   

        #-------------------------------------------------------------------------------------------- 
        #Set Default Rows 
        self.setDefaultRows()
        self.tableWidget.setSelectionBehavior(QAbstractItemView.SelectRows) #?
        self.tableWidget.setSelectionMode(QAbstractItemView.SingleSelection) #?
        #-------------------------------------------------------------------------------------------- 
        # User Event
        self.tableWidget.cellClicked.connect(self.cellClicked)
        self.deleteBtn.clicked.connect(self.deletRow)
        self.addBtn.clicked.connect(self.addRow)
        self.applyBtn.clicked.connect(self.setRequest)
        self.endBtn.clicked.connect(self.stopOperation)
    
    def stopOperation(self):
        self.connector.write("N".encode())#?
    
    def getStatus(self, response):  #?     
        # *** For some reason Some of the first responses were like S1 (line changed) N00F00N90NO. Thus, index out of range error
        if (len(response) == 13 and response[2] == 'Y'):  # Operating
            print(response)
            self.tempNow.setText("현재 온도 : " + response[3:5])
            self.tempGoal.setText("목표치 : " + self.bestTemp)
            if(response[5] == 'C'): self.tempWork.setText("쿨러 작동중!")
            elif(response[5] == 'H'): self.tempWork.setText("히터 작동중!")
            else: self.tempWork.setText("")
            
            self.tempWork.setStyleSheet("""
            QLabel {
            background-color: red;
            border: 4px solid black;
            border-radius: 10px;
            }
            """)
            self.tempWork.show()
            self.tempWork.setAlignment(Qt.AlignCenter)

            #Humidity
            self.humNow.setText("현재 습도 : " + response[6:8])
            self.humGoal.setText("목표치 : " + self.bestHum)
            if(response[8] == 'Y'): self.humWork.setText("가습기 작동중!") 
            else : self.humWork.setText("")

            self.humWork.show()
            #Moisture
            self.moistNow.setText("현재 수분 : " + response[9:11])
            self.moistGoal.setText("목표치 : " + self.bestMoist)
            if(response[11] == 'Y'): self.moistWork.setText("물 공급중!")
            else : self.moistWork.setText("")

            self.moistWork.show()
            #LED
            self.redRate.setText(response[12])
            self.redLabel.show()
            self.blueLabel.show()
            self.redRate.show()
            self.colonLabel.show()
            self.blueRate.show()

            #End
            self.endBtn.show()
        elif(len(response) == 13 and response[2] == 'N'): # Not Operating 
            print(response)
            self.tempNow.setText("현재 온도 : " + response[3:5])
            self.tempGoal.setText("온도조절 장치 미작동중")
            self.tempWork.hide()

            self.humNow.setText("현재 습도 : " + response[6:8])
            self.humGoal.setText("습도조절 장치 미작동중")
            self.humWork.hide()

            self.moistNow.setText("현재 수분 : " + response[9:11])
            self.moistGoal.setText("수분공급 장치 미작동중")
            self.moistWork.hide()

            self.ledLabel.setText("LED 미작동중")
            self.redLabel.hide()
            self.blueLabel.hide()
            self.redRate.hide()
            self.colonLabel.hide()
            self.blueRate.hide()

            self.endBtn.hide()

    def temp(self):
        selected_items = self.tableWidget.selectedItems()
        print(selected_items[2].text(), selected_items[3].text(), selected_items[6].text(), selected_items[4].text())


    def setRequest(self):
        selected_items = self.tableWidget.selectedItems()
        request = "Y"
        request = request + selected_items[1].text() + selected_items[2].text() + selected_items[5].text() + selected_items[3].text()
        print("*******" + request)
        self.connector.write(request.encode())#?

        self.bestTemp = selected_items[1].text()
        self.bestHum = selected_items[2].text()
        self.bestMoist = selected_items[1].text()


    def addRow(self):
        self.dialog = DialogClass(self) #?
        #dialog.setWindowModality(Qt.ApplicationModal)
        self.dialog.exec()


    def deletRow(self):
        retVal = self.askBeforeDel()
        if (retVal == QMessageBox.No) : return
        else :      
            selected_items = self.tableWidget.selectedItems() #?
            if(selected_items):
                self.cur.execute(f"DELETE FROM plant WHERE name = '{selected_items[0].text()}';")
                self.remote.commit()
                #----------------------------------------------------------------    
                row_indx = self.tableWidget.row(selected_items[1])
                print(selected_items[0].text() + " deleted")
                self.tableWidget.removeRow(row_indx)
       

    def cellClicked(self, row, col):
        print("Clicked row:", row, "Clicked column:", col)
        cell_item = self.tableWidget.item(row,0)

        self.clicked_name = cell_item.text()
        
        self.cur.execute(f"SELECT * from plant WHERE name = '{self.clicked_name}'")
        selected_row = self.cur.fetchall()
        print(selected_row)
        
    def setDefaultRows(self):
        self.cur.execute('SELECT count(*) from plant;')
        totalRow = self.cur.fetchall()[0][0]
        self.tableWidget.setRowCount(totalRow) # There is a checkbox ell in each row. so +1

        self.cur.execute('SELECT * from plant;')
        allRows = self.cur.fetchall()
        
        for rowCnt in range (totalRow):

            rowTuple = allRows[rowCnt]
            print(rowTuple) # 4 Debugging. 

            for colCnt in range(self.totalCol): # Again, need to consider the first cell of a row. it's fixed.
                cell = QTableWidgetItem(f"{rowTuple[colCnt]}")
                #cell.setFlags(cell.flags() & ~Qt.ItemIsEnabled) 
                self.tableWidget.setItem(rowCnt, colCnt, cell) # tuple index - 0 ~ 5 but column indx 1 ~ 6

        
    # item = MyQTableWidgetItemCheckBox()
        
    # self.table.setItem(idx, 0, item)

    def getCursor(self):
        remote = mysql.connector.connect(
        host = "smart-farming-database.cb4y0k88ysov.ap-northeast-2.rds.amazonaws.com",
        #port = '3306',
        user = "user1",
        password = "1234",
        database = "smart_farming"
        )   
        cur = remote.cursor(buffered=True)
        return [cur, remote]

    
    def getColTotal(self):
        self.cur.execute("select COUNT(*) FROM information_schema.COLUMNS WHERE table_schema = 'smart_farming' AND table_name = 'plant';")
        result = self.cur.fetchall()
        totalCol = result[0][0] # [(6,),]

        return totalCol

    def getColNames(self): #? 칼럼 정렬
        self.cur.execute("select COLUMN_NAME FROM information_schema.COLUMNS WHERE table_schema = 'smart_farming' AND table_name = 'plant' ORDER BY ORDINAL_POSITION;") 
        col_names = self.cur.fetchall() # ex) [('온도',), ('습도')]
        return col_names

    def endConnection(self):
        self.remote.end()
    
    def askBeforeDel(self):
        retVal = QMessageBox.question(self, 'Warning Before Deletion', '해당 행을 삭제 하시겠습니까?', 
                                      QMessageBox.Yes | QMessageBox.No , QMessageBox.No)
        return retVal

    def connect(self): #?
        conn = serial.Serial(port = "/dev/ttyACM0", baudrate=9600, timeout=1)
        return conn
    
    def detected(self, recv):
        print(recv)

        return
  
if __name__ == "__main__":
    app = QApplication(sys.argv)
    myWindows = WindowClass()
    myWindows.show()
    sys.exit(app.exec_())
    myWindows.endConnection() #?