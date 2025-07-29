import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node

def generate_launch_description():

    use_sim_time = LaunchConfiguration("use_sim_time", default="True")
    map_dir = LaunchConfiguration("map",
        default=os.path.join(get_package_share_directory("my_slam"), 
        "maps", "slam_map.yaml"),
    )
    param_dir = LaunchConfiguration(
        "params_file",
        default=os.path.join(
            get_package_share_directory("my_slam"), 
            "config", "ackermann_nav_config.yaml"),
    )

    my_slam_launch_dir = os.path.join(get_package_share_directory("my_slam"), "launch")
    grid_map_localizer_launch_dir= os.path.join(get_package_share_directory("grid_map_localizer"), "launch")
    nvblox_custom_launch_dir= os.path.join(get_package_share_directory("nvblox_custom"), "launch")

    return LaunchDescription(
        [
            DeclareLaunchArgument("map", 
                                default_value=map_dir, 
                                description="Full path to map file to load"
                                ),
            DeclareLaunchArgument("params_file",
                                default_value=param_dir, 
                                description="Full path to param file to load"
                                ),
            DeclareLaunchArgument("use_sim_time",
                                default_value="True", 
                                description="Use simulation (Omniverse Isaac Sim) clock if true"
                                ),
            IncludeLaunchDescription(
                PythonLaunchDescriptionSource([nvblox_custom_launch_dir, "/nvblox.launch.py"]),
                launch_arguments={"map": map_dir, "use_sim_time": use_sim_time,"params_file": param_dir}.items(),
            ),
            IncludeLaunchDescription(
                PythonLaunchDescriptionSource([my_slam_launch_dir, "/nav2.launch.py"]),
                launch_arguments={"map": map_dir, "use_sim_time": use_sim_time,"params_file": param_dir}.items(),
            ),
            IncludeLaunchDescription(
                PythonLaunchDescriptionSource([grid_map_localizer_launch_dir, "/occupancy_localizer.launch.py"]),
                launch_arguments={"num_cameras": "1" ,"lidar": "True" }.items(),
            ),
        ]
    )
