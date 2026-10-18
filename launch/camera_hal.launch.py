#!/usr/bin/env python3
"""
==============================================================================
BRONE CAMERA HARDWARE ABSTRACTION LAYER (HAL) MASTER LAUNCH
==============================================================================
Fungsi:
Menyediakan antarmuka tunggal untuk mengabstraksi perangkat keras kamera robot BRONE.
Konsumen downstream (Mas Evan, Kak Anya, Tim SDSC) HANYA perlu berlangganan topik
standar:
  - Citra Warna : /camera/color/image_raw (sensor_msgs/Image)
  - Kalibrasi   : /camera/color/camera_info (sensor_msgs/CameraInfo)
  - Kedalaman   : /camera/depth/image_rect_raw (sensor_msgs/Image - D455 Only)

Penggunaan di Terminal:
  # Mode A (Kamera Brio Sekarang):
  ros2 launch brone_system_architecture camera_hal.launch.py camera_type:=brio

  # Mode B (Intel RealSense D455 Nanti):
  ros2 launch brone_system_architecture camera_hal.launch.py camera_type:=d455
==============================================================================
"""

from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, LogInfo
from launch.conditions import IfCondition
from launch.substitutions import LaunchConfiguration, PythonExpression
from launch_ros.actions import Node

def generate_launch_description():
    # 1. Deklarasi Argumen Pemilihan Kamera (Default: 'brio' untuk keselamatan sistem eksisting)
    camera_type_arg = DeclareLaunchArgument(
        'camera_type',
        default_value='brio',
        description='Tipe kamera target: "brio" (Logitech BRIO USB) atau "d455" (Intel RealSense D455 RGB-D)'
    )

    camera_type = LaunchConfiguration('camera_type')

    # Kondisi Evaluasi
    is_brio = IfCondition(PythonExpression(["'", camera_type, "' == 'brio'"]))
    is_d455 = IfCondition(PythonExpression(["'", camera_type, "' == 'd455'"]))

    # 2. Driver Mode A: Logitech BRIO (usb_cam dengan remap standar)
    # Menghubungkan node usb_cam_node_exe eksisting ke topik baku /camera/color/image_raw
    brio_camera_node = Node(
        package='usb_cam',
        executable='usb_cam_node_exe',
        name='brio_camera_driver',
        namespace='camera',
        parameters=[{
            'video_device': '/dev/video0',
            'image_width': 640,
            'image_height': 480,
            'framerate': 30.0,
            'pixel_format': 'mjpeg2rgb',
            'camera_name': 'logitech_brio',
        }],
        remappings=[
            ('image_raw', 'color/image_raw'),
            ('camera_info', 'color/camera_info')
        ],
        condition=is_brio,
        output='screen'
    )

    # 3. Driver Mode B: Intel RealSense D455 (RGB-D Hardware Processor)
    d455_camera_node = Node(
        package='realsense2_camera',
        executable='realsense2_camera_node',
        name='d455_camera_driver',
        namespace='camera',
        parameters=[{
            'enable_color': True,
            'enable_depth': True,
            'rgb_camera.profile': '640x480x30',
            'depth_module.profile': '640x480x30',
            'align_depth.enable': True,
            'pointcloud.enable': False,
            'enable_sync': True,
        }],
        remappings=[
            ('color/image_raw', 'color/image_raw'),
            ('aligned_depth_to_color/image_raw', 'depth/image_rect_raw')
        ],
        condition=is_d455,
        output='screen'
    )

    # Log Notifikasi Status Mode Aktif
    log_status = LogInfo(
        msg=PythonExpression([
            "'[BRONE HAL] Kamera diinisialisasi dalam MODE: ' + '", camera_type, 
            "' -> Output terbit di /camera/color/image_raw'"
        ])
    )

    return LaunchDescription([
        camera_type_arg,
        log_status,
        brio_camera_node,
        d455_camera_node
    ])
