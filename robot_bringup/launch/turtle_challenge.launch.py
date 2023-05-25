from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
    ld = LaunchDescription()

    turtlesim_app = Node(
        package="turtlesim",
        executable="turtlesim_node"
    )

    turtlesim_tele_op = Node(
        package="turtlesim",
        executable="turtle_teleop_key"
    )
    
    ld.add_action(turtlesim_app)
    ld.add_action(turtlesim_tele_op)
    return ld