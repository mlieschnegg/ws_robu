#Exercise: Mein Erster Node - Fernsteuerung des Roboters
#Group: 1
#Class: 4BHME
#Date: 13.10.2022

import rclpy

from geometry_msgs.msg import Twist
from rclpy.qos import QoSProfile
import msvcrt


msg = """
Excercise:  ?
Group:      ?
Class:      ?
Date:       ?
"""

e = """
Communications Failed
"""

def get_key():
    return msvcrt.getch().decode('utf-8')

def main():
    rclpy.init()

    qos = QoSProfile(depth=10)
    node = rclpy.create_node('remotectrl')
    pub = node.create_publisher(Twist, 'cmd_vel', qos)

    try:
        pass
                
    except Exception as e:
        print(e)

    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
