import subprocess
import threading
import time
import rosbag
import rospy
import cv2
import yaml
from cv_bridge import CvBridge, CvBridgeError
from threading import Thread
import queue

test_bagfile ='/home/ros/rosbag/bag_file/subset.bag'
read_topic = '/usb_cam/image_raw/compressed'
Directory_Path= '/home/ros/rosbag'

# bag_start_time = 0
lock = threading.Lock()
class ROS_Bag():
    # bag_start_time = 0

    def __init__(self):
        print('init')
        rospy.init_node('ROS_bag',anonymous=True)
        self.bag_file = rosbag.Bag(test_bagfile)
        self.bag_start_time = 0
        self.update_time(self.bag_start_time)
        # self.input_time()

    # def input_time(self):
    #     # lock.acquire()
    #     # self.bag_start_time = (int(input("time input : ")))
    #     # return bag_start_time
    #     while True:
    #         self.bag_start_time = (int(input("time input : ")))
    #         t = threading.Thread(target=self.update_time, args=(self.bag_start_time,))
    #         t.start()
    #         t.join()
    #     # self.update_time(self.bag_start_time)
    #     # lock.release()



    def update_time(self, time):
        self.bag_start_time = time

        # print(bag_start_time)
        # lock.acquire()
        self.time_change(self.bag_start_time)
        # lock.release()
        # self.time_change(time)

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
                print(self.start_secs_time)
        for i in self.nsecs_dict.keys():
            if int(value) == i:
                self.start_nsecs_time = int(self.nsecs_dict[i])
                print(self.start_nsecs_time)

        self.bagfile_time(self.start_secs_time,self.start_nsecs_time)

    def bagfile_time(self, secs, nsecs):
        # print('start')
        self.frame_rate()
        self.bridge = CvBridge()
        self.read_bagfile = self.bag_file.read_messages(read_topic, start_time=rospy.Time(secs,nsecs))
        self.play()

    def play(self):
        # print('start')
        # lock.acquire()
        for topic, msg, t in self.read_bagfile:
            time.sleep(self.rate)
            cv_image = self.bridge.compressed_imgmsg_to_cv2(msg, "bgr8")
            cv2.imshow('cv_img', cv_image)

            key = cv2.waitKey(1)
            if key == 27:
                self.bag_close()
                break
        # lock.release()

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

def main():
    time = int(input("입력 : "))
if __name__ == '__main__':
    r = ROS_Bag()

    # time = int(input("입력 : "))
    #
    # # num = int(time)
    # t = threading.Thread(target=r.update_time,args=(time,))
    # t.start()


    # while True:
    #     t1 = Thread(target=r.input_time)
    #     t2 = Thread(target=r.play)
    #     # t2 = Thread(target=r.bagfile_time)
    #     t1.start()
    #     t2.start()
    #     t1.join()
    #     # t2.join()







