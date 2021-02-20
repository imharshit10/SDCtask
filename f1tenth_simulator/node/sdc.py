#! /usr/bin/env python3
import rospy
import message_filters
import math
from time import sleep
from ackermann_msgs.msg import AckermannDriveStamped
from sensor_msgs.msg import LaserScan
from race.msg import pid_input


class test():

    def __init__(self):

            self.pub = rospy.Publisher('/drive', AckermannDriveStamped, queue_size=5)
            self.ADS = AckermannDriveStamped()
            self.v = 1
            self.kp = -0.5
            self.kd = -0.1
            self.c_error = 0
            self.p_error = 0
        
    def run(self):
            rospy.Subscriber('/scan', LaserScan, self.callback)
            rospy.spin()    

    def pid(self, ce, de):
            V = self.kp * ce + self.kd *(de) 
            return V     
        
    def getRange(self, data,theta):
        
        angle_increment  = data.angle_increment
        angle_increment *= 57.296 
    
        for i in data.ranges:
            if math.isnan(i) or math.isinf(i):
                 data.ranges = 20
    
        index = round(theta / angle_increment)
        return data.ranges[index]
    

    def callback(self, data):
        
        theta = 50
        l = self.getRange(data, 270)
        a = self.getRange(data,(90 + theta))        
        r = self.getRange(data,90)	
        rad = theta / 57.296

        alpha = math.atan( (a * math.cos(rad) - r)/ a * math.sin(rad) )
        AB = r * math.cos(alpha) 
        CD = AB + 1 * math.sin(alpha) 
        dist =  1.5  #(l+r)/2
        error = dist - CD 
        
        self.c_error = error
        de = self.c_error - self.p_error
        p = 0
        p = p - self.pid(self.c_error, de)
        self.p_error = self.c_error
        
        self.ADS.drive.steering_angle = p
        self.ADS.drive.speed = self.v
        self.pub.publish(self.ADS)


if __name__=='__main__':
    rospy.init_node('sdc', anonymous= True)
    car = test()
    car.run()
