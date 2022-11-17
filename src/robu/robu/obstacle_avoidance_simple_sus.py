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

        self.scan = None
        
        self.REGIONAL_ANGLE_DEG = regional_angle_deg
        self.OBSTACLE_DIST = 0.3

        self.NORMAL_LIN_VEL = normal_lin_vel
        self.TRANS_LIN_VEL  = trans_lin_vel
        self.TRANS_ANG_VEL  = trans_ang_vel

                
        self.vel_obj = Twist()

        """************************************************************
        ** Initialise ROS publishers and subscribers
        ************************************************************"""
        qos = QoSProfile(depth=10)

        # Initialise publishers - use method create_publisher

        self.cmd_vel_pub = self.create_publisher(Twist, 'cmd_vel', qos)

        # Initialise subscribers - use method create_subscription
        self.cmd_scan_sub = self.create_subscription(LaserScan, 'scan', 
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

        if self.scan == None:
            return False, 0.0
        
        #Berechnung der Segmentanzahl...
        segment_size = int(360 / self.REGIONAL_ANGLE_DEG + 0.5)
        segment_distance_size = int(len(self.scan.ranges) / segment_size)

        #Die Suchpriorisierung festelegen. Das Array enthält die Nummern der Segmente
        #segement_order = [0, 1, 6, 2, 5, 3, 4] #.....
        segment_order = [0] * segment_size
        for i in range(int((segment_size)/2)):
            segment_order[2*i] = i
            segment_order[2*i+1] = segment_size-i-1
        segment_order[-1] = int((segment_size)/2)

        #Bestimmung welche Regionen Abstandsverletzungen enthält. 
        #D.h. das Array nach Abständen < self.OBSTACLE_DIST filtern
        segment_distances = segment_size * [[]]      #Array mit leeren Feldern je Segment erstellen 
        begin = -int(segment_distance_size/2)
        end = begin + segment_distance_size
        distances = self.scan.ranges[begin : ] + self.scan.ranges[ : end]
        #Abstandsverletzung vor dem Roboter = Segment 0 filtern/berechnen
        segment_distances[0] = [x for x in distances if x <= self.OBSTACLE_DIST and x != 'inf']
        #Abstandsverletzungen in den restlichen Segmenten suchen
        for i in range(1,segment_size):
            begin = end
            end = begin + segment_distance_size
            distances = self.scan.ranges[begin : end]
            segment_distances[i] = [x for x in distances if (x <= self.OBSTACLE_DIST) and (x != 'inf')]
        
        #TODO - Beste Ausweichroute suchen - Siehe 3. Flussdiagramm
        #Segement in der Reihenfolge ihrer Priorität durchsuchen -> segment_order
        #Leere Segmente werden bevorzugt (keine Hindernisse), wenn keine Leeren Segmente gefunden werden,
        #könnte der Robot das Segment mit den größen Absthänden anfahren

        #Rückgabewert -> Freies Segment oder Beste Ausweichmöglichkeit
        # return segmentnr, z_vel_angular


        #TODO - Berechnung der Drehgeschwindigkeit
        #0.0 rad/s, -xx rad/s, +xx rad/s

        #TODO - Rückgabe des Ausweichsegments und der Drehgeschindigkeit
        #return ....

    def steer(self, steer=False, ang_vel=0.0):
        if not steer:
            self.vel_obj.linear.x = self.NORMAL_LIN_VEL
        else:
            self.vel_obj.linear.x = self.TRANS_LIN_VEL
        self.vel_obj.linear.y  = 0.0
        self.vel_obj.linear.z  = 0.0
        self.vel_obj.angular.x = 0.0
        self.vel_obj.angular.y = 0.0
        self.vel_obj.angular.z = ang_vel

        self.cmd_vel_pub.publish(self.vel_obj)

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