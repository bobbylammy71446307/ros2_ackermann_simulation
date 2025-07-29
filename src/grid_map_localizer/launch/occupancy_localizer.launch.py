# SPDX-FileCopyrightText: NVIDIA CORPORATION & AFFILIATES
# Copyright (c) 2021-2024 NVIDIA CORPORATION & AFFILIATES. All rights reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
# SPDX-License-Identifier: Apache-2.0

import os

from ament_index_python.packages import get_package_share_directory

from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription
from launch.conditions import IfCondition
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import ComposableNodeContainer, Node
from launch_ros.descriptions import ComposableNode


def generate_launch_description():

    map_file_arg = DeclareLaunchArgument(
        'map_file', default_value=os.path.join(
            get_package_share_directory(
                'my_slam'), 'maps', 'slam_map.yaml'),
        description='Full path to map file to load')
    params_file_arg = DeclareLaunchArgument(
        'params_file', default_value=os.path.join(
            get_package_share_directory(
                'my_slam'), 'config', 'ackermann_nav_config.yaml'),
        description='Full path to param file to load')
    use_sim_time_arg = DeclareLaunchArgument(
        'use_sim_time', default_value='True',
        description='Use simulation (Omniverse Isaac Sim) clock if true')

    occupancy_grid_localizer_node = ComposableNode(
        package='isaac_ros_occupancy_grid_localizer',
        plugin='nvidia::isaac_ros::occupancy_grid_localizer::OccupancyGridLocalizerNode',
        name='occupancy_grid_localizer',
        parameters=[LaunchConfiguration('map_file'), {
            'loc_result_frame': 'map',
            'map_yaml_path': LaunchConfiguration('map_file'),
        }],
        remappings=[('localization_result', '/initialpose')])

    pointcloud_to_flatscan_node = ComposableNode(
        package='isaac_ros_pointcloud_utils',
        plugin='nvidia::isaac_ros::pointcloud_utils::PointCloudToFlatScanNode',
        name='pointcloud_to_flatscan',
        remappings=[('/pointcloud','/xt_lidar/points')])

    occupancy_grid_localizer_container = ComposableNodeContainer(
        package='rclcpp_components',
        name='occupancy_grid_localizer_container',
        namespace='',
        executable='component_container_mt',
        composable_node_descriptions=[
            occupancy_grid_localizer_node,
            pointcloud_to_flatscan_node
        ],
        output='screen'
    )

    return LaunchDescription([
        map_file_arg,
        params_file_arg,
        use_sim_time_arg,
        occupancy_grid_localizer_container
    ])
