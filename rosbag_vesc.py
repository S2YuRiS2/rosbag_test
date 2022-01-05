import datetime
import subprocess
import rosbag
import yaml
from sensor_msgs.msg import Imu
from sensor_msgs.msg import PointCloud2
import rospy
import time

test_bagfile ='2021_07_25_ourdoor_centerpark_(camera, 3d_lidar, imu, vesc).bag'
read_topic = '/velodyne_points'
Directory_Path='/home/ros/ROS_Bag_test'

class ROS_Bag(object):
    def callback(self,imu_msg):
        print('callback')
        try:
            info_dict = yaml.load(subprocess.Popen(['rosbag', 'info', '--yaml', test_bagfile], stdout=subprocess.PIPE).communicate()[0])
            bag = rosbag.Bag(test_bagfile)

            # string= time.ctime(1631262083.6111205)
            # print(string)

            read_Bag = bag.read_messages(read_topic,start_time=rospy.Time.from_sec(1627018884))
            #read_Bag = bag.read_messages(read_topic)


            string = time.ctime(1627018674.650923729)
            print(string)
            #
            for topic, msg in enumerate(read_Bag):
                rospy.sleep(1)
                print('%d / %d'%(topic,info_dict['messages']))          #현재 몇 번째 메세지인지 출력
                # print(info_dict['messages'])


                # print("topic : ",topic)
                # print("msg : ",msg)
                #print("time", rospy.get_rostime())
                print("timestamp : ", imu_msg.header)

                # print("time : ",rospy.get_time(read_Bag))
                # print("bagtime : ",time.time())
                print()

        except Exception as e:
            print(e)

    def start(self):
        print('init')
        rospy.Subscriber('/velodyne_points', PointCloud2, self.callback)
        rospy.init_node('ROS_bag', anonymous=True)
        rospy.spin()
        exit()

if __name__=='__main__':
    rb=ROS_Bag()
    rb.start()
