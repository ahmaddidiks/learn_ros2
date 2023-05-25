from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
    ld = LaunchDescription()

    rempap_number_topic = ("number", "new_number")

    number_publisher_node = Node(
        package="py_pkg",
        executable="number_publisher",
        name="new_number_publisher",
        remappings=[
            rempap_number_topic
        ],
        parameters=[
            {"number_to_publish": 4},
            {"publish_frequency": 10.0}
        ]
    )

    robot_news_station = Node(
        package="cpp_pkg",
        executable="robot_news_station"
    )

    number_counter_node = Node(
        package="py_pkg",
        executable="number_counter",
        name="new_number_counter",
        remappings=[
            rempap_number_topic,
            ("number_count", "new_number_count")
        ]
    )

    ld.add_action(number_publisher_node)
    ld.add_action(number_counter_node)
    # ld.add_action(robot_news_station)
    return ld