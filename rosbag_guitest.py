import sys
import rospy
import cv2
import numpy as np
import rosbag
from datetime import datetime
from cv_bridge import CvBridge, CvBridgeError
from sensor_msgs.msg import Image
from sensor_msgs.msg import CompressedImage
import time
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

test_bagfile ='/home/ros/rosbag/subset.bag'
read_topic = '/usb_cam/image_raw/compressed'
Directory_Path= '/home/ros/rosbag'
class Time_CONTROLLER :
    def __init__(self):
        self.slider = None

    def addSlider(self,item):
        self.slider = item

    def setSlider(self,index):
        self.slider.setValue(index)

    def getSlider(self):
        return self.slider
class cvThread(QThread):
    signal = pyqtSignal(QImage)

    def __init__(self, qt):
        super(cvThread, self).__init__(parent=qt)
        print('init')
        rospy.init_node('ROS_bag', anonymous=True)
        self.bridge = CvBridge()
        self.bag = rosbag.Bag(test_bagfile)
        bag_start_time = int(input("time input : "))
        self.read_Bag = self.bag.read_messages(read_topic, start_time=rospy.Time.from_sec(bag_start_time))
        print(datetime.fromtimestamp(1622614646))  # 타임스탬프 값
        print('init finished')

    def start(self):
        try :
            self.msg_time = []
            for topic, msg, t in self.read_Bag:
                rospy.sleep(0.02)
                self.msg_time.append(msg.header.stamp.secs)
                # print(msg.header)  # 메시지 헤더, 헤더의 경우 대부분의 메시지 자료형에 포함되어 있음
                # cb = CvBridge()
                # print("seq:", msg.header.seq)

                # print("seq : ", msg.header.seq)  # 메시지 헤더 구성 요소들 (seq, stamp, frame_id)
                # print("stamp : ", msg.header.stamp.secs)  #
                # print("frame_id : ", msg.header.frame_id)  #

                # print(msg) # 메시지 포맷, 각 메시지 별 출력가능한 내용은 검색을 통해 확인하도록
                # print(t) # 시간 값, secs(초), nsecs(나노초)로 나뉘어진다
                # print(datetime.fromtimestamp(t.secs))  # 타임스탬프 값
                # print()
                cv_image = self.bridge.compressed_imgmsg_to_cv2(msg, "bgr8")
                cv2.imshow('cv_img', cv_image)
                key = cv2.waitKey(1)
                if 113 == key:
                    print("q pressed")
                    break
            print("s : ", self.msg_time)

            # h, w, ch = cv_image.shape
            # bytesPerLine = ch * w
            # convertToQtFormat = QImage(cv_image.data, w, h, cv_image.strides[0], QImage.Format_RGB888)
            # p = convertToQtFormat.scaled(640, 480, Qt.KeepAspectRatio)
            # self.signal.emit(convertToQtFormat)

            cv2.destroyAllWindows()
            self.bag.close()




        except Exception as e:
            print(e)

        return self.msg_time

    def run(self):
        rospy.spin()

class App(QWidget):
    def __init__(self, parent):
        super(App,self).__init__(parent)
        self.pr = parent

        # self.title = 'PyQt5 Video'
        # self.left = 100
        # self.top = 100
        # self.width = 100
        # self.height = 100
        self.initUI()

    def initUI(self):
        p = self.palette()
        p.setColor(self.backgroundRole(),Qt.black)
        self.pr.setPalette(p)
        self.show()


class MyApp(QMainWindow):
    def __init__(self,parent=None):
        super(MyApp,self).__init__(parent)
        self.initUI()

    @pyqtSlot(QImage)
    def setImage(self, image):
        self.label.setPixmap(QPixmap.fromImage(image))

    def initUI(self):
        self.setWindowTitle('ROSbag_test')
        display_monitor = 0
        monitor = QDesktopWidget().screenGeometry(display_monitor)
        self.setGeometry(300, 300, 1500, 1000)
        self.move(monitor.left() + 300, monitor.top() + 300)
        self.initToolbar()

        # self.slider = QSlider(Qt.Horizontal, self)
        # self.slider.move(30, 30)
        # self.slider.setRange(0, 50)
        # self.slider.setSingleStep(1)

        # self.slider.valueChanged.connect(self.dial)

        # self.setWindowTitle(self.title)
        # self.setGeometry(self.left, self.top, self.width, self.height)
        # self.resize(1000, 1000)
        # create a label
        # self.label = QLabel(self)
        # self.label.resize(1000, 1080)

        self.show()
        # time.sleep(1)
        th = cvThread(self)
        th.signal.connect(self.setImage)
        # th.changePixmap.connect(self.setImage)
        th.start()

    def initToolbar(self):
        self.toolbar = self.addToolBar('d')
        slider = QSlider(Qt.Horizontal, self)
        slider.sliderMoved.connect(self.sliderMoved)

    def sliderMoved(self):
        self.start.msg_time


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyApp()
    sys.exit(app.exec_())