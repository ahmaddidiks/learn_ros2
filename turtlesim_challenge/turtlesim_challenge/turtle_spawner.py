#!/usr/bin/env python3
import rclpy
from functools import partial
import random
import math
from rclpy.node import Node

from turtlesim.srv import Spawn, Kill
from robot_interface.msg import Turtle, TurtleArray
from robot_interface.srv import CatchTurtle
 
class TurtleSpawnerNode(Node): # MODIFY NAME
    def __init__(self):
        super().__init__("node_name") # MODIFY NAME
        self.tutrle_name_prefix_ = "turtle"
        self.turtle_counter_ = 1
        self.alive_turtles_ = []
        self.alive_turtle_publisher_ = self.create_publisher(TurtleArray, "alive_turtles", 10)
        self.spawn_turtle_timer_ = self.create_timer(1.0, self.spawn_new_turtle)
        self.cath_turtle_service = self.create_service(CatchTurtle, "catch_turtle", self.cb_catch_turtle)
        self.get_logger().info("Turtle spawner has been started")

    def cb_catch_turtle(self, request, response):
        self.call_kill_server(request.name)
        response.success = True
        return response
    
    def call_kill_server(self, turtle_name):
        clinet = self.create_client(Kill, "kill")
        while not clinet.wait_for_service(1.0):
            self.get_logger().info("Waiting for server ...")
        
        request = Kill.Request()
        request.name = turtle_name
        future = clinet.call_async(request)
        future.add_done_callback(partial(self.callback_call_kill, turtle_name=turtle_name))
    
    def callback_call_kill(self, future, turtle_name):
        try:
            future.result()
            for (i, turtle) in enumerate(self.alive_turtles_):
                if turtle.name == turtle_name:
                    del self.alive_turtles_[i]
                    self.publish_alive_turtles()
                    break

        except Exception as e:
            self.get_logger().info("Service call failed %r" % (e,))
    
    def publish_alive_turtles(self):
      msg = TurtleArray()
      msg.turtles = self.alive_turtles_
      self.alive_turtle_publisher_.publish(msg)

    def spawn_new_turtle(self):
        self.turtle_counter_ +=1
        name = self.tutrle_name_prefix_ + str(self.turtle_counter_)
        x = random.uniform(0.0, 11.0)
        y = random.uniform(0.0, 11.0)
        theta = random.uniform(0.0, 2*math.pi)
        
        self.call_spawn_server(name, x, y, theta)
        
    
    def call_spawn_server(self, turtle_name, x, y, theta):
        clinet = self.create_client(Spawn, "spawn")
        while not clinet.wait_for_service(1.0):
            self.get_logger().info("Waiting for server ...")
        
        request = Spawn.Request()
        request.x, request.y = x,y
        request.theta, request.name = theta, turtle_name

        future = clinet.call_async(request)
        future.add_done_callback(partial(self.callback_call_spawn, turtle_name=turtle_name, x=x, y=y, theta=theta))
    
    def callback_call_spawn(self, future, turtle_name, x, y, theta):
        try:
            response = future.result()
            if response.name != "":
              self.get_logger().info(f"{response.name} is now alive")
              new_turtle = Turtle()
              new_turtle.name = response.name
              new_turtle.x = x
              new_turtle.y = y
              new_turtle.theta = theta
              self.alive_turtles_.append(new_turtle)
              self.publish_alive_turtles()

        except Exception as e:
            self.get_logger().info("Service call failed %r" % (e,))
 
 
def main(args=None):
    rclpy.init(args=args)
    node = TurtleSpawnerNode() # MODIFY NAME
    rclpy.spin(node)
    rclpy.shutdown()
 
 
if __name__ == "__main__":
    main()