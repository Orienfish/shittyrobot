from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import sys, random, math, time
from car import Car

class Canvas(QWidget):

    robot_size = 8 
    pts = []
    origins = [] # past origins
    orientation = -90
    theta = 0
    vector_length = 30
    blink = True
    scale = 100 # 1m <-> 100pt
    
    def __init__(self):
        super().__init__()
        self.GUI()
        self.origin = [self.width() / 2, self.height() / 2]
        self.origins.append((self.origin[0], self.origin[1]))
        self.setTimer()
        self.car = Car()

    def GUI(self):
        self.setGeometry(0, 0, 600, 600)
        self.setStyleSheet("QWidget {background-color:black;}")
        self.show()

    def setTimer(self):
        self._status_update_timer = QTimer(self)
        self._status_update_timer.setSingleShot(False)
        # self._status_update_timer.timeout.connect(self._update_points)
        self._status_update_timer.start(500)

    def _update_points(self):
        angles = random.randint(1, 360)
        depth = random.randint(1, 150)
        angle = angles * math.pi / 180
        # x, y = self.origin[0] + depth * math.cos(angle), self.origin[1] + depth * math.sin(angle)
        x, y = self.origin[0] + depth * math.cos(angle), self.origin[1] + depth * math.sin(angle)
        self.pts.append((x, y))
        self.update()
        print("point added")

    def orientation_to_radian_theta(self):
        '''
        convert orientation - the direction in canvas to  theta - the direction of robot
        '''
        return (self.orientation + 90) * math.pi / 180.0

    '''
    the point should be generated using two input variables:
    input: 
        - depth, orientation
    output:
        - a 2D point from the robot origin
    '''
    def paintEvent(self, e):
        qp = QPainter()
        qp.begin(self)
        self._drawRobotOrientation(e, qp)
        self._drawRobotOrigin(e, qp)
        self._drawPastOrigins(e, qp)
        if self.blink:
            self._drawDepthFields(e, qp)
        qp.end()


    def _drawRobotOrientation(self, e, qp):
        qp.setPen(Qt.red)
        x, y = self.width() // 2, self.height() // 2
        radian_basis = (self.orientation) * math.pi / 180
        end_x = x + self.vector_length * math.cos(radian_basis) 
        end_y = y + self.vector_length * math.sin(radian_basis)
        qp.drawLine(x, y, end_x, end_y)

    def _drawDepthFields(self, e, qp):
        pen = QPen()
        pen.setColor(Qt.white)
        pen.setWidth(3)
        qp.setPen(pen)
        for x, y in self.pts:
            qp.drawPoint(x - self.origin[0] + self.width() / 2, y - self.origin[1] + self.height() / 2)

    def _drawPastOrigins(self, e, qp):
        pen = QPen()
        pen.setColor(Qt.green)
        pen.setWidth(1)
        qp.setPen(pen)
        # print(self.origins)
        for i in range(0, len(self.origins)-1):
            x, y = self.origins[i]
            x_next, y_next = self.origins[i+1]
            qp.drawPoint(x - self.origin[0] + self.width() / 2, y - self.origin[1] + self.height() / 2)
            qp.drawLine(x - self.origin[0] + self.width() / 2, y - self.origin[1] + self.height() / 2, \
                x_next - self.origin[0] + self.width() / 2, y_next - self.origin[1] + self.height() / 2)
        
    def _drawRobotOrigin(self, e, qp):
        qp.setBrush(Qt.red)
        x, y = self.width() // 2, self.height() // 2
        qp.drawEllipse(x - self.robot_size // 2, y - self.robot_size // 2, self.robot_size, self.robot_size)
        qp.drawPoint(x, y)

    def keyPressEvent(self, event):
        theta = self.orientation_to_radian_theta()
        if event.key() == Qt.Key_Q:
            print('Killing')
            self.deleteLater()
        elif event.key() == Qt.Key_Up:
            # going up
            dx, dy, angle = self.car.Move(self.car.FORWARD)
            self.origin[0] += dx * math.sin(theta) * self.scale
            # self.origin[0] += -dy * math.cos(theta) * self.scale
            self.origin[1] += -dx * math.cos(theta) * self.scale
            # self.origin[1] += -dy * math.sin(theta) * self.scale
            self.orientation -= angle
            print("going forward")
            print("dx:", dx, "dy:", dy, "dangle:", angle)
            print("origin:", self.origin[0], self.origin[1], dx * math.sin(theta) * self.scale, -dx * math.cos(theta) * self.scale)
            print("theta:", theta)
        elif event.key() == Qt.Key_Down:
            # going down
            dx, dy, angle = self.car.Move(self.car.BACKWARD)
            self.origin[0] += dx * math.sin(theta) * self.scale
            # self.origin[0] += -dy * math.cos(theta) * self.scale
            self.origin[1] += -dx * math.cos(theta) * self.scale
            # self.origin[1] += -dy * math.sin(theta) * self.scale
            self.orientation -= angle
            print("going backward")
            print("dx:", dx, "dy:", dy, "dangle:", angle)            
            print("origin:", self.origin[0], self.origin[1], dx * math.sin(theta) * self.scale, -dx * math.cos(theta) * self.scale)
            print("theta:", theta)
        elif event.key() == Qt.Key_Left:
            # turn left
            dx, dy, angle = self.car.Move(self.car.LEFT)
            self.orientation -= angle
            
        elif event.key() == Qt.Key_Right:
            # turn right
            dx, dy, angle = self.car.Move(self.car.RIGHT)
            self.orientation -= angle
            
        self.origins.append((self.origin[0], self.origin[1]))
        self.update()
        event.accept()

    def proceed(self):
        print("Key_Enter")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    canvas = Canvas()
    sys.exit(app.exec_())
