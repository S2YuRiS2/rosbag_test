import rosbag
import rospy
from sensor_msgs.msg import CompressedImage
from turtlesim.msg import Pose
# from geometry_msgs.msg import Twist

bag = rosbag.Bag('test_1.bag','w')

def recorder():
    rospy.init_node('Image',anonymous=True)
    rospy.Subscriber('usb_cam/image_raw/compressed',CompressedImage,callback)
    rospy.spin()
    bag.close()

def callback(data):
    bag.write('usb_cam/image_raw/compressed',data)

if __name__=='__main__':
    try:
        recorder()
    except rospy.ROSInterruptException:
        pass