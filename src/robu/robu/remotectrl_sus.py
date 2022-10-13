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
#75...K links
#77...M rechts
#72...H vorwärts
#80...P rückwärts
#27...Escape
key_ctrl = [75, 77, 72, 80]

def get_key():
    return msvcrt.getch().decode('utf-8')

def main():
    rclpy.init()

    qos = QoSProfile(depth=10)
    node = rclpy.create_node('remotectrl')
    pub = node.create_publisher(Twist, 'cmd_vel', qos)

    try:
        print(msg)
        #add Code here
        while(1):
            key = get_key();
            print("ASCII Zeichen", key, "Code: ", ord(key))

            if ord(key) == 0x00:
                key_null_entered = True
            elif ord(key) == 27: #Escape wurde gedrueckt -> Roboter sollte stehen bleiben
                print("Escape")
            elif ord(key) == 3: #STRG+C
                break
            elif key_null_entered == True and ord(key) in key_ctrl:
                if key_ctrl[0] == ord(key):     #Links
                    print("Links")
                elif key_ctrl[1] == ord(key):   #Rechts
                    print("Rechts")
                elif key_ctrl[2] == ord(key):   #Vorwärts
                    print("Vorwärts")
                elif key_ctrl[3] == ord(key):   #Rückwärts
                    print("Rückwärts")
                key_null_entered = False
                
    except Exception as e:
        print(e)

    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
