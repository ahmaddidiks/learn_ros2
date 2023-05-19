#!/usr/bin/python3.10
import rclpy
from rclpy.node import Node

class MyNode(Node):
    def __init__(self, topic_name):
        super().__init__(topic_name)
        self.counter = 0
        self.get_logger().info("Hello ROS2")
        self.create_timer(0.5, self.timer_cb)
        self.create_timer(0.5, self.timer_2)
        
    def timer_cb(self):
        self.counter += 1
        self.get_logger().info("Hello1:  " + str(self.counter))
      
    def timer_2(self):
        self.counter -= 1
        self.get_logger().info("Hello2:  " + str(self.counter))

def main(args=None):
    rclpy.init(args=args)
    node = MyNode(topic_name="py_test")
    rclpy.spin(node)
    rclpy.shutdown()

if __name__ == "__main__":
    main()