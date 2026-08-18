from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
    return LaunchDescription([
        Node(
            package='turtlesim',
            executable='turtlesim_node',
            name='turtlesim_node',
            output='screen'
        ),
        Node(
            package='robot_control',
            executable='NODE',
            name='robot_trial_node',
            output='screen'
        ),
    ])