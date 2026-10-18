cmake_minimum_required(VERSION 3.8)
project(brone_system_architecture)

if(CMAKE_COMPILER_IS_GNUCXX OR CMAKE_CXX_COMPILER_ID MATCHES "Clang")
  add_compile_options(-Wall -Wextra -Wpedantic)
endif()

find_package(ament_cmake REQUIRED)

# Install executable scripts agar bisa dijalankan via: ros2 run brone_system_architecture <script>
install(PROGRAMS
  scripts/mock_target_publisher.py
  DESTINATION lib/${PROJECT_NAME}
)

# Install launch files, configs, dan scripts ke share/brone_system_architecture
install(DIRECTORY
  launch
  config
  scripts
  DESTINATION share/${PROJECT_NAME}
)

ament_package()
