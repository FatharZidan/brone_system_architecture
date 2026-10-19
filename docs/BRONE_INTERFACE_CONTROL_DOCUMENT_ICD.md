# 📄 INTERFACE CONTROL DOCUMENT (ICD): ROBOT BRONE (v1.0)
## *Standard System Contract, ROS 2 Middleware QoS, Coordinate Frames, & Failsafe Interlocks*

---

> **Dokumen Resmi:** BRONE-ICD-2026-v1.0  
> **Klasifikasi:** Dokumen Kontrak Teknis Antarmuka Sistem  
> **Otoritas:** Lead Systems, Middleware, OS & Integration Engineer  
> **Target Sub-Sistem:** 
> 1. Ingestion & Camera Hardware Abstraction Layer (HAL)  
> 2. Gaze Perception Subsystem (Mas Evan)  
> 3. Civitas Perception Subsystem (Kak Anya)  
> 4. Mobile Base Omniwheel Subsystem (Tim SDSC)  
> 5. Whole-Body Kinematics & ZMP Balance Subsystem (Tim Kinematika)  
> 6. Motor Kernel & Supervisor Subsystem (Intel NUC op3_manager & BOS v4.0)  
> **Rujukan Standar:** *IEEE 12207 Systems Engineering*, *Science Robotics (Macenski et al. 2022)*, & *IEEE Transactions (Xu et al. & Cheng et al. 2024)*  

---

## 1. TUJUAN & RUANG LINGKUP DOKUMEN

Dokumen Kontrak Antarmuka (ICD) ini menetapkan **spesifikasi teknis baku dan tidak dapat diubah sepihak (*binding contract*)** untuk seluruh pertukaran data antar-modul pada robot BRONE. 

Setiap pengembang sub-sistem (Vision, Kinematika, Base, dan Supervisor) diwajibkan mematuhi:
1. Nama topik dan tipe pesan ROS 2 yang terdaftar.
2. Satuan metrik dan sistem koordinat kartesian standar.
3. Batas frekuensi sampling dan Quality of Service (QoS).
4. Protokol pemutusan darurat (*safety interlocks*).

---

## 2. STANDAR SISTEM KOORDINAT & FRAME IDENTIFIER

Seluruh koordinat spasial pada robot BRONE mengacu pada konvensi **REP-103 (Standard Units of Measure & Coordinate Conventions)** dan **REP-105 (Mobile Robot Coordinate Frames)**:

```
          Z (Atas)                      Z (Atas)
          ▲                             ▲
          │                             │   X (Depan Kamera / Optical Axis)
          │                             │  /
          └───► X (Depan Robot)         └───► Y (Kiri)
         /
        ▼ Y (Kiri Robot)
   [FRAME: base_link]              [FRAME: camera_link]
```

1. **`base_link` (Frame Pusat Sasis 4-Omniwheel):**
   * **Sumbu X (+):** Mengarah lurus ke depan robot.
   * **Sumbu Y (+):** Mengarah ke sisi kiri robot.
   * **Sumbu Z (+):** Mengarah tegak lurus ke atas (melawan gravitasi).
   * **Satuan:** Meter ($\text{m}$) untuk posisi, Radian ($\text{rad}$) untuk orientasi, $\text{m/s}$ untuk kecepatan linear.
2. **`camera_link` (Frame Pusat Sensor Optik Leher):**
   * **Sumbu Z (+):** Jarak kedalaman metrik riil (*Depth Axis* / mengarah keluar lensa ke target orang).
   * **Sumbu X (+):** Deviasi horizontal target terhadap titik tengah lensa (kanan-kiri).
   * **Sumbu Y (+):** Deviasi vertikal target terhadap titik tengah lensa (atas-bawah).

---

## 3. MATRIKS KONTRAK DATA & ANTARMUKA TOPIK ROS 2

Setiap pertukaran data wajib mematuhi tabel Interface Control berikut:

| ID Kontrak | Nama Topik ROS 2 | Tipe Pesan | Frekuensi ($f_s$) | Profil QoS FastRTPS | Provider (Publisher) | Consumer (Subscriber) |
| :---: | :--- | :--- | :---: | :--- | :--- | :--- |
| **ICD-01** | `/camera/color/image_raw` | `sensor_msgs/Image` | 30 Hz | `Reliability: BEST_EFFORT`<br>`History: KEEP_LAST (1)` | **Camera HAL** (Jetson) | Mas Evan, Kak Anya |
| **ICD-02** | `/camera/color/camera_info` | `sensor_msgs/CameraInfo` | Latched | `Reliability: RELIABLE`<br>`Durability: TRANSIENT_LOCAL` | **Camera HAL** (Jetson) | Mas Evan (Gaze) |
| **ICD-03** | `/camera/depth/image_rect_raw` | `sensor_msgs/Image` | 30 Hz | `Reliability: BEST_EFFORT`<br>`History: KEEP_LAST (1)` | **Camera HAL** (D455) | Tim SDSC, Kinematika |
| **ICD-04** | `/brone/target_person` | `geometry_msgs/PointStamped` | 20–30 Hz | `Reliability: BEST_EFFORT`<br>`History: KEEP_LAST (1)` | **Mas Evan** (Gaze) | Tim SDSC, Kinematika |
| **ICD-05** | `/robotis/head_control/set_joint_states` | `sensor_msgs/JointState` | 30 Hz | `Reliability: BEST_EFFORT`<br>`History: KEEP_LAST (1)` | **Mas Evan** (Gaze) | `op3_manager` (NUC) |
| **ICD-06** | `/cmd_vel` | `geometry_msgs/Twist` | 20 Hz | `Reliability: BEST_EFFORT`<br>`History: KEEP_LAST (1)` | **Tim SDSC** (Base) | OpenCR Base Bridge |
| **ICD-07** | `/brone/perception/civitas` | `std_msgs/String` | Event | `Reliability: RELIABLE`<br>`History: KEEP_LAST (5)` | **Kak Anya** (Civitas) | BOS v4.0 (NUC) |
| **ICD-08** | `/state_machine/mode` | `std_msgs/String` | Event | `Reliability: RELIABLE`<br>`Durability: TRANSIENT_LOCAL` | **BOS v4.0** (NUC) | Seluruh Sub-Sistem |

---

## 4. SPESIFIKASI DETAIL PAYLOAD & BATASAN NILAI

### 4.1 ICD-04: Metadata Target Orang (`/brone/target_person`)
* **Header:**
  * `stamp`: Timestamp sinkronisasi frame gambar.
  * `frame_id`: `"camera_link"`
* **Point Coordinates:**
  * `point.x`: Offset deviasi lateral target ($[-1.5, +1.5]\text{ m}$).
  * `point.y`: Ketinggian target relatif terhadap lensa ($[-0.5, +0.5]\text{ m}$).
  * `point.z`: **Jarak kedalaman metrik riil** ($[0.5, 5.0]\text{ m}$).
* **Aturan Khusus:** Nilai $Z$ wajib diperoleh dari sensor kedalaman (D455) atau estimasi bounding box ternormalisasi (Brio).

### 4.2 ICD-05: Kontrol Sudut Leher (`/robotis/head_control/set_joint_states`)
* **Name Array:** `['head_pan', 'head_tilt']`
* **Position Array:** `[pan_rad, tilt_rad]`
* **Batasan Dinamis Keras (*Hard Safety Clamps*):**
  * $\text{pan\_rad} \in [-1.4, +1.4]\text{ rad}$ (Maksimum $\pm 80^\circ$)
  * $\text{tilt\_rad} \in [-0.80, +0.35]\text{ rad}$ (Maksimum nunduk $45^\circ$, dongak $20^\circ$)
  * Kecepatan putar sudut leher disaturasi: $|\dot{\theta}_{\text{pan}}| \le 45^\circ/\text{s}$ (Rujukan: *Xu et al. IEEE 2024*).

### 4.3 ICD-06: Kecepatan Gerak Roda Omniwheel (`/cmd_vel`)
* **Linear Velocity:**
  * `linear.x`: Kecepatan maju-mundur ($[-0.4, +0.4]\text{ m/s}$).
  * `linear.y`: Kecepatan geser lateral/strafe ($[-0.3, +0.3]\text{ m/s}$).
* **Angular Velocity:**
  * `angular.z`: Kecepatan putar sasis yaw ($[-0.5, +0.5]\text{ rad/s}$).
* **Batasan Akselerasi ZMP:** $\max |\ddot{x}| \le 0.5\text{ m/s}^2$ (Ditetapkan oleh Tim Kinematika ZMP).

---

## 5. PROTOKOL KESELAMATAN & FAILSAFE INTERLOCK (HARD REQUIREMENTS)

Seluruh pengembang wajib menerapkan logika pemutus keselamatan berikut:

```
                              [DATA KOORDINAT Z TARGET]
                                          │
                    ┌─────────────────────┴─────────────────────┐
                    ▼                                           ▼
             Z > 1.0 Meter                               Z <= 1.0 Meter
     [STATUS: APPROACH ZONE]                      [STATUS: AUTO-STOP INTERLOCK]
     • Roda SDSC diizinkan meluncur               • RODA TRANSLASI WAJIB 0.0 m/s
     • Leher tracking target aktif                • LEHER TETAP AKTIF MENATAP
                                                  • BOS memicu dialog suara sapaan!
```

1. **Safety Interlock Gate 1.0 Meter (Mandat Mutlak):**
   * Jika nilai $Z \le 1.0\text{ meter}$, kontroler roda SDSC **WAJIB memotong translasi murni**:
     $$\text{linear.x} = 0.0\text{ m/s}, \quad \text{linear.y} = 0.0\text{ m/s}$$
   * Pelanggaran terhadap batas ini berpotensi merusak integritas robot dan membahayakan tamu.
2. **Watchdog Timeout Jaringan & Kamera:**
   * Jika node navigasi SDSC tidak menerima pembaruan topik `/brone/target_person` selama $> 500\text{ ms}$, kecepatan roda **otomatis diset ke 0 (Emergency Deceleration)**.
3. **Graceful Hold pada Oklusi Wajah:**
   * Jika wajah orang terhalang sesaat ($< 1.5\text{ detik}$), servo leher dilarang bergerak kembali ke nol secara mendadak. Posisi terakhir wajib dipertahankan (*position hold*).

---

## 6. LEMBAR PENGESAHAN & GARIS DEMARKASI SUB-TIM

| Peran Sub-Sistem | Penanggung Jawab | Tanggung Jawab Kontrak | Batasan Terlarang |
| :--- | :--- | :--- | :--- |
| **Systems & OS Architect** | **FatharZidan (Anda)** | Menjamin stabilitas DDS, driver kamera HAL, latensi jaringan $< 2\text{ ms}$, dan alokasi CPU. | Dilarang mengutak-atik algoritma visi atau rumus kontrol internal tim. |
| **Gaze Perception Lead** | **Mas Evan** | Memenuhi kontrak ICD-04 & ICD-05, membaca parameter YAML, membatasi kecepatan leher $\le 45^\circ/\text{s}$. | Dilarang memanggil `v4l2-ctl` atau `pyrealsense2` di level kode algoritma. |
| **Civitas Perception Lead** | **Kak Anya** | Memenuhi kontrak ICD-07, menerima crop ROI dada ($160 \times 160$ px) dari ICD-01. | Dilarang membuka kamera via `cv2.VideoCapture(0)`. |
| **Omniwheel Base Lead** | **Tim SDSC (Wisnu)** | Memenuhi kontrak ICD-06, mengunci auto-stop $Z \le 1.0\text{ m}$, mematuhi batas akselerasi ZMP. | Dilarang memproses citra kamera video di modul base. |
| **Kinematika & Balance Lead** | **Tim Kinematika** | Menetapkan batas akselerasi aman $\ddot{x}_{\max}$ berbasis ZMP, meredam goyangan inersia badan. | Dilarang memutus pergerakan motor leher tanpa koordinasi dengan BOS. |

---
*Dokumen ini diterbitkan oleh Systems & OS Engineer sebagai cetak biru resmi integrasi robot BRONE.*
