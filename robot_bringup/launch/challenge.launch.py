from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
    ld = LaunchDescription()
    pkg_ = 'cpp_pkg'
    executable_ = "robot_news_station"
    new_name_ = ['giskard', 'bb8', 'daneel', 'jander', 'c3po']

    for name in new_name_:
        node = Node(
            package=pkg_,
            executable=executable_,
            name="robot_news_station_"+name
        )
        ld.add_action(node)
    
    smarphone = Node(
        package=pkg_,
        executable="smartphone",
    )
    ld.add_action(smarphone)
    return ld