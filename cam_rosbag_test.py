import sys
import rospy
import cv2
import numpy as np
from cv_bridge import CvBridge, CvBridgeError
from sensor_msgs.msg import Image
from sensor_msgs.msg import CompressedImage
import time
from PyQt5.QtWidgets import  QWidget, QLabel, QApplication
from PyQt5.QtCore import QThread, Qt, pyqtSignal, pyqtSlot
from PyQt5.QtGui import QImage, QPixmap

cv_image=np.empty(shape=[0])
class cv_Test(QThread):
    signal=pyqtSignal(QImage)

    def __init__(self,qt):
        super(cv_Test,self).__init__(parent=qt)
        print('init')
        rospy.init_node('rosbag_test')
        rospy.Subscriber('/usb_cam/image_raw', Image, self.callback, queue_size=1)
        self.bridge=CvBridge()

    def callback(self,data):
        global cv_image
        cv_image=self.bridge.imgmsg_to_cv2(data,"bgr8")

        cv2.imshow("test",cv_image)
        cv2.waitKey(1)

        # h, w, ch = cv_image.shape
        # bytesPerLine = ch * w
        # convertToQtFormat = QImage(cv_image.data, w, h, cv_image.strides[0], QImage.Format_RGB888)
        # p = convertToQtFormat.scaled(640, 480, Qt.KeepAspectRatio)
        # self.signal.emit(convertToQtFormat)

    def run(self):
        rospy.spin()

class App(QWidget):
    def __init__(self):
        super().__init__()
        self.title = 'PyQt5 Video'
        self.left = 100
        self.top = 100
        self.width = 1920
        self.height = 1080
        self.initUI()

    @pyqtSlot(QImage)
    def setImage(self, image):
        self.label.setPixmap(QPixmap.fromImage(image))

    def initUI(self):

        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        self.resize(2000, 1100)
        # create a label
        self.label = QLabel(self)
        self.label.resize(1920, 1080)

        # self.show()
        time.sleep(1)
        th = cv_Test(self)
        th.signal.connect(self.setImage)
        # th.changePixmap.connect(self.setImage)
        th.start()

if __name__ == '__main__':
    # cv = Cv_test()
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())

# class Cv_test():
#     def __init__(self):
#         print('init')
#         rospy.init_node('rosbag_test')
#         rospy.Subscriber('/usb_cam/image_raw/', Image, self.callback, queue_size=1)
#         self.bridge = CvBridge()
#
#     def callback(self,data):
#         cv_image=self.bridge.imgmsg_to_cv2(data,"bgr8")
#
#         while not rospy.is_shutdown():
#             if cv_image.size!=(640*480*3):
#                 continue
#             cv2.imshow("test", cv_image)
#             cv2.waitKey(1)
#
#         # h, w, ch = cv_image.shape
#         # bytesPerLine = ch * w
#         # convertToQtFormat = QImage(cv_image.data, w, h, cv_image.strides[0], QImage.Format_RGB888)
#         # p = convertToQtFormat.scaled(640, 480, Qt.KeepAspectRatio)
#         # self.signal.emit(convertToQtFormat)
#
# if __name__ == '__main__':
#     cv = Cv_test()
#     # app = QApplication(sys.argv)
#     # ex = App()
#     # sys.exit(app.exec_())




# import cv2
# import rospy
# import numpy as np
#
# from sensor_msgs.msg import Image
# from cv_bridge import CvBridge
#
# cv_image=np.empty(shape=[0])
#
# class cv_Test:
#     def __init__(self):
#         rospy.init_node('cam',anonymous=True)
#         rospy.Subscriber("/usb_cam/image/raw",Image,self.callback)
#         while not rospy.is_shutdown():
#             if cv_image.size!=(640*480*3):
#                 continue
#             cv2.imshow("test",cv_image)
#             cv2.waitKey(1)
#
#     def callback(self,data):
#         global cv_image
#         bridge=CvBridge()
#         self.cv_image=bridge.imgmsg_to_cv2(data,"bgr8")
#
# if __name__ == '__main__':
#     cv=cv_Test()
