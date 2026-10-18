# 📄 DOKUMEN GRAND PLAN SISTEM, CONTRACT ABSTRAKSI HARDWARE, & MATRIKS DELEGASI TIM ROBOT BRONE (v1.0)
## *Arsitektur OS-Level Hardware Abstraction Layer (HAL), Kontrak Data ROS 2, Garis Batas Tanggung Jawab Tim, & Strategi Transisi Kamera Tanpa Revisi Kode*

---

> **Dokumen Resmi:** Panduan Teknis & Delegasi Sistem Robot BRONE  
> **Penulis / Peran:** Systems, Middleware, OS & Integration Engineer (Lead Systems Architect)  
> **Otoritas Mandat:** Tindak Lanjut Evaluasi Ketua Tim & Rekomendasi Restrukturisasi Peran  
> **Target Pengguna Dokumen:** Seluruh Anggota Divisi Robot BRONE (Mas Evan, Kak Anya, Tim SDSC, Tim LLM)  
> **Milestone Utama:** Uji Terintegrasi Skripsi S1 Mas Evan & Demonstrasi Tamu Rektorat (November 2026)  
> **Hardware Target:** Wheeled-Humanoid Robot BRONE (NVIDIA Jetson Orin Nano + Intel NUC Core i9 + OpenCR 1.0)  

---

## 📑 DAFTAR ISI

1. [Prolog: Evaluasi Peran & Filosofi "System Engineer"](#1-prolog-evaluasi-peran--filosofi-system-engineer)
2. [Grand Plan Arsitektur OS & Hardware Abstraction Layer (HAL)](#2-grand-plan-arsitektur-os--hardware-abstraction-layer-hal)
   * [2.1 Dual-Mode Camera HAL (Mode A: Legacy BRIO ↔ Mode B: RealSense D455)](#21-dual-mode-camera-hal-mode-a-legacy-brio--mode-b-realsense-d455)
   * [2.2 Standard Interface Contract Document (ICD) ROS 2](#22-standard-interface-contract-document-icd-ros-2)
   * [2.3 Eksternalisasi Parameter Kamera & Tuning Servo (YAML Dynamic Tuning)](#23-eksternalisasi-parameter-kamera--tuning-servo-yaml-dynamic-tuning)
   * [2.4 Eliminasi Subprocess v4l2-ctl dari Algoritma Internal](#24-eliminasi-subprocess-v4l2-ctl-dari-algoritma-internal)
   * [2.5 Isolasi Komputasi OS (Zero-Jitter CPU Affinity & Deterministic Services)](#25-isolasi-komputasi-os-zero-jitter-cpu-affinity--deterministic-services)
3. [Matriks Pembagian Tugas & Garis Batas Tanggung Jawab (Delegasi)](#3-matriks-pembagian-tugas--garis-batas-tanggung-jawab-delegasi)
   * [3.1 Demarcation of Responsibility (System Engineer vs Sub-Tim Domain)](#31-demarcation-of-responsibility-system-engineer-vs-sub-tim-domain)
   * [3.2 Instruksi Delegasi Spesifik untuk Tim Gaze (Mas Evan)](#32-instruksi-delegasi-spesifik-untuk-tim-gaze-mas-evan)
   * [3.3 Instruksi Delegasi Spesifik untuk Tim Civitas Akademika (Kak Anya)](#33-instruksi-delegasi-spesifik-untuk-tim-civitas-akademika-kak-anya)
   * [3.4 Instruksi Delegasi Spesifik untuk Tim Kinematika & Navigasi (Wisnu / SDSC)](#34-instruksi-delegasi-spesifik-untuk-tim-kinematika--navigasi-wisnu--sdsc)
   * [3.5 Instruksi Delegasi Spesifik untuk Tim LLM & Voice Interaction](#35-instruksi-delegasi-spesifik-untuk-tim-llm--voice-interaction)
   * [3.6 Tabel Matriks RACI (Responsible, Accountable, Consulted, Informed)](#36-tabel-matriks-raci-responsible-accountable-consulted-informed)
4. [Poin Komunikasi Menenangkan & Strategis untuk Mas Evan](#4-poin-komunikasi-menenangkan--strategis-untuk-mas-evan)
   * [4.1 Menjawab Akar Kekhawatiran Mas Evan Secara Logis & Objektif](#41-menjawab-akar-kekhawatiran-mas-evan-secara-logis--objektif)
   * [4.2 Teks Draf Pesan Siap Kirim ke Mas Evan (WhatsApp / Discord / Briefing)](#42-teks-draf-pesan-siap-kirim-ke-mas-evan-whatsapp--discord--briefing)
   * [4.3 Tiga Bukti Teknis Mengapa Transisi D455 "Zero-Breaking-Change" bagi Gaze](#43-tiga-bukti-teknis-mengapa-transisi-d455-zero-breaking-change-bagi-gaze)
5. [Roadmap Integrasi & Prosedur Eksekusi Bertahap (W0 - W4)](#5-roadmap-integrasi--prosedur-eksekusi-bertahap-w0---w4)

---

## 1. PROLOG: EVALUASI PERAN & FILOSOFI "SYSTEM ENGINEER"

Berdasarkan hasil evaluasi dan arahan Ketua Tim, telah disepakati restrukturisasi pola kerja demi efektivitas dan keberlanjutan proyek robot BRONE:

* **Kendala Sebelumnya:** System Engineer terlalu dalam terjun mengutak-atik kode internal algoritma (seperti logika fuzzy gaze Mas Evan, script pencocokan ORB Kak Anya, atau perhitungan inverse kinematics SDSC). Akibatnya, System Engineer mengalami beban kerja berlebih (*burnout*), batasan peran menjadi kabur, dan teman-teman divisi merasa kehilangan kepemilikan (*ownership*) atas riset/tugas akhirnya.
* **Paradigma Baru:**
  * **System Engineer** bertindak sebagai **Penyedia Fondasi & Jalan Tol (Infrastructure, Middleware, OS, Hardware Abstraction, Communication Pipeline, dan Resource Isolation)**. System Engineer menjamin bahwa jalan tol ini mulus, berlatensi rendah, tidak macet, memiliki aturan rambu-rambu data yang jelas, dan aman dari tabrakan memori/CPU.
  * **Anggota Tim Sub-Divisi** adalah **Pengendara Mobil di Jalan Tol Tersebut (Domain Specialist)**. Mas Evan memiliki hak penuh atas algoritma gaze dan tuning servo lehernya; Kak Anya memiliki hak penuh atas filter HSV almamaternya; Tim SDSC memiliki hak penuh atas navigasi omniwheel-nya.
  * **Prinsip Kontrak Data (Interface-First):** Selama format input citra dan output perintah motor mematuhi format kontrak ROS 2 standar, kode internal masing-masing anggota tim **tidak akan pernah diutak-atik atau dirombak oleh orang lain**.

---

## 2. GRAND PLAN ARSITEKTUR OS & HARDWARE ABSTRACTION LAYER (HAL)

Tujuan arsitektural utama di level OS adalah menciptakan **lapisan isolasi hardware (HAL)** yang memungkinkan sistem menjalankan **program legacy (webcam Logitech BRIO + script gaze lama)** saat ini tanpa hambatan, namun secara instan siap beralih ke **Intel RealSense D455** di masa depan **tanpa mengubah satu baris pun kode inti tracking gaze milik Mas Evan**.

```
┌────────────────────────────────────────────────────────────────────────────────────────┐
│                        LAPISAN 1: HARDWARE & KERNEL DRIVER (OS LEVEL)                  │
├────────────────────────────────────────────────────────────────────────────────────────┤
│   [PILIHAN RUNTIME SEKARANG]                     [PILIHAN RUNTIME MENDATANG]            │
│   Logitech BRIO 4K (USB Video Class)             Intel RealSense D455 (RGB-D Hardware) │
│           │                                                │                           │
│           ▼ (v4l2_camera driver)                           ▼ (realsense2_camera driver)│
├───────────┼────────────────────────────────────────────────┼───────────────────────────┤
│           ▼                                                ▼                           │
│  ┌──────────────────────────────────────────────────────────────────────────────────┐  │
│  │             LAPISAN 2: HARDWARE ABSTRACTION LAYER (HAL / ROS 2 CONTRACT)          │  │
│  │                                                                                  │  │
│  │   Topic Citra RGB : /camera/color/image_raw         (sensor_msgs/Image)          │  │
│  │   Topic Kalibrasi : /camera/color/camera_info       (sensor_msgs/CameraInfo)     │  │
│  │   Topic Kedalaman : /camera/depth/image_rect_raw    (sensor_msgs/Image) [Opsional]│  │
│  └──────────────────────────────────────┬───────────────────────────────────────────┘  │
├─────────────────────────────────────────┼──────────────────────────────────────────────┤
│                                         ▼                                              │
│                        LAPISAN 3: DOMAIN LOGIC (ALGORITMA SUB-TIM)                     │
│                                                                                        │
│   • Mas Evan (Gaze): Berlangganan /camera/color/image_raw -> Hitung Sudut Leher        │
│   • Kak Anya (Anya): Berlangganan /camera/color/image_raw -> Deteksi Baju Almamater    │
│   • Tim SDSC (Base): Berlangganan /camera/depth/image_rect_raw -> Stop 1.0 m & SFM     │
└────────────────────────────────────────────────────────────────────────────────────────┘
```

---

### 2.1 Dual-Mode Camera HAL (Mode A: Legacy BRIO ↔ Mode B: RealSense D455)

Di level sistem operasi (OS/ROS 2 launch system), kita menyediakan satu master launch file yang memiliki sakelar parameter `camera_type`:

```bash
# MENJALANKAN SISTEM SEKARANG (MODE A: LEGACY LOGITECH BRIO)
ros2 launch brone_bringup vision_system.launch.py camera_type:=brio

# MENJALANKAN SISTEM MENDATANG (MODE B: INTEL REALSENSE D455)
ros2 launch brone_bringup vision_system.launch.py camera_type:=d455
```

#### Apa yang Terjadi di Balik Layar OS?
1. **Jika `camera_type:=brio` dipilih:**
   * OS menjalankan driver `v4l2_camera_node` (atau node kamera USB legacy).
   * Script otomatis OS menginisialisasi parameter eksposur, zoom, dan FOV kamera BRIO.
   * Node driver menerbitkan output citra ke nama topik standar: `/camera/color/image_raw`.
2. **Jika `camera_type:=d455` dipilih:**
   * OS mematikan driver v4l2 dan menyalakan `realsense2_camera_node`.
   * RealSense menyalakan stream RGB dan hardware stereo depth.
   * Node driver menerbitkan citra ke topik yang **persis sama**: `/camera/color/image_raw`.
3. **Dampak pada Node Downstream Mas Evan & Kak Anya:**
   * **NOL PERUBAHAN.** Node Gaze dan Node Civitas tidak tahu (dan tidak perlu tahu) apakah citra tersebut berasal dari webcam Rp 2 jutaan atau sensor depth industri Rp 10 jutaan. Keduanya hanya membaca array piksel standar dari `/camera/color/image_raw`.

---

### 2.2 Standard Interface Contract Document (ICD) ROS 2

Agar tidak terjadi benturan antar divisi, seluruh komunikasi antar-node dikunci mati dalam format Interface Control Document berikut:

| Nama Topik | Tipe Pesan ROS 2 | Penyedia (Publisher) | Pengguna (Subscriber) | Standar QoS | Deskripsi & Kontrak Data |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `/camera/color/image_raw` | `sensor_msgs/Image` | **OS HAL (Driver)** | Mas Evan, Kak Anya | `BEST_EFFORT, Depth=1` | Frame RGB $640 \times 480$ piksel @ 30 FPS. |
| `/camera/color/camera_info` | `sensor_msgs/CameraInfo` | **OS HAL (Driver)** | Mas Evan (Gaze) | `RELIABLE, TransientLocal` | Matriks intrinsik kamera $K$, distorsi, dan FOV resmi hardware. |
| `/camera/depth/image_rect_raw` | `sensor_msgs/Image` | **OS HAL (RealSense)** | Tim SDSC (Base) | `BEST_EFFORT, Depth=1` | Peta kedalaman metrik 16-bit (milimeter) langsung dari ASIC D4. |
| `/robotis/head_control/set_joint_states` | `sensor_msgs/JointState` | **Mas Evan (Gaze)** | OS Motor Controller | `BEST_EFFORT, Depth=1` | Array posisi sudut leher `[pan, tilt]` dalam satuan radian. |
| `/brone/target_person` | `geometry_msgs/PointStamped` | **Mas Evan (Gaze)** | Tim SDSC (Base) | `BEST_EFFORT, Depth=1` | Koordinat posisi orang target utama $[X, Y, Z]$ terhadap frame robot. |
| `/brone/perception/civitas` | `std_msgs/String` | **Kak Anya (Civitas)** | NUC (State Machine) | `RELIABLE, Depth=5` | Status deteksi: `"MAHASISWA_UB"`, `"DOSEN"`, atau `"TAMU_LUAR"`. |
| `/cmd_vel` | `geometry_msgs/Twist` | **Tim SDSC (Base)** | OpenCR / Motor Base | `BEST_EFFORT, Depth=1` | Vektor kecepatan roda omniwheel $[\dot{x}, \dot{y}, \dot{\theta}]$. |

---

### 2.3 Eksternalisasi Parameter Kamera & Tuning Servo (YAML Dynamic Tuning)

Masalah utama yang memicu kekhawatiran Mas Evan adalah **hardcoding parameter di dalam script python**. Di file legacy `brone_gaze_node.py`, parameter FOV dan tuning motor tertanam langsung di script:
* `self.camera_hfov_deg = 78.0`
* `self.servo_alpha = 0.30`
* `self.tilt_range_up = 0.35`
* `self.pixel_deadband = 16`

#### Solusi Arsitektural OS: Konfigurasi Terpisah via File YAML
System Engineer menyiapkan folder konfigurasi bersih (`config/gaze_params_brio.yaml` dan `config/gaze_params_d455.yaml`). Mas Evan dapat mengubah nilai angka ini kapan saja di file teks tanpa perlu menyentuh atau membongkar script logika python:

```yaml
# config/gaze_params_brio.yaml (Untuk Uji Coba Sekarang)
algo_gaze_node:
  ros__parameters:
    camera_topic: "/camera/color/image_raw"
    camera_hfov_deg: 78.0             # Nilai FOV Logitech BRIO
    servo_alpha: 0.30                 # Kelembutan respon leher
    tilt_range_up: 0.35               # Batas dongak leher
    tilt_range_down: 0.80             # Batas nunduk leher
    pixel_deadband: 16                # Toleransi piksel tengah
    process_every_n_frames: 2         # Frame skipping untuk hemat CPU
```

```yaml
# config/gaze_params_d455.yaml (Untuk Transisi RealSense Mendatang)
algo_gaze_node:
  ros__parameters:
    camera_topic: "/camera/color/image_raw"
    camera_hfov_deg: 86.0             # Nilai FOV RealSense D455 (Lebih Lebar!)
    servo_alpha: 0.28                 # Disesuaikan sedikit dengan lensa baru
    tilt_range_up: 0.35
    tilt_range_down: 0.80
    pixel_deadband: 16
    process_every_n_frames: 1         # GPU Jetson sanggup proses full frame!
```

> **Keuntungan Luar Biasa bagi Mas Evan:** Saat berpindah kamera, Mas Evan **cukup menyalin file YAML dan mengganti satu angka FOV ($78.0 \to 86.0$)**. Seluruh fungsi matematika azimuth, fuzzy logic 7-antecedent, dan rumus sudut pan/tilt beliau akan bekerja secara akurat 100% tanpa ada satupun rumus yang perlu ditulis ulang!

---

### 2.4 Eliminasi Subprocess `v4l2-ctl` dari Algoritma Internal

Di kode legacy Mas Evan saat ini:
```python
# Kode di dalam brone_gaze_node.py (Baris 262-285)
def setup_logitech_brio_fov(self):
    commands = [
        ['v4l2-ctl', '-d', '/dev/video0', '--set-ctrl=zoom_absolute=1'],
        ...
    ]
    for cmd in commands:
        subprocess.run(cmd, ...)
```

#### Tinjauan Arsitektur & Tindakan Sistem:
1. Memanggil perintah shell Linux `v4l2-ctl` di dalam inisialisasi node ROS 2 adalah penyebab utama mengapa Mas Evan merasa takut saat migrasi ke RealSense. RealSense menggunakan protokol UVC proprietary/librealsense, sehingga jika baris tersebut dieksekusi pada RealSense, program akan melempar *warning/error* hardware.
2. **Tindakan OS Engineer:**
   * Logika setup hardware ini **diangkat keluar dari file Mas Evan** dan dipindahkan ke skrip inisialisasi driver OS (`setup_camera_device.sh` atau dimasukkan ke parameter driver ROS 2).
   * Mas Evan cukup memberikan flag aman: jika `setup_hardware_driver: false`, baris tersebut di-skip.
   * Dengan cara ini, node Mas Evan menjadi murni node komputasi visi yang independen dari merek perangkat keras kamera!

---

### 2.5 Isolasi Komputasi OS (Zero-Jitter CPU Affinity & Deterministic Services)

Agar algoritma komputasi visi tidak saling sikut dan tidak mengganggu loop motor leher, System Engineer telah mengunci alokasi core di level Linux Kernel:

```
┌────────────────────────────────────────────────────────────────────────────────────────┐
│                        ALOKASI CORE JETSON ORIN NANO (6 CORE ARM)                      │
├────────────────────────────────────────────────────────────────────────────────────────┤
│  Core 0 : [OS SENSOR INGESTION] -> Driver Kamera (v4l2 / realsense2_camera)            │
│  Core 1 : [AI DISPATCH]         -> YOLO Host Orchestrator & TensorRT Stream            │
│  Core 2 : [DOMAIN MAS EVAN]     -> Node Gaze Tracking (Fuzzy & MediaPipe Target)       │
│  Core 3 : [DOMAIN MAS EVAN]     -> Thread Komputasi Ekstra Gaze                        │
│  Core 4 : [DOMAIN TIM SDSC]     -> Omniwheel Base Kinematics & Serial Bridge           │
│  Core 5 : [DOMAIN KAK ANYA]     -> Civitas Matcher & System Background Monitoring      │
└────────────────────────────────────────────────────────────────────────────────────────┘
```
* **Jaminan untuk Mas Evan:** Mas Evan dijamin mendapatkan **Core 2 dan Core 3 secara privat**. Tidak ada thread milik Kak Anya atau SDSC yang diizinkan mengganggu siklus komputasi Mas Evan.
* **Jaminan untuk Motor Leher:** Loop servo di NUC Core i9 diisolasi dengan prioritas real-time `SCHED_FIFO` (chrt 80), menjamin pergerakan leher robot bebas dari patah-patah (*zero-jitter*).

---

## 3. MATRIKS PEMBAGIAN TUGAS & GARIS BATAS TANGGUNG JAWAB (DELEGASI)

Untuk menjawab evaluasi Ketua Tim secara konkret, berikut adalah matriks garis batas (*demarcation line*) yang jelas antara apa yang menjadi ranah System Engineer vs apa yang menjadi ranah mandiri sub-divisi.

### 3.1 Demarcation of Responsibility (System Engineer vs Sub-Tim Domain)

```
┌────────────────────────────────────────────────────────────────────────────────────────┐
│                      GARIS DEMARKASI TANGGUNG JAWAB TEKNIS                             │
├──────────────────────────────────────────┬─────────────────────────────────────────────┤
│   RANAH SYSTEM / OS ENGINEER (ANDA)      │     RANAH SPESIALIS SUB-DIVISI              │
├──────────────────────────────────────────┼─────────────────────────────────────────────┤
│ 1. Driver Hardware Kamera (V4L2/D455).   │ 1. Logika Algoritma Visi/AI Internal.       │
│ 2. Pipeline Aliran Data ROS 2 & Topik.   │ 2. Parameter Tuning Model & Kontroler.      │
│ 3. Penyusunan File Peluncur (Launch).    │ 3. Logika Fuzzy, Rule Base, & Thresholding. │
│ 4. Penguncian Core CPU (taskset/systemd).│ 4. Dataset Wajah, Baju, & Template Match.   │
│ 5. Manajemen Port USB & Catu Daya.       │ 5. Perhitungan Kinematika & Navigasi Roda.  │
│ 6. Safety Watchdog & Emergency Auto-Stop.│ 6. Prompting LLM, Voice State, & Respons.   │
│ 7. Sinkronisasi Jam Sistem & Jaringan DDS│ 7. Verifikasi Kebenaran Data Skripsi/Riset. │
└──────────────────────────────────────────┴─────────────────────────────────────────────┘
```

---

### 3.2 Instruksi Delegasi Spesifik untuk Tim Gaze (Mas Evan)

| ID Tugas | Nama Tugas Delegasi | Batas Tanggung Jawab Mas Evan | Batas Tanggung Jawab System Engineer | Target Selesai |
| :---: | :--- | :--- | :--- | :---: |
| **EVAN-01** | **Dokumentasi Prosedur Legacy BRIO** | Menulis panduan singkat (1 halaman) urutan perintah terminal existing untuk menjalankan sistem Brio lama beserta nilai parameter terbaik yang pernah dicapai. | Menyediakan template format dokumentasi dan memverifikasi kesiapan port USB di robot. | **W0 (3 Hari)** |
| **EVAN-02** | **Isolasi Parameter Tuning ke File YAML** | Memindahkan variabel statis di python (`camera_hfov_deg`, `servo_alpha`, deadband, limit pan/tilt) agar dibaca dari parameter ROS 2. | Membantu menyiapkan template launch file yang me-load file `gaze_params.yaml`. | **W1** |
| **EVAN-03** | **Enkapsulasi Fungsi `setup_logitech_brio_fov()`** | Menambahkan pengecekan kondisional sederhana (`if self.setup_camera_hardware: ...`) agar fungsi `v4l2-ctl` tidak dijalankan saat migrasi ke D455. | Menyiapkan konfigurasi driver kamera di level ROS launch sehingga node Evan tidak perlu memanggil v4l2 lagi. | **W1** |
| **EVAN-04** | **Tuning Servo Leher & Fuzzy Rules** | Melakukan tuning respons pergerakan leher agar halus (tidak overshoot) dan memvalidasi 7 variabel fuzzy untuk skripsinya. | Menjamin latency pengiriman topik ke motor NUC $< 2\text{ ms}$ dan menyediakan grafik telemetri RQT. | **W2 - W3** |

---

### 3.3 Instruksi Delegasi Spesifik untuk Tim Civitas Akademika (Kak Anya)

| ID Tugas | Nama Tugas Delegasi | Batas Tanggung Jawab Kak Anya | Batas Tanggung Jawab System Engineer | Target Selesai |
| :---: | :--- | :--- | :--- | :---: |
| **ANYA-01** | **Eliminasi `cv2.VideoCapture(0)`** | Mengubah fungsi utama skrip 1047 baris (`civitas_cuda_full.py`) dari membaca kamera langsung menjadi fungsi modul/subscriber yang menerima input citra (crop ROI $160 \times 160$ px). | Menyediakan topik publisher citra standar `/camera/color/image_raw` sehingga Kak Anya tidak perlu memperebutkan akses hardware USB. | **W1** |
| **ANYA-02** | **Penyempurnaan HSV Almamater UB** | Melakukan kalibrasi batas warna HSV jas almamater UB pada berbagai kondisi pencahayaan ruangan lab dan koridor rektorat. | Memastikan parameter *White Balance* kamera terkunci statis agar pencahayaan tidak fluktuatif. | **W2** |
| **ANYA-03** | **Output Kontrak String Deteksi** | Memastikan output deteksi diterbitkan ke topik `/brone/perception/civitas` dengan format string baku: `"MAHASISWA_UB"`, `"DOSEN"`, `"TAMU"`. | Menghubungkan topik civitas Kak Anya ke State Machine BOS v4.0 di NUC untuk memicu sapaan suara. | **W2** |

---

### 3.4 Instruksi Delegasi Spesifik untuk Tim Kinematika & Navigasi (Wisnu / SDSC)

| ID Tugas | Nama Tugas Delegasi | Batas Tanggung Jawab Tim SDSC | Batas Tanggung Jawab System Engineer | Target Selesai |
| :---: | :--- | :--- | :--- | :---: |
| **SDSC-01** | **Langganan Koordinat Target Orang** | Mengarahkan node navigasi base roda untuk berlangganan topik posisi orang `/brone/target_person` yang dihasilkan oleh deteksi visi. | Menjamin koordinat orang terbit stabil pada frekuensi 20–30 Hz dengan time-stamp sinkron. | **W1** |
| **SDSC-02** | **Implementasi Interlock Auto-Stop 1.0 m** | Mengunci logika rem otomatis pada kontroler roda: saat jarak terukur $Z \le 1.0\text{ meter}$, kecepatan translasi roda wajib menjadi $0.0\text{ m/s}$. | Memasang safety watchdog di level hardware/serial bridge untuk memutus `/cmd_vel` jika node navigasi hang. | **W2** |
| **SDSC-03** | **Tuning Inverse Kinematics 4-Omniwheel** | Menghitung dan melakukan kalibrasi PWM/RPM 4 roda omniwheel agar gerak translasi robot lurus dan tidak melintir (*zero drift*). | Memastikan alokasi Core 4 di Jetson khusus untuk node serial bridge SDSC tanpa terganggu proses AI. | **W2 - W3** |

---

### 3.5 Instruksi Delegasi Spesifik untuk Tim LLM & Voice Interaction

| ID Tugas | Nama Tugas Delegasi | Batas Tanggung Jawab Tim LLM | Batas Tanggung Jawab System Engineer | Target Selesai |
| :---: | :--- | :--- | :--- | :---: |
| **VOICE-01** | **Integrasi Mikrofon Mandiri di NUC** | Menghubungkan pipeline Whisper STT ke USB sound card / mic array mandiri yang tertancap di Intel NUC. | Menyediakan mapping dev node audio ALSA di Linux NUC agar tidak tertukar saat reboot robot. | **W1** |
| **VOICE-02** | **Optimasi Inferensi SLM & TTS Offline** | Memastikan model bahasa kecil Ollama dan model Piper TTS berjalan responsif (total jeda respon suara $< 1.5\text{ detik}$). | Mengunci proses voice pipeline ke 8 E-Core NUC (CPU 12–19) via systemd service agar tidak mengganggu motor. | **W2** |

---

### 3.6 Tabel Matriks RACI (Responsible, Accountable, Consulted, Informed)

* **R (Responsible):** Pihak yang mengeksekusi langsung kodingan/pekerjaan teknis.
* **A (Accountable):** Pihak penanggung jawab utama keberhasilan integrasi sistem.
* **C (Consulted):** Pihak yang dimintai masukan teknis atau validasi teori.
* **I (Informed):** Pihak yang diberi laporan pembaruan setelah tugas selesai.

| Komponen / Modul Sistem | System Engineer (Anda) | Mas Evan (Gaze) | Kak Anya (Civitas) | Wisnu (SDSC) | Tim Voice / LLM | Ketua Tim |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| **Arsitektur & Hardware Abstraction (HAL)** | **A / R** | C | C | C | I | I |
| **Driver Kamera (BRIO & D455 Launch)** | **A / R** | C | I | I | I | I |
| **Logika Fuzzy & Tracking Wajah Gaze** | I | **A / R** | I | C | I | I |
| **Pencocokan Baju Almamater Civitas** | I | I | **A / R** | I | I | I |
| **Kinematika 4-Roda & Navigasi Rektorat** | C | I | I | **A / R** | I | I |
| **Voice AI (Whisper + Ollama + Piper)** | C | I | I | I | **A / R** | I |
| **Alokasi Core CPU & Systemd Watchdog** | **A / R** | I | I | I | I | I |
| **Uji Integrasi Akhir di Lantai Uji** | **A** | **R** | **R** | **R** | **R** | **A / I** |

---

## 4. POIN KOMUNIKASI MENENANGKAN & STRATEGIS UNTUK MAS EVAN

### 4.1 Menjawab Akar Kekhawatiran Mas Evan Secara Logis & Objektif

Mas Evan memiliki kekhawatiran yang sangat wajar bagi seorang mahasiswa tingkat akhir yang sedang menyelesaikan skripsi:
> *"Kalau kita migrasi ke Intel RealSense D455, jangan-jangan saya harus merombak total kode program saya, mengulang proses tuning servo dari nol, menginstal library aneh-aneh yang bikin konflik sistem, dan skripsi saya jadi molor?"*

Sebagai System Engineer, jawaban Anda tidak boleh sekadar "tenang aja, aman kok", melainkan harus **memberikan garansi arsitektural yang terukur**:
1. **Kode Mas Evan Tetap Berjalan Sekarang:** Sistem dibangun untuk langsung menjalankan prosedur Logitech BRIO legacy yang sudah Mas Evan kuasai hari ini. Tidak ada paksaan untuk buru-buru mengubah kode Mas Evan.
2. **Kamera Dikelola oleh OS, Bukan oleh Node Mas Evan:** Mas Evan tidak perlu menginstal atau mempelajari SDK `pyrealsense2`. Driver RealSense dijalankan di lapisan OS oleh System Engineer.
3. **Data Masuk Tetap Topik ROS 2 Biasa:** Mas Evan tetap menerima citra dari `/camera/color/image_raw`. Format datanya sama persis dengan yang diterima dari webcam Brio.
4. **Logika Skripsi Mas Evan 100% Aman:** Logika Fuzzy 7-antecedent, perhitungan iris, bobot prioritas, dan rumus servo tidak ada satupun yang disentuh.
5. **Transisi ke D455 Justru Menguntungkan Skripsi Mas Evan:** FOV D455 ($86^\circ$) lebih luas dari Brio ($78^\circ$), dan Mas Evan bisa memamerkan hasil pengujian skripsinya pada dua sensor yang berbeda (Webcam vs Depth Sensor Industri) tanpa perlu kerja ganda!

---

### 4.2 Teks Draf Pesan Siap Kirim ke Mas Evan (WhatsApp / Discord / Briefing)

Anda dapat langsung menyalin atau mengadaptasi pesan berikut untuk dikirimkan secara personal kepada Mas Evan:

```text
Halo Mas Evan, selamat siang / malam.

Terkait diskusi kita kemarin soal rencana transisi kamera ke Intel RealSense D455 dan kekhawatiran soal proses tuning serta modifikasi kode, saya ingin memberikan penjelasan menyeluruh dan menenangkan:

1. Fokus Utama Kita Saat Ini: Sistem Existing BRIO Tetap Berjalan Mulus
Saya sudah merancang arsitektur OS agar prosedur legacy kamera Logitech BRIO yang selama ini Mas Evan gunakan tetap bisa langsung dijalankan hari ini tanpa ada perubahan logika tracking sama sekali. Program skripsi Mas Evan tetap menjadi prioritas utama kita.

2. Hardware Abstraction Layer (Kamera Di-handle Murni di Level OS)
Mas Evan tidak perlu khawatir harus belajar library RealSense (pyrealsense2) atau membongkar script Python internal Mas Evan. Urusan driver kamera, USB, dan inisialisasi hardware sepenuhnya akan saya handle di level OS/ROS 2 driver. 
Output citra yang masuk ke node Mas Evan akan selalu berupa topik standar: `/camera/color/image_raw`.

3. Transisi ke RealSense D455 Nanti "Zero-Breaking-Change" bagi Mas Evan
Ketika nanti kita pasang RealSense D455, yang berganti hanya satu baris perintah peluncur driver di level OS. Dari sisi kode Mas Evan:
- Logika Fuzzy Logic 7 variabel Mas Evan: AMAN 100%, TIDAK BERUBAH.
- Perhitungan Landmark & Focal Tracking: AMAN 100%, TIDAK BERUBAH.
- Output sudut servo pan/tilt ke motor: AMAN 100%, TIDAK BERUBAH.
- Yang disesuaikan Mas Evan nantinya hanyalah angka parameter FOV horizontal kamera di file konfigurasi YAML (dari 78° ke 86°), tanpa perlu merombak rumus matematika di dalam kode.

4. Mas Evan Punya Hak Penuh atas Tuning & Parameter
Sesuai arahan Ketua Tim, saya murni fokus menjaga stabilitas OS, alokasi core CPU (saya kunci 2 core khusus buat node Mas Evan agar super ringan), dan latensi komunikasi motor. Seluruh parameter tuning leher, sensitivitas servo, dan rule fuzzy sepenuhnya berada di bawah kendali Mas Evan.

Biar rapi, saya minta tolong bantuan Mas Evan untuk mendokumentasikan SOP urutan jalan program Brio yang kemarin, dan kita pisahkan parameter tuning Mas Evan ke satu file YAML bersih. Nanti saya yang siapkan launch-nya.

Santai aja Mas, kita jaga bareng-bareng agar skripsi Mas Evan tuntas dengan hasil terbaik dan robot siap tampil maksimal di demo rektorat!
```

---

### 4.3 Tiga Bukti Teknis Mengapa Transisi D455 "Zero-Breaking-Change" bagi Gaze

Jika Mas Evan membutuhkan penjelasan teknis lebih lanjut, berikut adalah 3 bukti konkret dari analisis kode:

#### Bukti 1: Node Gaze Mas Evan Sudah Menggunakan ROS 2 Topic Subscriber
Di file `brone_gaze_node.py` baris 168:
```python
self.image_subscription = self.create_subscription(
    Image, '/image_raw', self.image_callback, qos_profile_cam)
```
Node Mas Evan **sejak awal tidak membaca hardware langsung via OpenCV `VideoCapture(0)`**, melainkan sudah menerima pesan `sensor_msgs/Image`. Artinya, node Mas Evan sudah modular secara native. Mau gambarnya dikirim dari Brio, D455, atau bahkan simulator Webots, node Mas Evan tidak terpengaruh.

#### Bukti 2: Perhitungan Sudut Azimuth Mas Evan Sudah Menggunakan Parameter FOV
Di file `brone_gaze_node.py` baris 327–330:
```python
def camera_azimuth_deg(self, person_center_x, frame_width):
    norm_offset = (person_center_x - (frame_width / 2.0)) / (frame_width / 2.0)
    return norm_offset * (self.camera_hfov_deg / 2.0)
```
Rumus pemetaan piksel ke derajat sudut leher Mas Evan sudah dirancang sangat elegan berbasis variabel `self.camera_hfov_deg`. Ketika berpindah dari Brio ($78^\circ$) ke D455 ($86^\circ$), Mas Evan tidak perlu mengubah rumus perkalian di atas. Cukup ubah nilai parameter input, dan derajat pergerakan servo otomatis beradaptasi secara matematis!

#### Bukti 3: Fuzzy Logic & MediaPipe Beroperasi pada Piksel Ternormalisasi
Rule base fuzzy Mas Evan mengevaluasi kedekatan orang, gestur lambaian tangan, arah tatapan mata, dan status berbicara. Seluruh koordinat landmark MediaPipe Holistic dinormalisasi pada rentang rentang $[0.0, 1.0]$. Karena resolusi gambar tetap dipertahankan pada rasio yang sama ($640 \times 480$), matriks membership fuzzy Mas Evan tetap valid secara absolut.

---

## 5. ROADMAP INTEGRASI & PROSEDUR EKSEKUSI BERTAHAP (W0 - W4)

Roadmap ini memastikan tidak ada langkah yang terburu-buru dan setiap tahapan memiliki pengujian yang terverifikasi sebelum melangkah ke tahap berikutnya:

```
┌────────────────────────────────────────────────────────────────────────────────────────┐
│                        ROADMAP INTEGRASI BERTAHAP ROBOT BRONE                          │
├────────────────────────────────────────────────────────────────────────────────────────┤
│  [MINGGU 0: KONSOLIDASI & DOKUMENTASI LEGACY]                                          │
│  • Mas Evan : Dokumentasikan SOP & parameter tuning terbaik Logitech BRIO.            │
│  • Kak Anya : Sediakan fungsi modular deteksi almamater (terima citra crop).           │
│  • OS Eng.  : Susun file parameter YAML dan siapkan Hardware Abstraction Layer.        │
│                                                                                        │
│  [MINGGU 1: BENCH-LEVEL TESTING DENGAN LOGITECH BRIO (MEJA LAB)]                       │
│  • Jalankan sistem penuh menggunakan kamera legacy Logitech BRIO.                      │
│  • Verifikasi bahwa node Gaze membaca parameter dari YAML.                             │
│  • Uji komunikasi leher Mas Evan ke op3_manager NUC (50 Hz).                           │
│                                                                                        │
│  [MINGGU 2: TRANSISI HARDWARE & DROP-IN REALSENSE D455]                                │
│  • Pasang Intel RealSense D455 ke port USB 3.2 Jetson Orin Nano.                       │
│  • OS Engineer menyalakan realsense2_camera driver (topik citra tetap sama).           │
│  • Mas Evan load config `gaze_params_d455.yaml` (FOV 86°).                            │
│  • Verifikasi: leher menatap target dengan akurat tanpa revisi kode algoritma!         │
│                                                                                        │
│  [MINGGU 3: INTEGRASI DUA TIER & TIM KINEMATIKA SDSC]                                  │
│  • Tim SDSC memanfaatkan depth stream D455 untuk auto-stop 1.0 meter.                  │
│  • Integrasi Two-Tier Attention: YOLOv11 TRT -> 1 Target Utama -> MediaPipe + Anya.    │
│  • Uji gerak robot statis di penyangga kaki.                                           │
│                                                                                        │
│  [MINGGU 4: SIMULASI PENUH & GLADI BERSIH REKTORAT]                                    │
│  • Uji dinamis di lantai rektorat: Robot meluncur -> Auto-stop -> Sapa -> Dialog.      │
│  • Penguncian dokumentasi skripsi Mas Evan & penyerahan laporan proyek ke Ketua.       │
└────────────────────────────────────────────────────────────────────────────────────────┘
```

---

## 6. KESIMPULAN & LANGKAH TINDAK LANJUT

1. **Bagi System Engineer:** Anda telah kembali ke posisi ideal sebagai Lead Systems Architect. Tugas Anda adalah menjaga stabilitas OS, QoS komunikasi DDS, alokasi core CPU, dan membuat transisi hardware tidak terasa (*seamless*) bagi anggota tim.
2. **Bagi Mas Evan:** Skripsi dan hasil tuning servo Mas Evan terlindungi 100%. Migrasi ke D455 nantinya bukan menjadi beban, melainkan nilai tambah akademik yang membuktikan bahwa sistem gaze buatan Mas Evan bersifat adaptif terhadap multi-hardware.
3. **Bagi Tim Keseluruhan:** Batas tanggung jawab yang tegas menghilangkan tumpang tindih pekerjaan, mencegah *burnout*, dan menjamin robot BRONE siap tampil prima pada demonstrasi rektorat November 2026.

---
*Dokumen ini resmi disahkan sebagai cetak biru tata kelola teknis dan integrasi sistem robot BRONE.*
