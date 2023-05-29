from PyQt5 import QtWidgets, QtSvg
from PyQt5.QtCore import Qt
from PyQt5.QtSvg import QSvgWidget
from PyQt5.QtWidgets import QApplication, QMainWindow, QToolTip, QPushButton, QWidget, QDesktopWidget, QLabel, \
    QStackedLayout
import sys
from PyQt5.QtGui import QIcon, QFont, QPixmap, QPainter, QPen, QColor, QBrush
import json
from random import randint
import parse
from PyQt5.uic.properties import QtCore, QtGui
from numpy import size


from Station import *


class Metro(QWidget):

    def __init__(self):
        super().__init__()
        self.__k = 1
        self.__path = []
        self.__stations = {}
        self.__way = [0, 0]
        self.__colt = 0
        self.__ids = {}
        self.initUI()

    def initUI(self):

        self.resize(1600, 900)
        self.center()
        self.setWindowTitle('Metro')
        self.setWindowIcon(QIcon('img/metro.svg'))


        self.__data = self.reader()

        for crd in self.__data['Points']:
            button = QPushButton(str(crd['point']['id']), self)
            button.setGeometry(12, 8, 6, 6)
            # setting radius and border
            button.setStyleSheet(f"""border-radius : 3; border: 2px solid {crd['point']['color']}""")
            button.clicked.connect(self.onClicked)
            button.move(int(crd['point']['x']) // 3 * self.__k, int(crd['point']['y']) // 3 * self.__k)

        button1 = QPushButton(str(crd['point']['id']), self)
        button1.setGeometry(1, 1, 20, 20)
        button.clicked.connect(self.reset)



        self.show()

    def reset(self):
        p = parse.Parser('index.html')
        p.parse()
        p.save('flats.json')

    def onClicked(self):
        sender = self.sender().text()
        self.__way[self.__colt] = int(sender)
        self.__colt = 1 if self.__colt == 0 else 0
        print(self.__way)
        if (self.__way[0] != 0 and self.__way[1] != 0) and self.__way[0] != self.__way[1]:
            #self.matrix()
            x1 = self.__stations[self.__way[0]].get_x()
            y1 = self.__stations[self.__way[0]].get_y()
            x2 = self.__stations[self.__way[1]].get_x()
            y2 = self.__stations[self.__way[1]].get_y()
            print(f'<line stroke="#000000" stroke-width="8" x1="{x1}" x2="{x2}" y1="{y1}" y2="{y2}" stroke-linecap="butt" fill="none"></line>')
            self.dejkstra()
            self.update()




    def dejkstra(self):
        self.__path = []
        frontier = []
        start = self.__way[0]
        frontier.append([start, 0])
        goal = self.__way[1]
        came_from = {}
        cost_so_far = {}
        came_from[start] = None
        cost_so_far[start] = 0

        while not len(frontier) == 0:
            current = frontier[0]
            #print(current)
            frontier.pop(0)

            #if current[0] == goal:
                #print('нихуя себе')
                #break

            #print(self.__stations[current[0]].get_ways())
            for nt in self.__stations[current[0]].get_ways():
                new_cost = cost_so_far[current[0]] + randint(60, 180)
                if nt not in cost_so_far or new_cost < cost_so_far[nt]:
                    cost_so_far[nt] = new_cost
                    priority = new_cost
                    frontier.append([nt, priority])
                    came_from[nt] = current[0]

        #print('egor ivlev')

        n = came_from[goal]
        self.__path.append(goal)
        while n != None:
            self.__path.append(n)
            n = came_from[n]
        #print(self.__path)
        self.__way = [0,0]

    def matrix(self):
        for i in self.__stations.items():
            print(f'id: {i[1].get_id()}')
            print(f'true_id: {i[1].get_true_id()}')
            for j in i[1].get_ways():
                print(j)
            print('\n')
            # print(i[1].get_id(),i[1].get_ways())


    def paintEvent(self, e):
        qp = QPainter(self)
        qp.begin(self)
        pixmap = QPixmap("graph.svg")
        pixmap = pixmap.scaledToWidth(1165 * self.__k)
        qp.drawPixmap(-81, -81, pixmap)
        # lbl = QLabel(self)
        # lbl.move(-81, -81)
        # lbl.setPixmap(pixmap)
        self.drawLines(qp)
        qp.end()

    def drawLines(self, qp):
        pen = QPen(Qt.black, 4, Qt.SolidLine)
        qp.setPen(pen)
        if len(self.__path) > 0:
            for i in range(len(self.__path[:-1])):
                s1 = self.__stations[self.__path[i]]
                s2 = self.__stations[self.__path[i+1]]
                #print(self.__stations[self.__path[i]])
                x1 = s1.get_x()
                y1 = s1.get_y()
                x2 = s2.get_x()
                y2 = s2.get_y()
                qp.drawLine(x1//3 * self.__k + 3,y1//3 * self.__k + 1,x2//3 * self.__k + 3,y2//3 * self.__k + 1)
        # qp.drawLine(20, 40, randint(100,400), randint(100,400))
        # for i in self.__stations.items():
        #     ways = i[1].get_ways()
        #     #print(ways)
        #     for j in ways:
        #         #print(j)
        #         qp.drawLine(i[1].get_x()//3 + 3, i[1].get_y()//3 + 1, self.__stations[j].get_x()//3 + 3, self.__stations[j].get_y()//3 + 1)
        #         # print(i[1].get_x(), i[1].get_y(), self.__stations[j].get_x(), self.__stations[j].get_y())

    def reader(self):
        data = []
        self.__stations = {}
        with open('flats.json', "r", encoding='utf8') as read_file:
            data = json.load(read_file)
        for i in data['Points']:
            self.__stations[int(i['point']['id'])] = Station(int(i['point']['id']), int(i['point']['true_id']), int(i['point']['x']), int(i['point']['y']), i['point']['color'])
            self.__ids[int(i['point']['id'])] = int(i['point']['true_id'])
        for i in data['Ways']:
            try:
                fr = int(i['way']['from'])
                to = int(i['way']['to'])
                if fr in self.__stations and to in self.__stations:
                    self.__stations[fr].add_way(to)
                    self.__stations[to].add_way(fr)
            except:
                pass
        return data

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Metro()
    sys.exit(app.exec_())
