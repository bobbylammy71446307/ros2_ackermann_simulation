cmake_minimum_required(VERSION 3.5)
project(my_slam)

find_package(ament_cmake REQUIRED)

install(DIRECTORY
  behavior_tree
  launch
  params
  maps
  rviz2
  config
  samples
  usd
  DESTINATION share/${PROJECT_NAME})

ament_package()
