#!/usr/bin/env python
import rospy
from geometry_msgs.msg import Twist
PI= 3.14
    
def hod ():
       # Starts a new node
       rospy.init_node('robot_cleaner', anonymous=True)
       velocity_publisher = rospy.Publisher('/turtle1/cmd_vel', Twist, queue_size=10)
       vel_msg = Twist()
 
       #Receiveing the user's input
       print("Let's rotate your robot")
       aspeed = input("Input your aspeed:")
       angle = input("Type your angle:")
       clockwise = input("clockwise?: ")#True or False
       distance = input("type your distance: ")
       linearspeed = input("input your lspeed:") 
       isForward = input("forward?: ")
              
       angular_speed = aspeed*2*PI/360
       relative = angle*2*PI/360

       #Checking if the movement is forward or backwards
       if clockwise:
           
	    vel_msg.angular.z = -abs(angular_speed)
	    
       else:
            vel_msg.angular.z = abs(angular_speed)
       
            	    
       #Since we are moving just in x-axis
       
      
      
       
  
       while not rospy.is_shutdown():
   
           #Setting the current time for distance calculus
           t0 = rospy.Time.now().to_sec()

           current_angle = 0
	   
           while(current_angle < relative):
	       velocity_publisher.publish(vel_msg)
               #Takes actual time to velocity calculus
               t1=rospy.Time.now().to_sec()
               #Calculates distancePoseStamped
               current_angle= angular_speed*(t1-t0)    
	   vel_msg.angular.z = 0
	   
	   
	   if(isForward):
	       vel_msg.linear.x = abs(linearspeed) 
       
           else:
	       vel_msg.linear.x = -abs(linearspeed)
	   while not rospy.is_shutdown():
   
               
               
	       t1=rospy.Time.now().to_sec()
		


	       current_distance = 0    #loop to move the bot in forward or backward direction
	       while(current_distance < distance):
	           #publish the velocity
                   velocity_publisher.publish(vel_msg)
	           #Takes actual time to velocity calculus
	           t2=rospy.Time.now().to_sec()
                   current_distance=linearspeed*(t2-t1)
               vel_msg.linear.x = 0

           #velocity_publisher.publish(vel_msg)
	   
if __name__ == '__main__':
       try:
           #Testing our function
           hod()
       except rospy.ROSInterruptException: pass

   
            
