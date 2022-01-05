import cv2
import numpy as np
import rosbag
import rospy
from sensor_msgs.msg import Image       #ROS Message
from sensor_msgs.msg import CompressedImage     #ROS Message
from cv_bridge import CvBridge,CvBridgeError

test_bagfile ='/home/ros/rosbag/subset.bag'
read_topic = '/usb_cam/image_raw/compressed'
# Directory_Path='/home/ros/ROS_Bag_test'
Directory_Path= '/home/ros/rosbag'

class ROS_Bag(object):
    def __init__(self):
        print('init')
        self.image=None
        self.selecting_sub_image="compressed"

        if self.selecting_sub_image == "compressed":
            self._sub=rospy.Subscriber('/usb_cam/image_raw/compressed',CompressedImage,self.callback,queue_size=1)
        else :
            self._sub=rospy.Subscriber('/usb_cam/image_raw',Image,self.callback,queue_size=1)
        self.bridge=CvBridge()

    def callback(self,img_msg):
        try:
            bag = rosbag.Bag(test_bagfile)
            read_Bag = bag.read_messages(read_topic)
            for topic, msg in enumerate(read_Bag):
                rospy.sleep(0.01)
                fmsg=CompressedImage()
                print('time : ',fmsg.header.stamp)
                print("topic : ",topic)
                print("msg : ",msg.timestamp)
                if self.selecting_sub_image=="compressed":
                    np_arr=np.fromstring(msg[1].data,np.uint8)
                    cv_image=cv2.imdecode(np_arr,cv2.COLOR_BGR2RGB)
                elif self.selecting_sub_image=="raw":
                    cv_image=self.bridge.imgmsg_to_cv2(msg[1],"bgr8")
                cv2.imshow('cv_img',cv_image)
                key = cv2.waitKey(1)

                if 113 == key:
                    print("q pressed. Abort")
                    break
            cv2.destroyAllWindows()
            bag.close()
            exit()

        except Exception as e:
            print(e)

    def start(self):
        rospy.spin()

if __name__=='__main__':
    try:
        rospy.init_node('ROS_bag',anonymous=True)
        rb=ROS_Bag()
        rb.start()
    except Exception as e:
        print(e)