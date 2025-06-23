#!/usr/bin/env python3
from launch import LaunchDescription
from launch_ros.actions import Node
from launch.substitutions import PathJoinSubstitution
from launch.actions import DeclareLaunchArgument
from launch_ros.substitutions import FindPackageShare

def generate_launch_description():
    # Path configurations
    # smac_config = PathJoinSubstitution([
    #     FindPackageShare("my_slam"),
    #     "config",
    #     "smac_planner.yaml"
    # ])
    
    # ackermann_config = PathJoinSubstitution([
    #     FindPackageShare("my_slam"),
    #     "config",
    #     "smac_planner.yaml"
    # ])
    
    map_dir = PathJoinSubstitution([
        FindPackageShare("my_slam"),
        "maps",
        "carter_warehouse_navigation.yaml"
    ])
    
    amcl_config = PathJoinSubstitution([
        FindPackageShare("my_slam"),
        "config",
        "amcl.yaml"
    ])

    return LaunchDescription([
        DeclareLaunchArgument(
            'use_sim_time',
            default_value='true',
            description='Use simulation clock'
        ),
        
        # Map Server
        Node(
            package='nav2_map_server',
            executable='map_server',
            name='map_server',
            output='screen',
            parameters=[{
                'use_sim_time': True,
                'yaml_filename': map_dir,
                'topic_name': 'map',
                'frame_id': 'map'
            }]
        ),
        
        # AMCL
        Node(
            package='nav2_amcl',
            executable='amcl',
            name='amcl',
            output='screen',
            parameters=[amcl_config],
            remappings=[('scan', '/scan'),
                        ('/tf', 'tf'),
                        ('/tf_static', 'tf_static')]
        ),
        
        # # SMAC Planner (Ackermann)
        # Node(
        #     package='nav2_planner',
        #     executable='planner_server',
        #     name='planner_server',
        #     output='screen',
        #     parameters=[smac_config]
        # ),
        
        # # Ackermann Controller
        # Node(
        #     package='nav2_controller',
        #     executable='controller_server',
        #     name='controller_server',
        #     output='screen',
        #     parameters=[ackermann_config]
        # ),
        
        # Node(
        #     package='nav2_bt_navigator',
        #     executable='bt_navigator',
        #     name='bt_navigator',
        #     output='screen',
        #     parameters=[
        #         PathJoinSubstitution([
        #             FindPackageShare('my_slam'),
        #             'config',
        #             'smac_planner.yaml'
        #         ])
        #     ]
        # ),
        
        # Lifecycle Manager
        Node(
            package='nav2_lifecycle_manager',
            executable='lifecycle_manager',
            name='lifecycle_manager',
            output='screen',
            parameters=[{
                'use_sim_time': True,
                'autostart': True,
                'node_names': [
                    'map_server',
                    'amcl'
                    # 'planner_server',
                    # 'controller_server',
                    # 'bt_navigator'
                ]
            }]
        )
    ])