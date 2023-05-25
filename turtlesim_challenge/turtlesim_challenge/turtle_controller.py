#!/usr/bin/env python3

import math
import rclpy
from rclpy.node import Node
from functools import partial

from turtlesim.msg import Pose
from geometry_msgs.msg import Twist
from robot_interface.msg import Turtle, TurtleArray
from robot_interface.srv import CatchTurtle
 
class TurtleCOntrollerNode(Node): # MODIFY NAME
    def __init__(self):
        super().__init__("turtle_controller") # MODIFY NAME

        self.turtle_to_catch_ = None

        self.pose_ = None
        self.turtles_alive_ = []
        self.cmd_vel_publisher_ = self.create_publisher(Twist, "turtle1/cmd_vel", 10)
        # self.remove_catched_turtle_publisher = self.create_publisher(Turtle, "")
        self.pose_subscriber_ = self.create_subscription(Pose, "turtle1/pose", self.cb_tutrle_pos, 10)
        self.alive_turtle_subscriber_ = self.create_subscription(TurtleArray, "alive_turtles", self.cb_alive_turtles, 10)
        self.control_loop_timer = self.create_timer(0.01, self.control_loop)
        self.get_logger().info("Turtle controller has been started")

    def cb_tutrle_pos(self, msg):
        self.pose_ = msg

    def cb_alive_turtles(self, msg):
        self.turtles_alive_ = msg
        if len(msg.turtles) > 0:
            self.turtle_to_catch_ = self.turtles_alive_.turtles[0]
    
    def control_loop(self):
        if self.pose_ == None or self.turtle_to_catch_ == None:
            return
        
        list_of_distance = []
        for turtle in self.turtles_alive_.turtles:
            _x_ = turtle.x - self.pose_.x
            _y_ = turtle.y - self.pose_.y
            list_of_distance.append(math.sqrt(_x_*_x_ + _y_*_y_))
        
        minimum_distance_index = list_of_distance.index(min(list_of_distance))
        self.turtle_to_catch_ = self.turtles_alive_.turtles[minimum_distance_index]

        dist_x = self.turtle_to_catch_.x - self.pose_.x
        dist_y = self.turtle_to_catch_.y - self.pose_.y
        distance_ = math.sqrt(dist_x*dist_x + dist_y*dist_y)

        msg = Twist()

        if distance_ > 0.5:
            # position
            msg.linear.x = 2*distance_

            #orientation
            tetha_goal =  math.atan2(dist_y, dist_x)
            diff = tetha_goal - self.pose_.theta
            if diff > math.pi:
                diff -= 2*math.pi
            elif diff < -math.pi:
                diff += 2*math.pi

            msg.angular.z = 6*diff
        else:
            # target reached
            msg.linear.x = 0.0
            msg.angular.z = 0.0
            if self.turtle_to_catch_:
                self.call_catch_turtle_server(self.turtle_to_catch_.name)
                self.turtle_to_catch_ = None

        self.cmd_vel_publisher_.publish(msg)
    
    def call_catch_turtle_server(self, turtle_name):
        clinet = self.create_client(CatchTurtle, "catch_turtle")
        while not clinet.wait_for_service(1.0):
            self.get_logger().info("Waiting for server ...")
        
        request = CatchTurtle.Request()
        request.name = turtle_name

        future = clinet.call_async(request)
        future.add_done_callback(partial(self.callback_call_catch_turtle, turtle_name=turtle_name))
    
    def callback_call_catch_turtle(self, future, turtle_name):
        try:
            response = future.result()
            if not response.success:
                self.get_logger().info(f"Turtle {turtle_name} could not be caught")
            else:
                self.get_logger().info(f"{turtle_name} killed")

        except Exception as e:
            self.get_logger().info("Service call failed %r" % (e,))
 
def main(args=None):
    rclpy.init(args=args)
    node = TurtleCOntrollerNode() # MODIFY NAME
    rclpy.spin(node)
    rclpy.shutdown()
 
 
if __name__ == "__main__":
    main()