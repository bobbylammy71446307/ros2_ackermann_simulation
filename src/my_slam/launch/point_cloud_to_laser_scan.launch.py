import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node
from rclpy.qos import QoSProfile, QoSReliabilityPolicy


def generate_launch_description():
    ackermann_launch_dir = os.path.join(get_package_share_directory("cmdvel_to_ackermann"), "launch")
    return LaunchDescription(
        [   IncludeLaunchDescription(
                PythonLaunchDescriptionSource([ackermann_launch_dir, "/cmdvel_to_ackermann.launch.py"]),
                launch_arguments={"map": map_dir, "use_sim_time": use_sim_time,"params_file": param_dir}.items(),
            ),
            Node(
                package='pointcloud_to_laserscan', executable='pointcloud_to_laserscan_node',
                remappings=[('cloud_in', ['/xt_lidar/point']),
                            ('scan', ['/scan'])],
                parameters=[{
                    'target_frame': 'xt_lidar',
                    'transform_tolerance': 0.01,
                    'min_height': 0.04,
                    'max_height': 0.75,
                    'angle_min': -3.14159,  # -M_PI/2
                    'angle_max': 3.14159,  # M_PI/2
                    'angle_increment': 0.0087,  # M_PI/360.0
                    'scan_time': 0.3333,
                    'range_min': 0.01,
                    'range_max': 100.0,
                    'use_inf': True,
                    'inf_epsilon': 1.0,
                    # 'concurrency_level': 1,
                }],
                name='pointcloud_to_laserscan'
            )
        ]
    )
