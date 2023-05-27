from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
    ld = LaunchDescription()

    turtlesim_app = Node(
        package="turtlesim",
        executable="turtlesim_node"
    )

    controller = Node(
        package="turtlesim_challenge",
        executable="turtle_controller"
    )

    spawner = Node(
        package="turtlesim_challenge",
        executable="turtle_spawner"
    )
    
    ld.add_action(turtlesim_app)
    ld.add_action(controller)
    ld.add_action(spawner)
    return ld