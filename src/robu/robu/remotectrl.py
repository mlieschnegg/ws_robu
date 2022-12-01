#Exercise Title:    Remote control for TurtleBot3 Burger
#Group:             LI/UW
#Class:             4 AHMBA
#Date:              20.10.2022


import rclpy

from geometry_msgs.msg import Twist
from rclpy.qos import QoSProfile
import msvcrt


msg = """
Excercise:  RemoteCtrl
Group:      1
Date:       13.10.2022
"""

e = """
Communications Failed
"""

key_ctrl = ['M', 'K', 'H', 'P'] 


MAX_LIN_VEL = 0.22      #m/s
MAX_ANG_VEL = 2.84      #rad/s

LIN_VEL_STEP_SIZE = 0.01    #m/s
ANG_VEL_STEP_SIZE = 0.1     #rad/s


def get_key():
    return msvcrt.getch().decode('utf-8')

def main():
    key_null_entered = False

    rclpy.init()

    qos = QoSProfile(depth=10)
    node = rclpy.create_node('remotectrl')
    pub = node.create_publisher(Twist, 'cmd_vel', qos)
    
    vel = Twist()
    try:
        print(msg)
        while(1):
            key = get_key()
            
            #print("Key: ", key, ", Ord: ", ord(key))
            if ord(key) == 0x00:    #Key: Null
                key_null_entered = True
            elif ord(key) == 0x1B:    #Key: Esc
                print("Esc")
                #rospy.loginfo("ESC") # 
                vel.linear.x = 0.0
                vel.angular.z = 0.0
            elif ord(key) == 0x03:    #Key: STRG+C
                vel.linear.x = 0.0
                vel.angular.z = 0.0
                pub.publish(vel)
                break
            elif key_null_entered and key in key_ctrl:
                if key == key_ctrl[0]: #Roboter beschleunigt Drehung um Z-Achse
                    print("Right")
                    vel.angular.z = vel.angular.z - ANG_VEL_STEP_SIZE
                    if (vel.angular.z < -MAX_ANG_VEL):
                        vel.angular.z = -MAX_ANG_VEL
                elif key == key_ctrl[1]:
                    print("Left")
                    vel.angular.z = vel.angular.z + ANG_VEL_STEP_SIZE
                    if (vel.angular.z > MAX_ANG_VEL):
                        vel.angular.z = MAX_ANG_VEL
                elif key == key_ctrl[2]:    #Roboter beschleunigt in X-Richtung
                    print("Up")
                    vel.linear.x = vel.linear.x + LIN_VEL_STEP_SIZE
                    if (vel.linear.x > MAX_LIN_VEL):
                        vel.linear.x = MAX_LIN_VEL
                elif key == key_ctrl[3]:    #Robter bremst in X-Richtung
                    print("Down")
                    vel.linear.x = vel.linear.x - LIN_VEL_STEP_SIZE
                    if (vel.linear.x < -MAX_LIN_VEL):
                        vel.linear.x = -MAX_LIN_VEL
                key_null_entered = False
            
            pub.publish(vel)
    except Exception as e:
        print(e)

    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
