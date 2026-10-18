#!/usr/bin/env python3
"""
==============================================================================
BRONE INTEGRATION TEST TOOL: MOCK TARGET PERSON PUBLISHER
==============================================================================
Fungsi:
Menyimulasikan posisi target orang (/brone/target_person) tanpa perlu menyalakan
kamera fisik atau meminta orang berdiri di depan robot.

Digunakan untuk:
1. Tim SDSC (Navigasi Base): Menguji algoritma pengereman otomatis (Auto-Stop 1.0 m).
2. Tim Kinematika (ZMP): Menguji respon kestabilan badan robot saat deselerasi roda.
3. Mas Evan (Gaze): Verifikasi alur subscriber sudut leher tanpa kamera.

Skenario Uji:
- Orang mulai pada jarak Z = 2.5 meter.
- Orang bergerak mendekat ke arah robot (Z berkurang secara bertahap).
- Begitu Z <= 1.0 meter, indikator [AUTO-STOP GATE] aktif.
- Roda SDSC diuji apakah benar-benar memutus /cmd_vel menjadi 0.0 m/s.
==============================================================================
"""

import rclpy
from rclpy.node import Node
from geometry_msgs.msg import PointStamped
import math
import time

class MockTargetPublisher(Node):

    def __init__(self):
        super().__init__('mock_target_publisher')
        
        # Publisher ke topik kontrak integrasi
        self.publisher_ = self.create_publisher(PointStamped, '/brone/target_person', 10)
        
        # Timer loop 20 Hz (frekuensi navigasi standar)
        self.timer = self.create_timer(0.05, self.timer_callback)
        
        self.start_time = time.time()
        self.get_logger().info('='*60)
        self.get_logger().info('🤖 [BRONE TEST TOOL] Mock Target Person Publisher AKTIF')
        self.get_logger().info('Topik: /brone/target_person (PointStamped)')
        self.get_logger().info('Skenario: Orang mendekat dari Z=2.5m menuju Z=0.7m')
        self.get_logger().info('Target Pengujian: Verifikasi Auto-Stop 1.0 m Tim SDSC')
        self.get_logger().info('='*60)

    def timer_callback(self):
        elapsed = time.time() - self.start_time
        
        # Gerak bolak-balik siklik 20 detik: 2.5m -> 0.7m -> 2.5m
        cycle_period = 20.0
        phase = (elapsed % cycle_period) / cycle_period  # 0.0 s.d. 1.0
        
        # Jarak Z disimulasikan dari 2.5m ke 0.7m lalu kembali
        z_distance = 1.6 + 0.9 * math.cos(phase * 2 * math.pi)
        
        # Sedikit osilasi horizontal X (+/- 0.3 meter) untuk menguji pelacakan leher
        x_offset = 0.3 * math.sin(phase * 4 * math.pi)
        y_offset = 0.0  # Ketinggian stabil di bidang horizontal dada robot
        
        msg = PointStamped()
        msg.header.stamp = self.get_clock().now().to_msg()
        msg.header.frame_id = 'camera_link'
        
        msg.point.x = float(x_offset)
        msg.point.y = float(y_offset)
        msg.point.z = float(z_distance)
        
        self.publisher_.publish(msg)
        
        # Log status keselamatan
        if z_distance <= 1.0:
            status = '🛑 [AUTO-STOP ACTIVE - RODA WAJIB DIAM 0.0 m/s]'
        else:
            status = '🟢 [APPROACH ZONE - RODA BOLEH MELUNCUR]'
            
        self.get_logger().info(
            f'Target [X={x_offset:+.2f}m, Z={z_distance:.2f}m] | Status: {status}',
            throttle_duration_sec=0.5
        )

def main(args=None):
    rclpy.init(args=args)
    node = MockTargetPublisher()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        node.get_logger().info('Mock Target Publisher dihentikan.')
    finally:
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()
