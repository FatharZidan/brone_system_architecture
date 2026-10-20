# 📦 BRONE SYSTEM ARCHITECTURE & INTEGRATION INFRASTRUCTURE (v1.0)
## *Dedicated OS Middleware, Hardware Abstraction Layer (HAL), & Safe Testing Harness*

Paket ini adalah repositori arsitektur sistem independen yang dikembangkan oleh **Lead Systems & OS Engineer** untuk mengorkestrasi komponen hardware robot BRONE tanpa mengotak-atik kodingan domain sub-tim (Gaze Mas Evan, Civitas Kak Anya, Kinematika SDSC/Balance).

---

### 📂 Struktur Repositori

```
brone_system_architecture/
├── config/
│   ├── gaze_params_brio.yaml      # Parameter tuning kamera Logitech BRIO (Legacy Baseline)
│   └── gaze_params_d455.yaml      # Parameter tuning kamera Intel RealSense D455 (Next-Gen 30 FPS)
├── launch/
│   └── camera_hal.launch.py       # Master launch file: Sakelar satu perintah Brio vs D455
├── scripts/
│   └── setup_opencr_udev.sh       # Skrip otomatisasi izin port OpenCR (Hapus kebutuhan 'sudo bash')
├── docs/                          # Dokumen Arsitektur, ICD, Memo, dan Slide Presentasi
└── README.md                      # Dokumentasi teknis & panduan operasional
```

---

### 🚀 Cara Penggunaan Praktis

#### 1. Menjalankan Master Driver Kamera (Hardware Abstraction Layer)
Downstream node (Mas Evan, Kak Anya) selalu membaca dari topik yang sama: `/camera/color/image_raw`.

```bash
# OPSI A: Menjalankan Kamera Logitech BRIO (Sekarang)
ros2 launch brone_system_architecture camera_hal.launch.py camera_type:=brio

# OPSI B: Menjalankan Kamera Intel RealSense D455 (Mendatang)
ros2 launch brone_system_architecture camera_hal.launch.py camera_type:=d455
```

---

#### 2. Menghilangkan Kebutuhan `sudo bash` di Terminal 1
Jalankan skrip ini sekali saja di Intel NUC:

```bash
# Pasang aturan udev (Aman & Otomatis)
bash brone_system_architecture/scripts/setup_opencr_udev.sh --install

# Jika ingin mengembalikan ke kondisi semula kapan saja:
bash brone_system_architecture/scripts/setup_opencr_udev.sh --uninstall
```

---

### 🛡️ Jaminan Keamanan & Reversibilitas (Non-Destructive)
1. **Zero Overwrite:** Paket ini tidak pernah menimpa file asli di `~/brone_main_ws/` robot BRONE.
2. **100% Reversible:** Jika suatu saat ingin dibersihkan, cukup hapus folder `brone_system_architecture`.
3. **Decoupled:** Mas Evan dan tim lain tetap bebas mengembangkan algoritmanya secara independen.
