import cv2
import rospy
import numpy as np

from sensor_msgs.msg import Image
from sensor_msgs.msg import CompressedImage
from cv_bridge import CvBridge
from PyQt5.QtWidgets import QWidget

class cvTest:
    def __init__(self):
        super(cvTest, self).__init__()
        print('init')
        rospy.init_node('rosbag_test',anonymous=True)
        self.bridge=CvBridge()
        self.sub_image="compressed"

        if self.sub_image == "compressed":
            self._sub = rospy.Subscriber("/usb_cam/image_raw/compressed",CompressedImage,self.callback)
            print("compressed")
        else:
            self._sub = rospy.Subscriber("/usb_cam/image_raw",Image,self.callback)
            print("raw")
        cv2.namedWindow("Image Window", 1)

    def show_image(self, img):
        cv2.imshow("Image Window",img)
        cv2.waitKey(1)

    def callback(self, img_msg):
        # rospy.loginfo(img_msg.header)
        # cv_image=bridge.imgmsg_to_cv2(img_msg,"bgr8")

        if self.sub_image == "compressed":
            np_arr = np.fromstring(img_msg,np.uint8)
            cv_image = cv2.imdecode(np_arr,cv2.COLOR_BGR2RGB)
        elif self.sub_image=="raw":
            cv_image=self.bridge.imgmsg_to_cv2(img_msg,"bgr8")

        self.show_image(cv_image)

    def run(self):
        while not rospy.is_shutdown():
            rospy.spin()
            
class App(QWidget):
    def __init__(self):
        super.__init__()
        self.title = "PyQT"
    

if __name__ =='__main__':
    cv = cvTest()


#
# while not rospy.is_shutdown():
#     rospy.spin()
