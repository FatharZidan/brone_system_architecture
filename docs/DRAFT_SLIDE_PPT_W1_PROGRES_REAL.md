# 📊 DRAF SLIDE PRESENTASI PROGRES SISTEM ROBOT BRONE (W1)
**Presenter:** Systems, OS, Middleware, & Integration Engineer  
**Fokus:** Kilas Balik Evaluasi, Progres Nyata Arsitektur & Git, serta Kesiapan Infrastruktur LLM  

---

## 🏷️ SLIDE 1: KILAS BALIK & PENYELARASAN BATASAN KERJA (REFOCUSING)

### 🖥️ Tampilan Layar (On-Slide):
* **Prinsip Utama:** *Zero-Risk Integration & Modularity Isolation*
* **Penyelarasan Peran Sesuai Evaluasi:**
  * Fokus murni pada **Infrastruktur OS, Middleware ROS 2, Hardware Abstraction, & Kontrak Data (ICD)**.
  * **Tidak mencampuri logika internal modul:** Algoritma Gaze (Mas Evan) dan kendali roda (Tim SDSC) sepenuhnya berada di ranah pemilik modul.
  * SOP dan file operasional robot legacy (`brone_main_ws`) tetap **100% utuh tanpa diubah**.
* **Tujuan Akhir:** Menyediakan fondasi sistem yang stabil, aman dari crash USB/resource, dan siap menerima integrasi tanpa merusak kode yang sudah jalan.

> 🎙️ **Speaker Notes (Apa yang Diucapkan):**  
> *"Selamat pagi/siang rekan-rekan dan ketua. Mengawali laporan progres kali ini, saya ingin menegaskan kembali komitmen penyelarasan peran saya sebagai Systems & Integration Engineer. Berdasarkan evaluasi sebelumnya, saya membatasi ruang lingkup secara disiplin: tidak mencampuri atau mengubah algoritma internal rekan-rekan sub-tim, baik Gaze Tracking Mas Evan maupun kendali roda SDSC. Seluruh konfigurasi sistem legacy yang sudah berjalan di robot dijaga 100% utuh tanpa mengubah SOP harian. Fokus saya murni memastikan infrastruktur hardware, sistem operasi, middleware, dan jalur komunikasi data antar-modul berjalan stabil dan bebas konflik."*

---

## 🏷️ SLIDE 2: KILAS BALIK AUDIT GROUND TRUTH (HARDWARE & REPO TIM)

### 🖥️ Tampilan Layar (On-Slide):
* **Verifikasi Hardware Robot:**
  * Kamera terpasang di leher BRONE: **Intel RealSense D455** (RGB-D Hardware Stereo Depth).
* **Inspeksi Repositori Rekan Tim:**
  * **Modul Gaze (Mas Evan):** Gaze baru (YOLOv11 + MediaPipe + Fuzzy) sedang dalam tahap pengembangan lokal Mas Evan untuk skripsi; robot BRONE saat ini masih menjalankan versi legacy.
  * **Modul SDSC (`SDSC-Omniwheel`):** Terkonfirmasi menggunakan *Social Force Model* & *Proxemic Zones* (Emergency Stop di jarak $<0.45\text{ m}$, pelambatan 30% di $<1.20\text{ m}$; tidak ada auto-stop 1m palsu).
* **Kesimpulan:** Seluruh keputusan arsitektur disandarkan pada kode dan hardware nyata, bukan asumsi sepihak.

> 🎙️ **Speaker Notes:**  
> *"Sebagai kilas balik kedua, kami melakukan verifikasi fakta lapangan secara langsung. Pertama, kamera fisik robot terkonfirmasi adalah Intel RealSense D455 yang memiliki ASIC depth hardware mandiri. Kedua, dari penelusuran repositori, sistem Gaze baru Mas Evan saat ini masih berjalan di environment development miliknya untuk skripsi, sehingga NUC masih aman menjalankan sistem legacy. Ketiga, kami menginspeksi repositori SDSC-Omniwheel secara langsung untuk menyelaraskan parameter: sistem mereka menggunakan model Proxemic Zones dengan rem darurat di 0.45 meter dan perlambatan di 1.2 meter. Dengan memastikan fakta ini, kita tidak membuat asumsi-asumsi sepihak yang membingungkan integrasi."*

---

## 🏷️ SLIDE 3: PROGRES NYATA 1 — REPOSITORI RESMI & OVERLAY WORKSPACE AMAN

### 🖥️ Tampilan Layar (On-Slide):
* **Pembangunan Repositori Terpusat:**
  * GitHub: `https://github.com/FatharZidan/brone_system_architecture`
  * Berisi launch files, parameter YAML, dokumen ICD, dan utilitas hardware.
* **Metode Deployment: Isolated ROS 2 Overlay Workspace**
  * Di-clone di NUC robot pada direktori mandiri: `~/brone_arch_ws/src/`.
  * **100% Zero-Risk:** Tidak menyentuh workspace utama `~/brone_main_ws` dan tidak memodifikasi `~/.bashrc`.
  * Begitu terminal SSH ditutup, robot otomatis kembali bersih ke konfigurasi bawaan tanpa jejak perubahan permanen.

> 🎙️ **Speaker Notes:**  
> *"Masuk ke progres nyata yang sudah kami selesaikan: Kami telah membangun repositori arsitektur terpusat di GitHub bernama `brone_system_architecture`. Di robot NUC, kami mendemonstrasikan metode deployment berstandar industri menggunakan Isolated ROS 2 Overlay Workspace di `~/brone_arch_ws`. Keunggulan metode ini adalah zero-risk: kami sama sekali tidak menyentuh workspace lama `~/brone_main_ws` ataupun mengubah file konfigurasi sistem seperti `.bashrc`. Ketika sesi pengujian selesai dan terminal ditutup, robot tetap berada dalam kondisi semula. Ini menjamin pengujian arsitektur baru tidak akan pernah mengganggu jalannya demonstrasi harian robot."*

---

## 🏷️ SLIDE 4: PROGRES NYATA 2 — HARDWARE ABSTRACTION LAYER (CAMERA HAL)

### 🖥️ Tampilan Layar (On-Slide):
* **Tantangan Fisik:**
  * Port USB kamera RealSense di Linux hanya dapat dibuka oleh 1 proses (*Device Busy* jika diakses bersamaan oleh Gaze & SDSC).
* **Solusi: `camera_hal.launch.py`**
  * Driver kamera dijalankan **satu kali** sebagai node resmi ROS 2.
  * Mendukung argumen fleksibel:
    ```bash
    ros2 launch brone_system_architecture camera_hal.launch.py camera_type:=d455
    ```
  * Mem-publish topik standar:
    * `/camera/color/image_raw` $\rightarrow$ untuk pengolahan visi/Gaze Mas Evan.
    * `/camera/depth/image_rect_raw` $\rightarrow$ untuk obstacle avoidance Tim SDSC.
* **Dampak:** Mas Evan dan Tim SDSC dapat membaca frame kamera secara bersamaan tanpa tabrakan port USB.

> 🎙️ **Speaker Notes:**  
> *"Progres nyata kedua adalah modul Camera Hardware Abstraction Layer (HAL). Sebelumnya, jika dua program berbeda mencoba mengakses RealSense secara langsung lewat OpenCV atau pyrealsense2, Linux akan melempar error 'Device or Resource Busy'. Melalui `camera_hal.launch.py`, kami mengabstraksi kamera ke dalam node ROS 2 tunggal. Kamera cukup dibuka satu kali, lalu datanya dipancarkan ke topik standar ROS 2. Mas Evan bisa mengambil data warna RGB untuk deteksi wajah, dan rekan-rekan SDSC bisa mengambil data depth untuk penghindaran halangan secara simultan tanpa konflik perangkat keras."*

---

## 🏷️ SLIDE 5: PROGRES NYATA 3 — EKSTERNALISASI KONFIGURASI PARAMETER (YAML)

### 🖥️ Tampilan Layar (On-Slide):
* **Eliminasi Hardcoded Values:**
  * Parameter operasional dipisahkan dari script kode sumber ke file YAML eksternal:
    * `config/gaze_params_d455.yaml` (RealSense D455)
    * `config/gaze_params_brio.yaml` (Logitech Brio)
* **Manfaat Operasional:**
  * Pengaturan resolusi ($640 \times 480$), target frame rate ($30\text{ fps}$), field of view ($86^\circ$), serta batas mekanik pergerakan leher dapat diatur langsung via file konfigurasi.
  * Memudahkan tuning saat robot berganti pencahayaan atau sensor tanpa perlu menyentuh atau me-recompile kode program pengembang.

> 🎙️ **Speaker Notes:**  
> *"Progres nyata ketiga adalah perapian konfigurasi parameter. Selama ini banyak parameter sensor dan pergerakan leher tertanam mati di dalam kode program (hardcoded). Kami menyediakan konfigurasi eksternal berbasis file YAML untuk RealSense D455 dan Logitech Brio. Melalui parameter file ini, batas sudut mekanik leher, target FPS, dan FOV kamera dapat disesuaikan dengan cepat di lapangan tanpa harus mengedit script Python pengembang. Ini membuat pemeliharaan sistem jauh lebih rapi dan aman dari bug sintaks saat uji coba di lapangan."*

---

## 🏷️ SLIDE 6: PROGRES NYATA 4 — INTERFACE CONTROL DOCUMENT (ICD v1.0)

### 🖥️ Tampilan Layar (On-Slide):
* **Standardisasi Antarmuka Sistem:**
  * Dokumen resmi: `docs/BRONE_INTERFACE_CONTROL_DOCUMENT_ICD.md`.
  * Menetapkan kontrak antarmuka komunikasi antar-komputer (Jetson $\leftrightarrow$ NUC $\leftrightarrow$ Base):
    * **Topik Visi:** `/camera/color/image_raw` & `/camera/depth/image_rect_raw`
    * **Topik Target Orang:** `/brone/target_person` (`geometry_msgs/PointStamped`)
    * **Topik Motor Leher:** `/robotis/head_control/set_joint_states` (`sensor_msgs/JointState`)
    * **Topik Roda Base:** `/cmd_vel` (`geometry_msgs/Twist`)
* **Dampak Positif:** Menghilangkan kebingungan antar-subtim; setiap pengembang tahu persis input/output modulnya tanpa saling menduga-duga.

> 🎙️ **Speaker Notes:**  
> *"Progres nyata keempat adalah penyusunan dokumen Interface Control Document atau ICD v1.0. Dokumen ini menjadi kontrak kerja sama resmi antar-subtim di Robot BRONE. ICD memetakan nama topik, tipe data, frekuensi transmisi, dan batasan nilai numerik yang disepakati—mulai dari output visi leher hingga perintah gerak roda. Dengan adanya ICD ini, Mas Evan, Tim SDSC, dan saya memiliki referensi antarmuka yang transparan, sehingga proses integrasi tidak lagi bergantung pada asumsi verbal."*

---

## 🏷️ SLIDE 7: RENCANA MINGGU INI (W1) — DUKUNGAN INFRASTRUKTUR LLM & NEXT STEPS

### 🖥️ Tampilan Layar (On-Slide):
* **Status Modul Visi:**
  * Infrastruktur HAL dan overlay workspace telah siap; tinggal menunggu kesiapan Mas Evan untuk mendemokan / men-deploy modul vision barunya ke robot.
* **Agenda Utama Minggu Ini (W1 Transition):**
  * **Rancang Bangun Infrastruktur Sub-Tim LLM / Voice Pipeline:**
    * Pemetaan resource alokasi CPU & VRAM di Intel NUC untuk Local LLM / Whisper / TTS.
    * Standarisasi *Audio Hardware Abstraction* (USB mic array & speaker output) agar tidak bentrok dengan pipeline audio BOS v4.0.
    * Perancangan arsitektur event-driven bridge antara respon LLM dan ekspresi/gerakan robot.
* **Target:** Fondasi sistem komputasi tetap stabil saat beban pipeline komputasi bahasa mulai masuk ke robot.

> 🎙️ **Speaker Notes:**  
> *"Untuk rencana kerja minggu ini di fase W1: Dari sisi visi, seluruh infrastruktur pembungkus dan kontrak antarmuka sudah siap di robot, sehingga kami berada pada posisi siap mendampingi begitu Mas Evan hendak menguji coba modul Gaze barunya di BRONE. Selanjutnya, agenda prioritas saya minggu ini adalah mulai membantu merancang infrastruktur pendukung untuk tim LLM dan interaksi suara. Mengingat model bahasa dan speech-to-text menuntut komputasi memori yang cukup intensif di NUC, saya akan memetakan pembagian resource CPU/VRAM serta mengabstraksi hardware audio (mic dan speaker) agar pipeline percakapan dapat terintegrasi mulus tanpa menimbulkan latency atau crash di sistem operasi. Terima kasih, saya siap menerima masukan dari ketua dan rekan-rekan."*
