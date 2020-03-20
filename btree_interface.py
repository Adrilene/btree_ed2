from PyQt5.QtWidgets import QLabel, QMainWindow, QApplication, QWidget, QVBoxLayout, QPushButton, QHBoxLayout
from PyQt5.QtGui import QPixmap, QPainter, QBrush, QPen, QColor, QFont
from PyQt5.QtCore import Qt
from PyQt5 import QtGui
import threading
import sys
import json
from time import sleep
    

class Window(QMainWindow):
    def __init__(self):
        super().__init__()
        self.title = "B Tree"
        self.top = 1000
        self.left = 1000
        self.width = 2000
        self.height = 2000
        self.data = []
        self.button = False
        self.start_thread = False
        self.m = None
        self.situation = None
        self.InitWindow()

    def button_pressed_start(self):
        self.button = True

    def qtd_pages_for_level(self, level, pages):
        temp = []
        for page in pages:
            if page[2] == level:
                temp.append(page)
        
        return len(temp)

    def paintEvent(self, event):
        if self.situation:
            painter = self.situation
        else:
            painter = QPainter(self)
            painter.setPen(QPen(Qt.darkBlue,  2, Qt.SolidLine))
        
        pages = self.data[0].split(';')
        pages.pop()
        self.m = int(pages.pop(0)) * 2
        
        for i in range(len(pages)):
            pages[i] = eval(pages[i])

        levels = set()
        for i in pages:
            levels.add(i[2])

        all_pages = []
        for level in levels:
            temp = []
            for i in pages:
                if i[2] == level:
                    temp.append(i)
                
                if i == pages[-1]:
                    temp.sort()
                    for a in temp:
                        all_pages.append(a)
        
        pages = all_pages

        max_values = self.m
        lenght_square = 25 * max_values
        height_square = 60
        height_number = height_square + 30

        square_position_x = 580
        square_position_y = 100
        circle_position_x = square_position_x
        circle_position_y = square_position_y + 45
        number_position_x = square_position_x
        number_position_y = square_position_y + 25

        past = pages[0][0]   
        i = 0
        for page in pages:
            current = page[-1]
            qtd_page_level = self.qtd_pages_for_level(current, pages)
            qtd_page_level = qtd_page_level / 2
            # Pages
            painter.setBrush(QBrush(Qt.white, Qt.SolidPattern))
            if i == 0:
                # Desenha a primeira página
                painter.drawRect(square_position_x, square_position_y, lenght_square, height_square)
                circle_position_x = square_position_x
                circle_position_y = square_position_y + height_square - 15
                number_position_x = square_position_x
                number_position_y = square_position_y + height_square - 35    
            elif past != current:
                i = 1
                painter.drawRect(square_position_x - (lenght_square*qtd_page_level) + lenght_square/2, square_position_y + int(page[-1]) * square_position_y, lenght_square, height_square)
                circle_position_x = square_position_x - (lenght_square*qtd_page_level) + lenght_square/2
                circle_position_y =  square_position_y + page[-1] * square_position_y + height_square - 15
                number_position_x = square_position_x - (lenght_square*qtd_page_level) + lenght_square/2
                number_position_y = square_position_y + page[-1] * square_position_y + height_square - 15
                past = current
            else:
                painter.drawRect(square_position_x - (lenght_square*qtd_page_level) + (i-1)*lenght_square  + lenght_square/2, square_position_y + int(page[-1]) * square_position_y, lenght_square, height_square)
                circle_position_x = square_position_x - (lenght_square*qtd_page_level) + (i-1)*lenght_square + lenght_square/2 + 8
                circle_position_y = square_position_y + page[-1] * square_position_y + height_square - 15
                number_position_x = square_position_x - (lenght_square*qtd_page_level) + (i-1)*lenght_square + lenght_square/2 + 8
                number_position_y = square_position_y + page[-1] * square_position_y + height_square - 15
            
            positions_circles = list()
            
            for number_of_point in range(max_values + 1):
                spaces_beetwen_circle = (lenght_square/max_values) - 5
                if number_of_point == 0:
                    painter.drawEllipse(circle_position_x + (number_of_point*spaces_beetwen_circle) + 3, circle_position_y, 8, 8)
                    positions_circles.append((circle_position_x + (number_of_point*spaces_beetwen_circle), circle_position_y))
                else:
                    painter.drawEllipse(circle_position_x + (number_of_point*spaces_beetwen_circle), circle_position_y, 8, 8)
                    positions_circles.append((circle_position_x + (number_of_point*spaces_beetwen_circle), circle_position_y))
            
            positions_numbers = []

            space_beetwen_number = (lenght_square/max_values) - 5
            j = 0

            for number in page[1]:
                if i == 0:
                    painter.drawText(number_position_x + (j*space_beetwen_number) + 10, number_position_y, str(number))
                    painter.drawText(number_position_x, number_position_y - 30, str(page[0]))
                    positions_numbers.append((number_position_x + 30, number_position_y))
                    j += 1
                else:
                    painter.drawText(number_position_x + (j*space_beetwen_number) + 10, number_position_y - 15, str(number))
                    painter.drawText(number_position_x, number_position_y - 50, str(page[0]))
                    positions_numbers.append((number_position_x + (i*space_beetwen_number) + 30, number_position_y))
                    j += 1

            j = 0
            i += 1
    

    def InitWindow(self):
        self.setGeometry(self.top, self.left, self.width, self.height)
        # Define title device
        self.titleDevice = QLabel(self)
        self.titleDevice.setText('<strong>B Tree<\strong>')
        self.titleDevice.setFont(QtGui.QFont('Arial', 12))
        self.titleDevice.adjustSize()
        self.titleDevice.move(30, 10)

        datas = open('data_to_interface.txt', encoding='utf8')
        for data in datas:
            self.data.append(data.replace('\n', ''))

        self.show()

def execute_interface():
    app = QApplication(sys.argv)
    ex = Window()
    sys.exit(app.exec_())