#!/usr/bin/env python 

import rospy
import sys 
from geometry_msgs.msg import PoseStamped
from mavros_msgs.msg import State 
from mavros_msgs.srv import CommandBool, SetMode
from mavros_msgs.srv import *


current_state = State()


def FCU_callback(msg):

    global current_state 
    current_state = msg



rospy.init_node("offb_node",anonymous=True)
local_pos_pub = rospy.Publisher('/mavros/setpoint_position/local', PoseStamped, queue_size= 10)
state_sub = rospy.Subscriber('/mavros/state',State, FCU_callback)

'''variable = rospy.ServiceProxy(topic name, msg_type.topic)'''
arming_client = rospy.ServiceProxy('mavros/cmd/arming', mavros_msgs.srv.CommandBool)
set_mode_client = rospy.ServiceProxy('mavros/set_mode',mavros_msgs.srv.SetMode)


rate = rospy.Rate(20)

while not current_state.connected:
        print(current_state.connected)
        rate.sleep()


pose = PoseStamped()


pose.pose.position.z = 2

for i in range(100):
    local_pos_pub.publish(pose)
    rate.sleep()

offb_set_mode = SetMode()

offb_set_mode.custom_mode = "OFFBOARD"

arm_cmd = CommandBool()

arm_cmd.value = True

def offboard():
    offb = set_mode_client(0,offb_set_mode.custom_mode)
    if offb.mode_sent:
        print("offboard is enabled")
    last_request = rospy.Time.now()

def arming():
    arm = arming_client(arm_cmd.value)
    if arm.success:
        print("vechile is armed")
    last_request = rospy.Time.now()


last_request = rospy.Time.now()

while not rospy.is_shutdown():
    while(current_state.mode !="OFFBOARD" and (rospy.Time.now()-last_request > rospy.Duration(5))):
        offboard()

    while(not current_state.armed and(rospy.Time.now()-last_request>rospy.Duration(5))):
        arming()

    local_pos_pub.publish(pose)
    while (pose.pose.position.z > 1.5 and (rospy.get_rostime()-last_request > rospy.Duration(15))):
        pose.pose.position.z = 0
        print("Drone has reached its peak position and required time limit is satisfied")


        last_request = rospy.Time.now()

    local_pos_pub.publish(pose)


    while (pose.pose.position.z < 0.2 and (rospy.get_rostime()-last_request > rospy.Duration(5))):
        dis_arm()

rate.sleep()

if __name__ == '__main__':
    try:
        rospy.spin()
    except KeyboardInterrupt:
        print("shutting Down")

