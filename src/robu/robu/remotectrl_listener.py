import rclpy
from rclpy.node import Node

from geometry_msgs.msg import Twist
from std_msgs.msg import String


def listener_callback(msg):
    print(msg)
    #print('I heard: "%s"' % msg.data)
    #get_logger().info('I heard: "%s"' % msg.data)


def main(args=None):
    rclpy.init(args=args)

    node = rclpy.create_node('remotectrl_listener')
    print("started")
    node.create_subscription(
        Twist,
        'cmd_vel',
        listener_callback,
        10)

    rclpy.spin(node)

    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()