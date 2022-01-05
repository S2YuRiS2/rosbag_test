import subprocess
import threading
import time
import rosbag
import rospy
import cv2
import yaml
from cv_bridge import CvBridge, CvBridgeError
from threading import Thread
import multiprocessing
from multiprocessing import freeze_support


test_bagfile = '/home/ros/ROS_Bag_test/bag_file/subset.bag'
read_topic = '/usb_cam/image_raw/compressed'
Directory_Path= '/home/ros/rosbag'

lock = threading.Lock()
class ROS_Bag():
    def __init__(self):
        print('init')
        rospy.init_node('ROS_bag',anonymous=True)
        self.bag_file = rosbag.Bag(test_bagfile)
        self.running = True
        self.threads = []
        self.read_bagfile = self.bag_file
        self.rate = 0
        self.bridge = CvBridge()
        self.secs = 0
        self.nsecs = 0
        # self.bag_start_time = 0
        # self.update_time(self.bag_start_time)
        # self.input_time()

    # def go(self):
    #     t1 = threading.Thread(target=self.play)
    #     t2 = threading.Thread(target=self.input_time)
    #     t1.daemon = True
    #     t2.daemon = True
    #     t1.start()
    #     t2.start()
    #     self.threads.append(t1)
    #     self.threads.append(t2)

    def input_time(self):
        self.bag_start_time = (int(input("time input : ")))

        self.update_time(self.bag_start_time)
        # lock.release()

    def update_time(self, time):

        self.bag_start_time = time
        self.time_change(self.bag_start_time)
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
                # print(self.start_secs_time)
        for i in self.nsecs_dict.keys():
            if int(value) == i:
                self.start_nsecs_time = int(self.nsecs_dict[i])
                # print(self.start_nsecs_time)

        return self.start_secs_time, self.start_nsecs_time
        # self.bagfile_time(self.start_secs_time,self.start_nsecs_time)

    # def bagfile_time(self, secs, nsecs):
    #     # print('start')
    #     # self.frame_rate()
    #     self.read_bagfile = self.bag_file.read_messages(read_topic, start_time=rospy.Time(secs,nsecs))
    #     self.play(self.read_bagfile)

    def play(self, secs,nsecs):
        self.secs = secs
        self.nsecs = nsecs
        # while(self.running):
        self.frame_rate()
        while True:
            for topic, msg, t in self.bag_file.read_messages(read_topic, start_time=rospy.Time(secs, nsecs)):
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

# def join_threads(threads):
#     for t in threads:
#         while t.is_alive():
#             t.join(5)
#             # print(t)


def main():
    r = ROS_Bag()
    process =[]
    while True:
        i = input("입력 : ")
        # (v1,v2) = r.time_change(i)
        # r.play(v1,v2)
        if i == 'q':
            break

        elif i.isdigit():
            (v1, v2) = r.time_change(i)
            t1 = multiprocessing.Process(target=r.play, args=(v1, v2))
            # t1.daemon=True
            t1.start()
            process.append(t1)
        # for t1 in process:
            # t1.terminate()




if __name__ == '__main__':
    main()





