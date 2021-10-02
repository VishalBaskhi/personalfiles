#! /usr/bin/env/python
#!/bin/bash


import rospy 
from mavros_msgs.msg import State
import sys
from std_msgs.msg import String 

class FCU_state_monitor:
	

	def __init__(self):

		rospy.init_node('FCU_state_monitor)

		self.FCU_sub = rospy.Subscriber('/mavros/state' State, self.FCU_callback)

		self.FCU_status = "Initialising"


	def FCU_callback(self,msg)

		self.FCU_status = msg.mode
		print self.FCU_status

	#rospy.spin()

if __name__ == '__main__'

	try:
		FCU_state_monitor()

	except KeyboardInterrupt:
		print("shutting Down")

	

