from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import sys, random, math, time
# from stereo import Stereo
from sonic import Sonic

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
        self.sonic = Sonic()
        # self.car = Car()
        # self.stereo = Stereo(30)

    def GUI(self):
        self.setGeometry(0, 0, 600, 600)
        self.setStyleSheet("QWidget {background-color:black;}")
        self.show()

    def setTimer(self):
        self._status_update_timer = QTimer(self)
        self._status_update_timer.setSingleShot(False)
        self._status_update_timer.timeout.connect(self._update_points)
        self._status_update_timer.start(200)

    def _update_points(self):
        # angles = random.randint(1, 360)
        # depth = random.randint(1, 150)
        # angle = angles * math.pi / 180
        # x, y = self.origin[0] + depth * math.cos(angle), self.origin[1] + depth * math.sin(angle)
        # x, y = self.origin[0] + depth * math.cos(angle), self.origin[1] + depth * math.sin(angle)
        # xs, ys = self.stereo.stereo_map(self.orientation, self.origin[0], self.origin[1])
        # self.pts = [(x, y) for x, y in zip(xs, ys)]
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
        average = 0
        count = 0
        for i in range(100):
            val = self.sonic.measure()
            if val > 1000:
                continue
            average += val
            count += 1
        if count > 0:
            depth = average / count 
            for j in range(5):
                theta = (self.orientation -2 + j) * math.pi / 180
                x, y = self.origin[0] + depth * math.cos(theta), self.origin[1] + depth * math.sin(theta)
                self.pts.append((x,y))
        self.update()
        event.accept()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    canvas = Canvas()
    sys.exit(app.exec_())
