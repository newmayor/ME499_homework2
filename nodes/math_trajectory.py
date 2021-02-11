#!/usr/bin/env python3

##############################
## NOTES ##

##############################
import rospy
from std_msgs.msg import String
from geometry_msgs.msg import Twist, Vector3
import math
from math import cos, sin, tan, atan, pi, sqrt
from turtlesim.srv import TeleportAbsolute
import sys

T = 15 
#T = input("How fast should Mr.Happy Turtle run?")

#get turtle located and oriented correctly for t=0
# def orient_turtle():
rospy.wait_for_service('turtle1/teleport_absolute')
turtle1_teleport_absolute = rospy.ServiceProxy('turtle1/teleport_absolute', TeleportAbsolute)
resp1 = turtle1_teleport_absolute(5.54, 5.54, 0.0)
	
def get_vel(t):

	
	v_x = 12*pi*cos(4*pi*t/T)/T
	v_y = 6*pi*cos(2*pi*t/T)/T

	a_x = (-48*pi**2*sin(4*pi*t/T))/T**2
	a_y = (-12*pi**2*sin(2*pi*t/T))/T**2
	
	velocity_linear = sqrt(v_x**2 + v_y**2)
	
	theta = atan(v_x/v_y)

	velocity_angular = ((a_y*v_x)-(a_x*v_y))/((v_x*v_x)+(v_y*v_y))


		#the following in terminal will make it go in perfect circle
	#rostopic pub /turtle1/cmd_vel geometry_msgs/Twist -r 1 -- '[2.0, 0.0, 0.0]' '[0.0, 0.0, 1.0]'
	return [velocity_linear, velocity_angular]

def send_vel_command():
	
	pub = rospy.Publisher('turtle1/cmd_vel',Twist, queue_size = 10)
	rospy.init_node('send_vel_command', anonymous=True)
	r = rospy.Rate(62.5) #62.5hz

	while not rospy.is_shutdown():


		t = rospy.get_time()
		velocity_linear=get_vel(t)[0]
		velocity_angular= get_vel(t)[1]
		velocities = Twist(Vector3((velocity_linear),0,0), Vector3(0,0,(velocity_angular)))
		rospy.loginfo(velocities)
		pub.publish(velocities)


		r.sleep()


                                                                                                                        
if __name__ == '__main__':
	
	try:
		# orient_turtle()
		send_vel_command()
	except rospy.ROSInterruptException: pass