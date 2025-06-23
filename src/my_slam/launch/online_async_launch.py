import os

from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node
from ament_index_python.packages import get_package_share_directory



def generate_launch_description():
    use_sim_time = LaunchConfiguration('use_sim_time')
    slam_params_file = os.path.join(get_package_share_directory("my_slam"),
                                   'config', 'mapper_params_online_async.yaml')
    
    rviz_config_file = os.path.join(get_package_share_directory("my_slam"),
                                   'rviz', 'mapping.rviz')

    declare_use_sim_time_argument = DeclareLaunchArgument(
        'use_sim_time',
        default_value='true',
        description='Use simulation/Gazebo clock')
    declare_slam_params_file_cmd = DeclareLaunchArgument(
        'slam_params_file',
        default_value=os.path.join(get_package_share_directory("my_slam"),
                                   'config', 'mapper_params_online_async.yaml'),
        description='Full path to the ROS2 parameters file to use for the slam_toolbox node')

    start_async_slam_toolbox_node = Node(
        parameters=[
          slam_params_file,
          {'use_sim_time': use_sim_time}
        ],
        package='slam_toolbox',
        executable='async_slam_toolbox_node',
        name='slam_toolbox',
        output='screen')
    
    point_cloud_to_laser_node=Node(
        package='pointcloud_to_laserscan', executable='pointcloud_to_laserscan_node',
        remappings=[('cloud_in', ['/xt_lidar/points']),
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
        ros_arguments=['--ros-args', '--log-level', 'info'],
        arguments=['--qos-reliability', 'reliable'],  # Force RELIABLE QoS
        name='pointcloud_to_laserscan'
    )

    rviz_node=Node(
        package='rviz2',
        executable='rviz2',
        name='rviz2',
        output='screen',
        arguments=['-d', rviz_config_file],
        parameters=[{'use_sim_time': use_sim_time}]
    )

    ld = LaunchDescription()
    ld.add_action(point_cloud_to_laser_node)
    ld.add_action(declare_use_sim_time_argument)
    ld.add_action(declare_slam_params_file_cmd)
    ld.add_action(start_async_slam_toolbox_node)
    ld.add_action(rviz_node)

    return ld
