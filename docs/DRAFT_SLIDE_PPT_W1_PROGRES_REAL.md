# 📊 DRAF SLIDE PRESENTASI W1 (VERSI RINGKAS & PUNCHY)
**Presenter:** Systems, OS, Middleware, & Integration Engineer  

---

## 🏷️ SLIDE 1: KILAS BALIK & BATASAN KERJA (REFOCUSING)

### 🖥️ Tampilan Layar (On-Slide):
* **Prinsip Utama:** *Zero-Risk Integration* (Aman, tidak merusak sistem berjalan)
* **Fokus Peran:** Murni pada OS, Middleware ROS 2, & Kontrak Data
* **Batasan Jelas:** Algoritma internal (Gaze & Roda) 100% milik sub-tim
* **SOP Robot:** Sistem legacy (`brone_main_ws`) tetap utuh tanpa perubahan

> 🎙️ **Speaker Notes:**  
> *"Sesuai hasil evaluasi, peran saya terfokus murni pada arsitektur OS, middleware, dan jalur komunikasi data. Logika algoritma Mas Evan dan SDSC tidak dicampuri, dan sistem operasional robot yang ada tetap aman 100% tanpa diubah."*

---

## 🏷️ SLIDE 2: KILAS BALIK AUDIT GROUND TRUTH (HARDWARE & REPO)

### 🖥️ Tampilan Layar (On-Slide):
* **Kamera Leher:** Terverifikasi **Intel RealSense D455** (Hardware Stereo Depth)
* **Modul Gaze (Mas Evan):** Gaze baru dikembangkan di dev lokal (belum masuk NUC)
* **Modul Roda (SDSC):** Model *Proxemics* asli (Stop $<0.45\text{m}$, Slow $<1.2\text{m}$; bukan rem 1m)
* **Landasan Integrasi:** Berpijak pada kode & hardware nyata, bukan asumsi

> 🎙️ **Speaker Notes:**  
> *"Kami memverifikasi langsung fakta di lapangan: sensor fisik adalah RealSense D455, Gaze baru Mas Evan masih di dev lokal, dan sistem SDSC memakai zona proxemics asli. Seluruh integrasi kita berpijak pada data nyata, bukan dugaan sepihak."*

---

## 🏷️ SLIDE 3: PROGRES 1 — REPO PUSAT & OVERLAY WORKSPACE AMAN

### 🖥️ Tampilan Layar (On-Slide):
* **Repositori Resmi:** [`brone_system_architecture`](https://github.com/FatharZidan/brone_system_architecture) di GitHub
* **Metode Deployment:** Isolated ROS 2 Overlay di `~/brone_arch_ws/`
* **Zero-Risk:** Tanpa menyentuh `brone_main_ws` dan tanpa ubah `.bashrc`
* **Jaminan:** Terminal SSH ditutup $\rightarrow$ robot otomatis kembali standar pabrik

> 🎙️ **Speaker Notes:**  
> *"Kami membangun repositori resmi di GitHub dan menerapkannya di NUC menggunakan metode Isolated ROS 2 Overlay. Metode ini zero-risk: begitu terminal ditutup, sistem robot otomatis kembali bersih ke kondisi semula tanpa merusak operasional harian."*

---

## 🏷️ SLIDE 4: PROGRES 2 — CAMERA HARDWARE ABSTRACTION (HAL)

### 🖥️ Tampilan Layar (On-Slide):
* **Masalah:** Port USB kamera crash (*Device Busy*) jika dibuka bersamaan oleh Gaze & SDSC
* **Solusi (`camera_hal.launch.py`):** Kamera dibuka 1 kali di ROS 2, disiarkan ke:
  * `/camera/color/image_raw` $\rightarrow$ untuk Visi/Gaze Mas Evan
  * `/camera/depth/image_rect_raw` $\rightarrow$ untuk Obstacle Avoidance SDSC
* **Hasil:** Gaze dan SDSC berbagi data kamera bersamaan tanpa tabrakan USB

> 🎙️ **Speaker Notes:**  
> *"Untuk mencegah crash colokan USB saat kamera diakses bersamaan oleh Gaze dan SDSC, kami buat Camera HAL. Kamera dinyalakan satu kali oleh ROS 2, lalu videonya disiarkan sehingga Mas Evan dan tim SDSC bisa memakai gambar yang sama tanpa konflik hardware."*

---

## 🏷️ SLIDE 5: PROGRES 3 — PARAMETER BEBAS HARDCODE (YAML)

### 🖥️ Tampilan Layar (On-Slide):
* **Konfigurasi Eksternal:** `gaze_params_d455.yaml` & `gaze_params_brio.yaml`
* **Tuning Praktis:** Resolusi ($640\times480$), target FPS ($30$), FOV ($86^\circ$), & limit sudut leher
* **Bebas Bongkar Kode:** Kalibrasi sensor di lapangan tanpa edit script Python pengembang
* **Hasil:** Pemeliharaan rapi dan aman dari risiko bug sintaks

> 🎙️ **Speaker Notes:**  
> *"Parameter sensor dan batas sudut mekanik leher kami pisahkan ke file konfigurasi YAML. Jadi saat kalibrasi di lapangan, kita cukup ubah angka di file config tanpa perlu membongkar atau mengedit kodingan Python pengembang."*

---

## 🏷️ SLIDE 6: PROGRES 4 — INTERFACE CONTROL DOCUMENT (ICD v1.0)

### 🖥️ Tampilan Layar (On-Slide):
* **Kontrak Data Resmi:** Dokumen `BRONE_INTERFACE_CONTROL_DOCUMENT_ICD.md`
* **Standardisasi Topik:**
  * Topik Kamera: `/camera/...`
  * Topik Motor Leher: `/robotis/head_control/set_joint_states`
  * Topik Gerak Roda: `/cmd_vel`
* **Manfaat:** Antarmuka transparan; hilangkan miskomunikasi & dependensi liar antar-subtim

> 🎙️ **Speaker Notes:**  
> *"Kami menyusun dokumen ICD sebagai kontrak data resmi antar-subtim. Format data, frekuensi, dan batasan nilai numerik disepakati bersama, sehingga Mas Evan, SDSC, dan saya punya acuan yang jelas tanpa saling menduga."*

---

## 🏷️ SLIDE 7: RENCANA MINGGU INI (W1) — DUKUNGAN INFRASTRUKTUR LLM

### 🖥️ Tampilan Layar (On-Slide):
* **Status Visi:** Infrastruktur HAL siap; standby menunggu Mas Evan deploy modulnya
* **Fokus Minggu Ini (W1 Transition):**
  * **Alokasi Resource NUC:** Manajemen beban CPU & RAM (Ollama + Whisper + TTS)
  * **Audio Abstraction:** Standarisasi colokan mic & speaker USB agar kebal crash
  * **Bridge Telemetri:** Jalur komunikasi status percakapan LLM ke controller robot
* **Target:** Fondasi komputasi tetap ringan & stabil saat pipeline suara aktif

> 🎙️ **Speaker Notes:**  
> *"Dari sisi visi, seluruh infrastruktur sudah siap dan standby. Di W1 ini fokus kami bergeser ke persiapan infrastruktur LLM di NUC: membagi kapasitas CPU/RAM dan menata jalur audio USB agar percakapan suara berjalan mulus tanpa membebani sistem operasi robot."*
