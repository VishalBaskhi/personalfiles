#!/usr/bin/env python
import rospy
from geometry_msgs.msg  import Twist
from turtlesim.msg import Pose
from math import pow,atan2,sqrt
pi=3.14
angular_speed = 1.744


class turtlebot():
	def __init__(self):
    #Creating our node,publisher and subscriber
		rospy.init_node('turtlebot_controller', anonymous=True)
		self.velocity_publisher = rospy.Publisher('/turtle1/cmd_vel', Twist, queue_size=10)
		self.pose_subscriber = rospy.Subscriber('/turtle1/pose', Pose, self.callback)
		self.pose = Pose()
		self.rate = rospy.Rate(10)




	def callback(self,pose_data):
		self.pose = pose_data
		self.pose.x = round(self.pose.x, 2)
		self.pose.y = round(self.pose.y, 2)
	
		
		
	def goal(self):
		goal_pose= Pose()
		goal_pose.x = input("Set your x goal:")
		goal_pose.y = input("Set your y goal:")
		vel_msg = Twist()
		goal_angle = (atan2(goal_pose.y - self.pose.y, goal_pose.x - self.pose.x)-self.pose.theta)							
		vel_msg.angular.z = abs(angular_speed)
		

		if(self.pose.x > goal_pose.x):        #3  
			if(self.pose.y > goal_pose.y):
				vel_msg.angular.z = -abs(angular_speed)
				goal_angle = -goal_angle
		
				

		if(self.pose.x < goal_pose.x):   #4
			if(self.pose.y > goal_pose.y):
				vel_msg.angular.z = -abs(angular_speed)				
				goal_angle = -goal_angle
		
			
		
		current_angle = 0
		
		t0 = rospy.Time.now().to_sec()
		

		while (current_angle < goal_angle):
				
			self.velocity_publisher.publish(vel_msg) 								
			t1 = rospy.Time.now().to_sec()
			current_angle = angular_speed * ( t1 - t0)	
		vel_msg.angular.z = 0
		




		
		linear_speed = 10

		vel_msg.linear.x= abs(linear_speed)
		t1 = rospy.Time.now().to_sec()
		distance = sqrt(pow((goal_pose.x - self.pose.x), 2) + pow((goal_pose.y - self.pose.y), 2))
		current_distance = 0

		while( current_distance < distance):
			self.velocity_publisher.publish(vel_msg)
			t2 = rospy.Time.now().to_sec()
			current_distance = linear_speed * (t2-t1)
		vel_msg.linear.x = 0	
		self.velocity_publisher.publish(vel_msg)
	
			

		


if __name__ == '__main__':
	try:
        #Testing our function
		x = turtlebot()       
		x.goal()
        

	except rospy.ROSInterruptException: 
		pass