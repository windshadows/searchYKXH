# -*- coding: UTF-8 -*-

from PyQt5.QtWidgets import QWidget,QApplication,QHeaderView,\
    QTableWidgetItem,QMessageBox,QAbstractItemView
import sys
import os
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
from Search import Ui_Form



areadict={"嘉兴地调":"./fes/fes_send_yx_chan_0484.txt",
          "海宁":"./fes/fes_send_yx_chan_0630.txt",
          "海盐":"./fes_send_yx_chan_0726.txt",
          "平湖":"./fes/fes_send_yx_chan_0678.txt",
          "桐乡":"./fes_send_yx_chan_0679.txt",
          "嘉善":"./fes_send_yx_chan_0737.txt"}



class mWidget(QWidget,Ui_Form):
    def __init__(self):
        super(mWidget,self).__init__()
        self.YXList=[]
        self.arealist=["全部","嘉兴地调","海宁","海盐","平湖","桐乡","嘉善"]
        self.areadict = {"嘉兴地调": "./fes/fes_send_yx_chan_0484.txt",
                    "海宁": "./fes/fes_send_yx_chan_0630.txt",
                    "海盐": "./fes/fes_send_yx_chan_0726.txt",
                    "平湖": "./fes/fes_send_yx_chan_0678.txt",
                    "桐乡": "./fes/fes_send_yx_chan_0679.txt",
                    "嘉善": "./fes/fes_send_yx_chan_0737.txt"}
        self.initUi()
        self.FreshYXList()
        self.showTableWidget(self.comboBox.currentText())
        self.setWindowIcon(QIcon("./img/e.ico"))
        self.setFixedSize(self.width(), self.height())

    def initUi(self):
        self.setupUi(self)
        self.setWindowTitle("查询AVC遥控序号")
        self.comboBox.addItems(self.arealist)

        #信号连接槽
        self.pushButton_2.clicked.connect(self.close)
        self.comboBox.currentIndexChanged.connect(self.My_comboBox_currentIndexChanged)
        self.tableWidget.horizontalHeader().sectionClicked.connect(self.sortByColumn)
        self.tableWidget.horizontalHeader().sectionDoubleClicked.connect(self.sortByColumn2)
        self.toolButton_2.clicked.connect(self.SearchYKXH)
        self.toolButton.clicked.connect(lambda :self.showTableWidget(self.comboBox.currentText()))
        self.pushButton.clicked.connect(self.chachong)


    #定义槽函数
    #on_comboBox_currentIndexChanged
    def My_comboBox_currentIndexChanged(self,i):
        self.showTableWidget(self.comboBox.currentText())

    def sortByColumn(self,i):
        self.tableWidget.sortByColumn(i,Qt.AscendingOrder)

    def sortByColumn2(self,i):
        self.tableWidget.sortByColumn(i,Qt.DescendingOrder)

    def initTableWidget(self):
        self.tableWidget.clear()
        self.tableWidget.setColumnCount(5)
        self.tableWidget.setRowCount(0)
        self.tableWidget.setHorizontalHeaderLabels(['设备ID', '厂站名', '遥控名称', '转发序号', '区域'])
        self.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        #self.tableWidget.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.tableWidget.setSelectionBehavior(QAbstractItemView.SelectRows)



    def FreshYXList(self):
        self.YXList = []
        for i in self.areadict:
            self.LoadFromFile(i)

    def LoadFromFile(self,areaName):
        filepath=self.areadict.get(areaName)
        if os.path.exists(filepath):
            with open(filepath,'r') as f:
                templist=[]
                text_lines = f.readlines()
                filterlist=["电抗器开关","电抗器中性点开关","电容器开关","升","降"]
                for line in text_lines:
                    for x in filterlist:
                        if x in line:
                            str=line.strip()
                            data=str.split()
                            data[5]=int(data[5])
                            data.append(areaName)
                            if len(data[3])<13 \
                                    and data[4]=="遥信值" \
                                    and data[1]=="20"\
                                    and ("小车" not in data[3]) \
                                    and ("线开关" not in data[3]) \
                                    and ("闸刀" not in data[3]):
                                templist.append(data)
                            break

                for i in templist:
                    self.YXList.append(i)

        #Tablewidget中展示
    def showTableWidget(self,areaName):
        self.initTableWidget()
        if areaName == "全部":
            self.tableWidget.setRowCount(len(self.YXList))
            n=0
            for i in self.YXList:
                Item0 = QTableWidgetItem(i[0])
                Item1 = QTableWidgetItem(i[2])
                Item2 = QTableWidgetItem(i[3])
                Item3 = QTableWidgetItem()
                Item3.setData(Qt.DisplayRole,int(i[5]))
                Item4 = QTableWidgetItem(i[6])
                self.tableWidget.setItem(n, 0,Item0)
                self.tableWidget.setItem(n, 1, Item1)
                self.tableWidget.setItem(n, 2, Item2)
                self.tableWidget.setItem(n, 3, Item3)
                self.tableWidget.setItem(n, 4, Item4)
                n += 1

        else:
            n = 0
            for i in self.YXList:
                if i[6]==areaName:
                    self.tableWidget.setRowCount(n+1)
                    Item0 = QTableWidgetItem(i[0])
                    Item1 = QTableWidgetItem(i[2])
                    Item2 = QTableWidgetItem(i[3])
                    Item3 = QTableWidgetItem()
                    Item3.setData(Qt.DisplayRole, int(i[5]))
                    Item4 = QTableWidgetItem(i[6])
                    self.tableWidget.setItem(n, 0, Item0)
                    self.tableWidget.setItem(n, 1, Item1)
                    self.tableWidget.setItem(n, 2, Item2)
                    self.tableWidget.setItem(n, 3, Item3)
                    self.tableWidget.setItem(n, 4, Item4)
                    n += 1

    def SearchYKXH(self):

        text = self.lineEdit.text()
        items = self.tableWidget.findItems(text, Qt.MatchExactly)
        if len(items)>0:
            templist=[]
            for item in items:
                row = item.row()
                data = []

                data.append(self.tableWidget.item(row, 0).text())
                data.append(self.tableWidget.item(row, 1).text())
                data.append(self.tableWidget.item(row, 2).text())
                data.append(self.tableWidget.item(row, 3).text())
                data.append(self.tableWidget.item(row, 4).text())
                templist.append(data)

            self.initTableWidget()
            n = 0
            for i in templist:
                self.tableWidget.setRowCount(n + 1)
                Item0 = QTableWidgetItem(i[0])
                Item1 = QTableWidgetItem(i[1])
                Item2 = QTableWidgetItem(i[2])
                Item3 = QTableWidgetItem()
                Item3.setData(Qt.DisplayRole, int(i[3]))
                Item4 = QTableWidgetItem(i[4])
                self.tableWidget.setItem(n, 0, Item0)
                self.tableWidget.setItem(n, 1, Item1)
                self.tableWidget.setItem(n, 2, Item2)
                self.tableWidget.setItem(n, 3, Item3)
                self.tableWidget.setItem(n, 4, Item4)
                n += 1


            #self.tableWidget.verticalScrollBar().setSliderPosition(row)
        else:
            res = QMessageBox.information(self,'信息提示','没有找到匹配的序号！',
                                          QMessageBox.Yes|QMessageBox.No)
    #只在YXList里面查重
    def chachong(self):
        self.YXList.sort(key=lambda x:x[5])
        templist=[]
        for i in range(len(self.YXList)):
            for j in range(i+1,len(self.YXList)):
                if self.YXList[i][5]==self.YXList[j][5]:
                    if self.YXList[i] not in templist:
                        templist.append(self.YXList[i])
                    if self.YXList[j] not in templist:
                        templist.append(self.YXList[j])

        if len(templist)>0:
            self.initTableWidget()
            n = 0
            for i in templist:
                self.tableWidget.setRowCount(n + 1)
                Item0 = QTableWidgetItem(i[0])
                Item1 = QTableWidgetItem(i[2])
                Item2 = QTableWidgetItem(i[3])
                Item3 = QTableWidgetItem()
                Item3.setData(Qt.DisplayRole,int(i[5]))
                Item4 = QTableWidgetItem(i[6])
                self.tableWidget.setItem(n, 0,Item0)
                self.tableWidget.setItem(n, 1, Item1)
                self.tableWidget.setItem(n, 2, Item2)
                self.tableWidget.setItem(n, 3, Item3)
                self.tableWidget.setItem(n, 4, Item4)
                n += 1



if __name__=="__main__":
    app = QApplication(sys.argv)
    w=mWidget()
    w.show()
    sys.exit(app.exec())