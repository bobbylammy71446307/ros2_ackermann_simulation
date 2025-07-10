import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node
# import py_trees
# import py_trees_ros.viewer as py_trees_viewer



def generate_launch_description():

    use_sim_time = LaunchConfiguration("use_sim_time", default="True")

    map_dir = LaunchConfiguration(
        "map",
        default=os.path.join(
            # get_package_share_directory("my_slam"), "maps", "carter_warehouse_navigation.yaml"
            # get_package_share_directory("my_slam"), "maps", "new_map.yaml"
            get_package_share_directory("my_slam"), "maps", "slam_map.yaml"

        ),
    )
#     # Create your behavior tree
#     root = py_trees.composites.Sequence("MyTree")
#     # ... (add nodes)

# # Start the viewer (publishes BT structure to ROS 2)
#     py_trees_viewer.display_tree(
#         root,  # Your BT root
#         namespace="/behaviour_tree",  # ROS 2 namespace
#         with_blackboard_variables=True  # Optional: show variables
#     )

    param_dir = LaunchConfiguration(
        "params_file",
        default=os.path.join(
            get_package_share_directory("my_slam"), "config", "warehouse_omni_config.yaml"
        ),
    )


    nav2_bringup_launch_dir = os.path.join(get_package_share_directory("nav2_bringup"), "launch")
    ackermann_launch_dir = os.path.join(get_package_share_directory("cmdvel_to_ackermann"), "launch")


    rviz_config_dir = os.path.join(get_package_share_directory("my_slam"), "rviz2", "my_navigation.rviz")

    return LaunchDescription(
        [
            DeclareLaunchArgument("map", default_value=map_dir, description="Full path to map file to load"),
            DeclareLaunchArgument(
                "params_file", default_value=param_dir, description="Full path to param file to load"
            ),
            DeclareLaunchArgument(
                "use_sim_time", default_value="True", description="Use simulation (Omniverse Isaac Sim) clock if true"
            ),
            IncludeLaunchDescription(
                PythonLaunchDescriptionSource(os.path.join(nav2_bringup_launch_dir, "rviz_launch.py")),
                launch_arguments={"namespace": "", "use_namespace": "False", "rviz_config": rviz_config_dir}.items(),
            ),
            IncludeLaunchDescription(
                PythonLaunchDescriptionSource([nav2_bringup_launch_dir, "/bringup_launch.py"]),
                launch_arguments={"map": map_dir, "use_sim_time": use_sim_time,"params_file": param_dir}.items(),
            ),
            IncludeLaunchDescription(
                PythonLaunchDescriptionSource([ackermann_launch_dir, "/cmdvel_to_ackermann.launch.py"]),
                launch_arguments={"map": map_dir, "use_sim_time": use_sim_time,"params_file": param_dir}.items(),
            ),

            Node(
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
                name='pointcloud_to_laserscan'
            )
        ]
    )
