import cv2
import rospy
import numpy as np

from sensor_msgs.msg import Image, CompressedImage
from cv_bridge import CvBridge

rospy.init_node('rosbag_test',anonymous=True)
bridge=CvBridge()
sub_image="cFompressed"

def show_image(img):
    cv2.imshow("Image Window",img)
    cv2.waitKey(1)

def callback(img_msg):

    if sub_image=="compressed":
        np_arr = np.fromstring(img_msg.data, np.uint8)
        cv_image = cv2.imdecode(np_arr, cv2.COLOR_BGR2RGB)
    elif sub_image=="raw":
        cv_image=bridge.imgmsg_to_cv2(img_msg,"bgr8")
    show_image(cv_image)

if sub_image=="compressed":
    rospy.Subscriber("/usb_cam/image_raw/compressed",CompressedImage,callback)
elif sub_image=="raw":
    rospy.Subscriber("/usb_cam/image_raw",Image,callback)
    print("raw")
cv2.namedWindow("Image Window",1)

while not rospy.is_shutdown():
    rospy.spin()


