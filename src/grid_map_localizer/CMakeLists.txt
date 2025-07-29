cmake_minimum_required(VERSION 3.5)
project(grid_map_localizer)

find_package(ament_cmake REQUIRED)

install(DIRECTORY
  launch
  DESTINATION share/${PROJECT_NAME})

ament_package()
