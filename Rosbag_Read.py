import subprocess, yaml
import rosbag
import rospy
from cv_bridge import CvBridge
from datetime import datetime
import cv2

# test_bag = 'cam_2021-07-14-14-12-25.bag'
# test_bag ='/home/ros/rosbag/subset.bag'
test_bag = 'cam_2021-07-14-14-12-25.bag'
read_topic = '/usb_cam/image_raw/compressed'
# read_topic = '/velodyne_points'
outputPath = '/home/ros/ROS_Bag_test'


if __name__ == '__main__':
	# info_dict = yaml.load(subprocess.Popen(['rosbag', 'info', '--yaml', test_bag], stdout=subprocess.PIPE).communicate()[0])

	bag = rosbag.Bag(test_bag)
	print(bag)

	#genBag = bag.read_messages(read_topic,start_time=rospy.Time.from_sec(1622614646))
	# genBag = bag.read_messages(read_topic)
	print("print:",read_topic)

	for topic, msg, t in genBag:
		rospy.sleep(0.01)
		# print("OK, %d / %d" % (k, info_dict['messages']))
		cb = CvBridge()
		# print('topic :',topic)
		# print('msg :',msg)
		# np_arr=np.fromstring(read_topic.data,np.uint8)
		# cv_image=cv2.imdecode(np_arr,cv2.COLOR_BGR2RGB)
		cv_image = cb.compressed_imgmsg_to_cv2(msg,"bgr8")
		print(datetime.fromtimestamp(t.secs))
		print()
		print(msg.header)
		# cv_image_r = cb.compressed_imgmsg_to_cv2(msg.message,"")

		# cv_image = cb.imgmsg_to_cv2(msg.message, msg.message.encoding )
		#
		# cv_image_r = cb.imgmsg_to_cv2(msg.message, "bgr8")
		cv2.imshow('cv_image', cv_image)
		key = cv2.waitKey(1)

		if 113 == key:
			print("q pressed. Abort.")
			break

	cv2.destroyAllWindows()

	bag.close()
# import rosbag
# from cv_bridge import CvBridge
# import cv2
#
# test_bag = 'cam_2021-07-14-14-12-25.bag'
# read_topic = '/usb_cam/image_raw'
# outputPath = '/home/ros/SADAT/SADAT/example/rosbag_test'
#
# if __name__ == '__main__':
#     bag=rosbag.Bag(test_bag)
#     read_Bag=bag.read_messages(read_topic)
#
#     while True :
#         for k, b in enumerate(read_Bag):
#             bridge = CvBridge()
#             cv_image = bridge.imgmsg_to_cv2(b.message,b.message.encoding)
#             cv_image_read=bridge.imgmsg_to_cv2(b.message,"bgr8")
#             cv2.imshow('topic',cv_image_read)
#             cv2.waitKey(100)
#             # key = cv2.waitKey()
#         if cv2.waitKey() == ord('q') or cv2.waitKey() == ord('Q'):
#             break
#
#     cv2.destroyAllWindows()
#     bag.close()