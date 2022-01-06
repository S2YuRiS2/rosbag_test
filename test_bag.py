import subprocess
import time
import rosbag
import rospy
import yaml

test_bagfile = '/home/ros/ROS_Bag_test/bag_file/subset.bag'     #확인할 bag 파일 경로 입력
read_topic = '/usb_cam/image_raw/compressed'        #확인하고 싶은 토픽 정보 입력

# start_secs = 500
# start_nsecs = 500
class ROS_Bag():
    def __init__(self):
        print('init')
        rospy.init_node('ROS_bag',anonymous=True)
        # self.bag_file = rosbag.Bag(test_bagfile)
        self.bag_file = rosbag.Bag(test_bagfile)
        self.start_secs_time = 0
        self.start_nsecs_time = 0
        self.time_change(500)


    # bagfile의 특정 토픽의 토픽, 메시지, 시간 정보
    # read_messages topic 인자 값에 확인할 토픽을 입력하면 확인할 수 있음
    def time_change(self, value):
        secs_list = []
        nsecs_list = []

        # self.start_secs_time = 0
        # self.start_nsecs_time = 0

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



    def play(self):
        # print(self.start_secs_time)
        # print(500)
        # global start_secs, start_nsecs
        count = 0

        # print(1)
        for topic, msg, t in self.bag_file.read_messages(start_time=rospy.Time(self.start_secs_time,self.start_nsecs_time)):
            time.sleep(1)
            # print("topic : ",topic)
            # print("msg : " ,msg)
            print("time : ",t.secs)
            print()
            count+=1
            print(count)
            # print(self.start_secs)
            if count == 5:
                print("change")
                # self.bag_file.close()
                self.time_change(1000)
                # self.bag_file = rosbag.Bag(test_bagfile)

                # print(self.start_secs_time)
                # print(1000)
                # self.start_secs = 1000
                # self.start_nsecs =1000
                # print()
                # print(self.start_secs)
                break


    #bagfile duration, topic, messages 정보
    def bagfile_info(self):
        yaml.warnings({'YAMLLoadWarning': False})
        info_dict=yaml.load(subprocess.Popen(['rosbag','info','--yaml',test_bagfile],stdout=subprocess.PIPE).communicate()[0])

        duration = info_dict['duration']
        compressed_topic = info_dict['topics']
        compressed_message = compressed_topic[0].get('messages')
        self.rate = (compressed_message/duration)/1000

        # print(duration)
        # print(compressed_topic)
        # print(compressed_message)


def main():
    r = ROS_Bag()

    #여기서 원하는 함수 주석 해제해서 확인하세요.
    while True:
        r.play()
    # r.bagfile_info()

if __name__ == '__main__':
    main()





