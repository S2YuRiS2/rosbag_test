import subprocess
import threading
import time
import rosbag
import rospy
import cv2
import yaml
from cv_bridge import CvBridge
from threading import Thread
import multiprocessing

test_bagfile ='/home/ros/ROS_Bag_test/bag_file/subset.bag'
read_topic = '/usb_cam/image_raw/compressed'

lock = threading.Lock()
class ROS_Bag():
    def __init__(self):
        print('init')
        rospy.init_node('ROS_bag', anonymous=True)
        self.bag_file = rosbag.Bag(test_bagfile)
        self.running = True
        self.threads = []
        self.read_bagfile = self.bag_file
        self.bridge = CvBridge()
        self.rate = 0
        self.secs = 0
        self.nsecs = 0

    def input_time(self):
        t = int(input("\n입력 : \n"))
        self.time_change(t)

    def time_change(self, value):
        secs_list = []
        nsecs_list = []

        self.start_secs_time = 0
        self.start_nsecs_time = 0

        for topic, msg, t in self.bag_file.read_messages(read_topic):
            secs_list.append(msg.header.stamp.secs)
            nsecs_list.append(msg.header.stamp.nsecs)
        self.secs_dict = dict(zip(range(len(secs_list)), secs_list))
        self.nsecs_dict = dict(zip(range(len(nsecs_list)), nsecs_list))

        for i in self.secs_dict.keys():
            if int(value) == i:
                self.start_secs_time = int(self.secs_dict[i])
                # print(self.start_secs_time)
        for i in self.nsecs_dict.keys():
            if int(value) == i:
                self.start_nsecs_time = int(self.nsecs_dict[i])
                # print(self.start_nsecs_time)

        self.bagfile_time(self.start_secs_time, self.start_nsecs_time)

    def bagfile_time(self,secs, nsecs):
        self.read_bagfile = self.bag_file.read_messages(read_topic, start_time=rospy.Time(secs, nsecs))
        self.play()

    def play(self):
        self.frame_rate()

        for topic, msg, t in self.read_bagfile:
            time.sleep(self.rate)
            cv_image = self.bridge.compressed_imgmsg_to_cv2(msg, "bgr8")
            cv2.imshow('cv_img', cv_image)
            key = cv2.waitKey(1)

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

    while True :
        # r.input_time()
        t1 = multiprocessing.Process(target=r.input_time)
        # t2 = Thread(target=r.play)
        # t1.daemon = True
        t1.start()
        time.sleep(5)

        # t1.join()
        # t2.start()