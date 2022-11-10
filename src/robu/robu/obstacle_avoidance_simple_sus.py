#Exercise Title:    Obstacle Avoidance Simple - TurtleBot3
#Group:             ?
#Class:             ?
#Date:              ?


import rclpy
from rclpy.node import Node
import math

from geometry_msgs.msg import Twist
from rclpy.node import Node
from rclpy.qos import QoSProfile
from rclpy.qos import qos_profile_sensor_data
from sensor_msgs.msg import LaserScan


class ObastacleAvoidanceSimple(Node):
    def __init__(self, regional_angle_deg = 30, normal_lin_vel=0.2, trans_lin_vel=-0.05, trans_ang_vel=1.0):
        super().__init__('ObstacleAvoidanceSimple')

        """************************************************************
        ** Initialise variables
        ************************************************************"""

        self.REGIONAL_ANGLE_DEG = regional_angle_deg
        self.NORMAL_LIN_VEL = normal_lin_vel
        self.TRANS_LIN_VEL = trans_lin_vel
        self.OBSTACLE_DIST = 0.3 #Meter
        
        #.....

        """************************************************************
        ** Initialise ROS publishers and subscribers
        ************************************************************"""
        qos = QoSProfile(depth=10)

        # Initialise publishers - use method create_publisher
        
        self.vel_obj = self.create_publisher(Twist, 'cmd_vel', qos)

        # Initialise subscribers - use method create_subscription
        self.scan_obj = self.create_subscription(LaserScan, 'scan', 
                            self.scan_callback, qos_profile_sensor_data)
                            
        
        """************************************************************
        ** Initialise timers
        ************************************************************"""
        self.update_timer = self.create_timer(
            0.010,  # unit: s
            self.timer_callback)
    
    def scan_callback(self, msg):
        self.scan = msg
    
    def timer_callback(self):
        segment, z_vel_angular = self.obstacle_avoidance()
        self.steer( segment!=0, z_vel_angular )


    def obstacle_avoidance(self):
        #Berechnung der Segmentanzahl

        segment_size = 360 / self.REGIONAL_ANGLE_DEG

        segment_distance_size = len(self.scan.ranges) / segment_size

        #segment_order = segment_size * [0]

        segement_order = [0, 1, 6, 2, 5, 3, 4] #.....


        distances = self.scan.ranges[-segment_distance_size/2:] + self.scan.ranges[0:segment_distance_size/2]

        self.segment[0] = [ x for x in distances if (x < self.OBSTACLE_DIST) and (x != 'inf')]

        end = segment_distance_size/2
        for i in range(1, segment_size):
            begin = end
            end = begin + segment_distance_size
            distances = self.scan.ranges[begin:end]
            self.segment[i] = [ x for x in distances if (x < self.OBSTACLE_DIST) and (x != 'inf')]

        #ToDo
        #Beste Ausweichroute suchen
        #Siehe 3. Flussdiagramm
        #Segement nach Priorität durchsuchen

        #Rückgabewert -> Freies Segment oder Beste Ausweichmöglichkeit
        # return segmentnr, z_vel_angular

    def steer(self, steer=False, ang_vel=0.0):
        #set lineara and angular speed

        vel = Twist()
        if not steer:
            vel.linear.x = self.NORMAL_LIN_VEL
            vel.angular.z = 0
        else:
            vel.linear.x = self.TRANS_LIN_VEL
            vel.angular.z = ang_vel
        
        vel.linear.y = 0
        vel.linear.z = 0
        vel.angular.x = 0
        vel.angular.y = 0

        self.vel_obj.publish(vel)


        #publish the cmd_vel topic to the other ros nodes
        pass
    def __del__(self):
        pass
        

def main(args=None):
    rclpy.init(args=args)

    obstacleavoidance_node = ObastacleAvoidanceSimple()

    rclpy.spin(obstacleavoidance_node)

    # Destroy the node explicitly
    # (optional - otherwise it will be done automatically
    # when the garbage collector destroys the node object)
    obstacleavoidance_node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()