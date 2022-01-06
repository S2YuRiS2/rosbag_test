import subprocess
import time
import rosbag
import rospy
import yaml

test_bagfile = '/home/ros/ROS_Bag_test/bag_file/subset.bag'     #확인할 bag 파일 경로 입력
read_topic = '/usb_cam/image_raw/compressed'        #확인하고 싶은 토픽 정보 입력

class ROS_Bag():
    def __init__(self):
        print('init')
        rospy.init_node('ROS_bag',anonymous=True)
        self.bag_file = rosbag.Bag(test_bagfile)


    # bagfile의 특정 토픽의 토픽, 메시지, 시간 정보
    #read_messages topic 인자 값에 확인할 토픽을 입력하면 확인할 수 있음
    def play(self):
        for topic, msg, t in self.bag_file.read_messages(topics="/usb_cam/image_raw/compressed"):
            time.sleep(1)
            print("topic : ",topic)
            # print("msg : " ,msg)
            print("time : ",t)
            print()


    #bagfile duration, topic, messages 정보
    def bagfile_info(self):
        yaml.warnings({'YAMLLoadWarning': False})
        info_dict=yaml.load(subprocess.Popen(['rosbag','info','--yaml',test_bagfile],stdout=subprocess.PIPE).communicate()[0])

        duration = info_dict['duration']
        compressed_topic = info_dict['topics']
        compressed_message = compressed_topic[0].get('messages')
        self.rate = (compressed_message/duration)/1000

        print(duration)
        print(compressed_topic)
        print(compressed_message)


def main():
    r = ROS_Bag()

    #여기서 원하는 함수 주석 해제해서 확인하세요.
    r.play()
    # r.bagfile_info()

if __name__ == '__main__':
    main()





