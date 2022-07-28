import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QPixmap, QColor, QPainter
from PyQt5.QtWidgets import QLabel, QApplication


class Stack():
    def __init__(self) -> None:
        self.data = []
    
    def push(self, value):
        self.data.append(value)
    
    def pop(self):
        if len(self.data) == 0:
            return
        return self.data.pop()


class Canvas(QLabel):
    def __init__(self,height, width, background_color=QColor('#FFFFFF')):
        super().__init__()
        qpixmap = QPixmap(int(height), int(width))
        qpixmap.fill(background_color)
        self.setPixmap(qpixmap)
        self.pen_color = QColor('#000000')
        self.undoStack = Stack()
        self.redoStack = Stack()
        self.line = []

    def set_pen_color(self, color):
        self.pen_color = QtGui.QColor(color)

    def draw_point(self, x, y):
        painter = QPainter(self.pixmap())
        p = painter.pen()
        p.setWidth(4)
        p.setColor(self.pen_color)
        painter.setPen(p)
        painter.drawPoint(x, y)
        painter.end()
        self.update()


    def draw_line(self, x0, y0, x1, y1):
        painter = QPainter(self.pixmap())
        p = painter.pen()
        p.setWidth(4)
        p.setColor(self.pen_color)
        painter.setPen(p)
        painter.drawLine(x0, y0, x1, y1)
        painter.end()
        self.update()


    def mousePressEvent(self, e: QtGui.QMouseEvent):
        self.draw_point(e.x(), e.y())
        self.prev_point = (e.x(), e.y())
        self.line.append(self.prev_point)

    def mouseMoveEvent(self, e):
        self.draw_line(self.prev_point[0], self.prev_point[1], e.x(), e.y())
        self.prev_point = (e.x(), e.y())
        self.line.append(self.prev_point)

    def mouseReleaseEvent(self, e):
        self.prev_point = tuple()
        self.undoStack.push(self.line)
        self.line = []

    def undoFunction(self):
        linePoints = self.undoStack.pop()
        if not linePoints:
            return
        self.pen_color = QColor('#FFFFFF')
        for point in linePoints:
            index = linePoints.index(point)
            if index == 0:
                self.draw_point(point[0], point[1])
            else:
                self.draw_line(linePoints[index - 1][0], linePoints[index - 1][1], point[0], point[1])
        self.pen_color = QColor('#000000')
        self.redoStack.push(linePoints)
    
    def redoFunction(self):
        linePoints = self.redoStack.pop()
        if not linePoints:
            return
        self.pen_color = QColor('#000000')
        for point in linePoints:
            index = linePoints.index(point)
            if index == 0:
                self.draw_point(point[0], point[1])
            else:
                self.draw_line(linePoints[index - 1][0], linePoints[index - 1][1], point[0], point[1])
        self.pen_color = QColor('#FFFFFF')
        self.undoStack.push(linePoints)

class PaletteButton(QtWidgets.QPushButton):

    def __init__(self, color):
        super().__init__()
        self.setFixedSize(QtCore.QSize(32, 32))
        self.color = color
        self.setStyleSheet("background-color: %s;" % color + "border-radius : 15; ")


class MainWindow(QtWidgets.QMainWindow):

    def __init__(self):
        super().__init__()
        self.colors = [
            '#000002', '#868687', '#900124', '#ed2832', '#2db153', '#13a5e7', '#4951cf',
            '#fdb0ce', '#fdca0f', '#eee3ab', '#9fdde8', '#7a96c2', '#cbc2ec', '#a42f3b',
            '#f45b7a', '#c24998', '#81588d', '#bcb0c2', '#dbcfc2',
        ]
        app = QApplication.instance()
        screen = app.primaryScreen()
        geometry = screen.availableGeometry()
        self.canvas = Canvas(geometry.width()*0.60, geometry.height()*0.7)
        w = QtWidgets.QWidget()
        w.setStyleSheet("background-color: #313234")
        l = QtWidgets.QVBoxLayout()  # vertical layout
        w.setLayout(l)
        l.addWidget(self.canvas)

        palette = QtWidgets.QHBoxLayout()  # horizontal layout
        self.add_palette_button(palette)
        l.addLayout(palette)

        self.setCentralWidget(w)


    def add_palette_button(self, palette):
        for c in self.colors:
            item = PaletteButton(c)
            item.pressed.connect(self.set_canvas_color)
            palette.addWidget(item)

    def set_canvas_color(self):
        sender = self.sender()
        self.canvas.set_pen_color(sender.color)

    def keyPressEvent(self, event: QtGui.QKeyEvent) -> None:
        if(event.key() == 90):
            self.canvas.undoFunction()
        
        if(event.key() == 89):
            self.canvas.redoFunction()


app = QtWidgets.QApplication(sys.argv)
window = MainWindow()
window.setWindowFlags(QtCore.Qt.WindowCloseButtonHint | QtCore.Qt.WindowMinimizeButtonHint)
window.show()
app.exec_()

# Window dimensions