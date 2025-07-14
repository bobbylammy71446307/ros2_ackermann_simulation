# ROS Package Installation Guide

This package requires ROS dependencies to be installed before building.

## Prerequisites

1. Install `rosdep` if you haven't already:
   ```bash
   sudo apt-get install python3-rosdep
   sudo rosdep init
   rosdep update

2. Install dependencies
   ```bash
   rosdep install --from-paths src --ignore-src -y
3. Install ackermann message type
   ```bash
   sudo apt-get install ros-humble-ackermann-msgs
