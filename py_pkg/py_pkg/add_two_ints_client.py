#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from functools import partial

from example_interfaces.srv import AddTwoInts
 
class AddTwoIntsClientNode(Node): # MODIFY NAME
    def __init__(self):
        super().__init__("add_two_ints_client") # MODIFY NAME
        for i in range(10):
            self.call_add_two_ints_server(5,i)
    
    def call_add_two_ints_server(self, a, b):
        clinet = self.create_client(AddTwoInts, "add_two_ints")
        while not clinet.wait_for_service(1.0):
            self.get_logger().info("Waiting for server Add Two Ints...")
        
        request = AddTwoInts.Request()
        request.a, request.b = a,b

        future = clinet.call_async(request)
        future.add_done_callback(partial(self.callback_call_add_two_ints, a=a, b=b))
    
    def callback_call_add_two_ints(self, future, a, b):
        try:
            response = future.result()
            self.get_logger().info(f"{a} + {b} = {response.sum}")
        except Exception as e:
            self.get_logger().info("Service call failed %r" % (e,))
 
def main(args=None):
    rclpy.init(args=args)
    node = AddTwoIntsClientNode() # MODIFY NAME
    rclpy.spin(node)
    rclpy.shutdown()
 
 
if __name__ == "__main__":
    main()