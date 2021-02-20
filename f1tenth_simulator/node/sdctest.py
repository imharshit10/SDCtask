#! /usr/bin/env python3
import rospy
import math
from time import sleep
from ackermann_msgs.msg import AckermannDriveStamped
from sensor_msgs.msg import LaserScan
from race.msg import pid_input




pub = rospy.Publisher("/drive", AckermannDriveStamped, queue_size=10)




def callback():
	











if __name__=='__main__':
	print("Laser node started")
    	rospy.init_node('sdc', anonymous= True)
	rospy.Subscriber("scan",LaserScan,callback)
	rospy.spin()
    
    
