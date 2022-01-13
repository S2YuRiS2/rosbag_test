import subprocess
import threading
import time
import rosbag
import rospy
import cv2
import yaml
from cv_bridge import CvBridge
from threading import Thread

test_bagfile ='/home/ros/ROS_Bag_test/bag_file/subset.bag'
read_topic = '/usb_cam/image_raw/compressed'

lock = threading.Lock()

class ROS_Bag():
    def __init__(self):
        print('init')
        rospy.init_node('ROS_bag', anonymous=True)
        self.bag_file = rosbag.Bag(test_bagfile)
        self.bridge = CvBridge()
        self.start_secs_time = 0
        self.start_nsecs_time = 0
        self.t = 0
        self.list1 = [0]
        self.flag = False

    def input_time(self):
        print("start")
        while True:
            self.t = int(input("\n입력 : "))
            self.list1.append(self.t)
            print("list print ", self.list1)

            if self.list1[0] != self.list1[-1]:
                self.flag = True
                print('list index not true')

    def time_change(self, value):
        secs_list = []
        nsecs_list = []

        for topic, msg, t in self.bag_file.read_messages(read_topic):
            secs_list.append(msg.header.stamp.secs)
            nsecs_list.append(msg.header.stamp.nsecs)
        self.secs_dict = dict(zip(range(len(secs_list)), secs_list))
        self.nsecs_dict = dict(zip(range(len(nsecs_list)), nsecs_list))

        self.start_secs_time = self.secs_dict[value]
        self.start_nsecs_time = self.nsecs_dict[value]

    def play(self):
        self.frame_rate()
        while True :
            for topic, msg, t in self.bag_file.read_messages(read_topic, start_time=rospy.Time(self.start_secs_time, self.start_nsecs_time)):
                cv_image = self.bridge.compressed_imgmsg_to_cv2(msg, "bgr8")
                cv2.imshow('cv_img', cv_image)
                time.sleep(self.rate)
                key = cv2.waitKey(1)

                if self.flag == True:
                    print("success")
                    self.time_change(self.list1[-1])
                    self.flag = False
                    if self.flag == False:
                        del self.list1[-1]
                    break

                if key == 27:
                    self.bag_close()
                    break

    def bag_close(self):
        self.bag_file.close()
        cv2.destroyAllWindows()

    def frame_rate(self):
        yaml.warnings({'YAMLLoadWarning': False})
        info_dict=yaml.load(subprocess.Popen(['rosbag','info','--yaml',test_bagfile],stdout=subprocess.PIPE).communicate()[0])

        duration = info_dict['duration']
        compressed_topic = info_dict['topics']
        compressed_message = compressed_topic[0].get('messages')
        self.rate = (compressed_message/duration)/1000



if __name__ == '__main__':
    r = ROS_Bag()

    t1 = Thread(target=r.input_time)
    t2 = Thread(target=r.play)
    t1.start()
    t2.start()
