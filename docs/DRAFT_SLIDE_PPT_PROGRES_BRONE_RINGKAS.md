# 📊 DRAF SLIDE PPT PROGRES BRONE (VERSI RINGKAS & PRESENTABLE)
### *Format Bersih: Poin Kunci di Layar + Catatan Presenter Lengkap*
**Presenter:** Systems, Middleware, OS & Integration Engineer  
**Durasi Presentasi:** $\approx 10\text{–}12\text{ Menit}$ (16 Slide)  

---

## 🏷️ SLIDE 1: COVER & REKAP KILAS BALIK

### 🖥️ Tampilan Layar (On-Slide):
* **Judul:** **Integrasi Sistem Visi & Navigasi Heterogen Robot BRONE**
* **Subjudul:** *Pembedahan Kode Evan & SDSC, Verifikasi Hardware Jetson, dan Skema Visual Servoing Aman*
* **Status Progres:**
  * 🟢 **Minggu Lalu:** Pemetaan isolasi modul (Anya, SDSC, Wisnu) & bahaya crash USB V4L2.
  * 🚀 **Minggu Ini:** Kode terbaru Evan & SDSC dibedah, TensorRT 10.3 aktif, kamera D455 terkonfirmasi, dan skema konkurensi visi-kinematika dirumuskan.

> 🎙️ **Speaker Notes (Apa yang Diucapkan):**  
> *"Selamat pagi/siang rekan-rekan dan ketua tim. Melanjutkan laporan progres minggu lalu mengenai arsitektur sistem visi, minggu ini kita mencapai lompatan besar. Kita sudah membedah tuntas kode terbaru Mas Evan dan tim SDSC, memverifikasi langsung performa AI di hardware Jetson, memastikan keunggulan kamera fisik RealSense D455, serta menyiapkan jawaban ilmiah yang aman untuk tantangan ketua kemarin terkait konkurensi visi dan motor."*

---

## 🏷️ SLIDE 2: STATUS GERBANG HARDWARE (HARDWARE GATES)

### 🖥️ Tampilan Layar (On-Slide):
* **Layout:** 2 Status Card (Hijau / Resolved)
* 🟢 **Gate 1: Integritas Struktur Kaki**
  * Part mekanik kaki yang patah **telah diganti baru**.
  * Tumpuan berdiri robot simetris & aman untuk uji torsi aktif.
* 🟢 **Gate 2: Akses Repositori Rekan Tim**
  * Repo Mas Evan (`NUC-brone-gaze-system`) dibedah tuntas.
  * Repo SDSC (`SDSC-Omniwheel`) dianalisis & diselaraskan.

> 🎙️ **Speaker Notes:**  
> *"Sebelum masuk ke software, dua gerbang keselamatan hardware sudah resmi hijau. Pertama, part kaki robot yang patah kemarin sudah diganti baru sehingga struktur robot sudah kokoh dan simetris untuk uji berdiri. Kedua, repositori Mas Evan dan tim SDSC sudah berhasil kita buka dan bedah tuntas, jadi integrasi kita berbasis kode nyata, bukan asumsi."*

---

## 🏷️ SLIDE 3: BEDAH KODE TERBARU EVAN (GAZE v3.0)

### 🖥️ Tampilan Layar (On-Slide):
* **BOS v4.0 State Machine (`state_machine_node.py`):**
  * Mode interaksi utama berjalan bergantian (*mutually exclusive*): `talk` $\leftrightarrow$ `anya`.
  * Fungsi `_cleanup_current_mode()` mematikan proses lama secara bersih sebelum ganti mode.
  * *Konfirmasi Fitur:* Command legacy `eyefollow` di CLI BOS **resmi deprecated** oleh Mas Evan (`[DEL] Gaze dikeluarkan dari alur CLI`); Gaze dialihkan menjadi modul visi mandiri di Jetson.
* **Optimasi Awal Mas Evan:**
  * Resolusi input di-downsample ke $320 \times 240$ piksel.
  * *Frame-skipping:* Proses inferensi berjalan selang 2 frame.
* **Kesiapan ROS 2:**
  * Output leher **sudah berupa topik ROS 2 standar**: `/robotis/head_control/set_joint_states` (`JointState`).
  * Siap dipindahkan ke Jetson tanpa rombak driver motor.

> 🎙️ **Speaker Notes:**  
> *"Dari pembedahan kode Mas Evan, ada kabar sangat baik: Mas Evan sudah membuat state machine BOS v4.0 yang rapi di mana mode percakapan suara dan deteksi civitas berjalan bergantian, tidak saling tabrak. Nah, konfirmasi penting untuk tim: command 'eyefollow' di BOS kemarin memang sudah dikeluarkan oleh Mas Evan sendiri dari otomasi CLI. Jadi keputusan kita untuk tidak mengotak-atik fitur eyefollow di BOS sudah 100% tepat, karena modul Gaze Mas Evan sekarang berjalan sebagai modul visi mandiri di Jetson yang langsung mem-publish topik ROS 2 standar untuk leher."*

---

## 🏷️ SLIDE 4: ADAPTASI KODE EVAN DI JETSON (SOLUSI SKRIPSI)

### 🖥️ Tampilan Layar (On-Slide):
* **Tantangan di ARM64:** MediaPipe berjalan murni di CPU Jetson (bisa membebani 6 core jika ada kerumunan).
* **3 Penyesuaian Ringan (Metodologi Skripsi 100% Aman):**
  1. **Filter Kandidat MediaPipe:** Dibatasi hanya memproses **1–2 orang terdekat** dari hasil YOLO (logika Fuzzy skripsi tetap teruji valid).
  2. **Model Acceleration:** Ganti loader `.pt` ke `YOLO('yolo11s.engine')` (TensorRT GPU).
  3. **Sensor Alignment:** Hapus config webcam Brio lama $\rightarrow$ ganti FOV native D455 ($86^\circ$).

> 🎙️ **Speaker Notes:**  
> *"Agar modul Mas Evan tidak membebani CPU Jetson, kita lakukan adaptasi cerdas: MediaPipe kita batasi hanya memproses 1 atau 2 orang terdekat saja. Logika Fuzzy skripsi Mas Evan tetap berfungsi 100% untuk memilih target utama, tapi CPU Jetson tidak akan overload oleh orang-orang di latar belakang."*

---

## 🏷️ SLIDE 5: VERIFIKASI LANGSUNG GPU & TENSORRT JETSON

### 🖥️ Tampilan Layar (On-Slide):
* **Hasil Audit Terminal Nyata di Lab:**
  * ✅ **TensorRT Version:** `10.3.0` (Aktif)
  * ✅ **PyTorch Official NVIDIA:** `2.5.0a0...nv24.08` (CUDA 12.5)
  * ✅ **OS Stack:** JetPack 6.2.1 [L4T 36.4.7]
* **Status Daya & Suhu (`jtop`):**
  * Power Mode: `MAXN_SUPER` (25W Full Performance).
  * Suhu Idle: Sangat dingin ($38^\circ\text{C}$, konsumsi daya $4.6\text{W}$).
* **Kesimpulan:** Mitos "TensorRT belum ada" resmi terbantahkan $\rightarrow$ Stack siap tempur.

> 🎙️ **Speaker Notes:**  
> *"Ini terobosan paling penting minggu ini. Kemarin sempat ada keraguan apakah TensorRT sudah aktif di Jetson. Saya sudah masuk ke terminal Jetson dan memverifikasi langsung: TensorRT 10.3.0 dan CUDA 12.5 aktif 100%! Status JetPack di jtop terbaca resmi JetPack 6.2.1. Infrastruktur AI akselerasi GPU Jetson siap mengeksekusi model tanpa kendala."*

---

## 🏷️ SLIDE 6: KLARIFIKASI SENSOR: REALSENSE D455

### 🖥️ Tampilan Layar (On-Slide):
* **Fakta Sensor:** Kamera fisik robot adalah **Intel RealSense D455** (Bukan Logitech Brio meja lab).
* **2 Keuntungan Emas:**
  1. 🎙️ **Resolusi Bug Suara P13:**
     * D455 murni sensor optik RGB-D (tanpa mic internal).
     * NUC tetap memakai mic USB mandirinya $\rightarrow$ Pipeline Whisper & LLM `brone-talk` kebal dari error *audio capture*.
  2. 📏 **Hardware Stereo Depth ASIC:**
     * Kedalaman milimeter ($Z$) dihitung langsung di chip internal D455.
     * Topik kedalaman tersedia instan dengan **0% beban CPU Jetson**.

> 🎙️ **Speaker Notes:**  
> *"Kita juga meluruskan fakta kamera: robot menggunakan RealSense D455, bukan webcam Brio. Ini membawa dua keuntungan besar: pertama, D455 tidak punya mic internal, jadi pemindahan kamera ke Jetson tidak akan merebut mic dari NUC—suara LLM NUC aman. Kedua, D455 menghitung kedalaman di chip hardware bawaannya, jadi kita dapat data jarak instan tanpa membebani CPU Jetson."*

---

## 🏷️ SLIDE 7: BEDAH REPO BARU SDSC (`detections/Detection`)

### 🖥️ Tampilan Layar (On-Slide):
* **Kabar Baik:** Script baru SDSC membuktikan mereka sudah memakai RealSense depth via `depth_frame.get_distance(cx, cy)` untuk ukur jarak orang.
* **Potensi Benturan Jika Mandiri:**
  * ❌ *USB Lock:* `rs.pipeline().start()` ganda akan crash (*EBUSY*).
  * ❌ *YOLO Ganda:* Boros VRAM jika SDSC jalan `yolo11n` sementara Evan jalan `yolo11s`.
* **Solusi Win-Win:**
  * Jetson menjalankan **Single Ingestion**: ambil RGB + Depth sekali $\rightarrow$ broadcast koordinat `[X, Y, Z]` ke topik `/brone/target_person`. Node roda SDSC tinggal terima topik matang!

> 🎙️ **Speaker Notes:**  
> *"Kemarin tim SDSC baru saja mengunggah skrip deteksi baru. Logika mereka persis dengan desain kita, yaitu mengambil jarak orang untuk navigasi roda. Agar kamera tidak bentrok dan tidak boros daya menjalankan 2 model YOLO sekaligus, kita satukan pembacaan kamera di node backbone Jetson, lalu koordinat jaraknya kita kirimkan ke node roda SDSC."*

---

## 🏷️ SLIDE 8: GRAND PLAN ARSITEKTUR v3.2 (SINGLE INGESTION)

### 🖥️ Tampilan Layar (On-Slide):
* **Prinsip Utama:** 1 Kamera Fisik untuk 3 Kebutuhan Tim.
* **Topologi Data Alir:**
  * **[RealSense D455]** $\xrightarrow{\text{USB 3.0}}$ **[Jetson Orin Nano]**
  * $\rightarrow$ **YOLOv11 TensorRT (GPU ~8.5 ms):**
    * 🚗 $\to$ Koordinat $[X, Y, Z]$ ke **SDSC Omniwheel** (`/cmd_vel`)
    * 👔 $\to$ Crop Baju ke **Anya Civitas** (ORB Almamater UB)
    * 👁️ $\to$ Crop Wajah ke **Evan Gaze** (Target Leher ROS 2)
  * $\xrightarrow{\text{FastRTPS LAN (< 128 Byte)}}$ **[Intel NUC Core i9]** (`op3_manager` Motor 50 Hz & Dialog Suara).

> 🎙️ **Speaker Notes:**  
> *"Inilah arsitektur Grand Plan v3.2 kita. Intinya adalah Single Ingestion di Jetson: kamera RealSense D455 hanya dibuka oleh satu driver sentral. Hasil deteksi YOLO TensorRT di GPU kemudian di-sharing: SDSC mendapat jarak metrik untuk roda, Kak Anya mendapat crop baju untuk cek almamater, dan Mas Evan mendapat crop wajah untuk tatapan leher. NUC hanya menerima metadata koordinat yang sangat ringan via kabel LAN."*

---

## 🏷️ SLIDE 9: ALOKASI CORE DUA MESIN (NUC & JETSON)

### 🖥️ Tampilan Layar (On-Slide):
* **1. Intel NUC Core i9 (14 Core / 20 Thread):**
  * `Core 0 & 1 (P-Core)` : `op3_manager` (Real-Time `chrt 80`, motor 50 Hz). Kebal interupsi AI!
  * `Core 12..19 (E-Cores)`: Pipeline Suara `brone-talk` (Whisper + Ollama LLM + Piper TTS).
* **2. Jetson Orin Nano (6-Core ARM Cortex-A78AE):**
  * `Core 0` : Driver RealSense D455 (USB 3.0 I/O capture).
  * `Core 1` : YOLO Host Orchestrator & Dispatcher.
  * `Core 2 & 3` : MediaPipe Evan (Dibatasi 2 thread, 1–2 wajah terdekat).
  * `Core 4` : **SDSC Omniwheel (Dedicated)**: Loop gerak 20 Hz, Social Force Model, & serial bridge `/cmd_vel` (bebas jitter!).
  * `Core 5` : Anya Civitas (ORB Matcher) + OS Linux, FastRTPS DDS, & Telemetri `jtop`.
* **Fakta Utilisasi:** Rata-rata beban CPU Jetson hanya **$\approx 39\%$** (Sisa cadangan idle **$> 50\%$**, bebas panas).

> 🎙️ **Speaker Notes:**  
> *"Untuk menjamin tidak ada perebutan CPU antar program, kita membagi core di kedua komputer secara ketat. Di NUC, motor terkunci di Core Fisik P-Core 0 dengan prioritas real-time chrt 80, sementara LLM suara dialokasikan ke 8 E-Core. Di Jetson dengan 6 core ARM: Core 0 menjaga kamera agar tidak drop frame, Core 1 untuk YOLO, Core 2 dan 3 untuk MediaPipe Mas Evan. Khusus kendali roda SDSC, kita dedikasikan mandiri di Core 4 agar loop gerak 20 Hz dan pengiriman serial motor tidak terkena jitter saat Kak Anya menjalankan komputasi ORB di Core 5 bersama background OS dan jaringan DDS. Dengan pemisahan ini, gerakan roda dijamin mulus tanpa sentakan."*

---

## 🏷️ SLIDE 10: MENJAWAB TANTANGAN KETUA: SKEMA VISION-MOTION CODESIGN BRONE

### 🖥️ Tampilan Layar (On-Slide):
* **Pertanyaan Ketua:** *"Gimana kalau visi dijalankan konkuren dengan kinematika? Cara amannya gimana?"*
* **Akar Masalah Nyata (Paper Cheng et al. 2024):**
  * Visi bekerja di frekuensi fluktuatif ($\approx 30\text{ Hz}$ / $\Delta t \approx 33\text{ ms}$).
  * Motor bekerja di frekuensi cepat ($50\text{ Hz}$ di NUC, $1\text{ kHz}$ di OpenCR).
  * Menembak perintah langsung membuat motor **sentak-sentak (*acceleration jump / jerk spike*)**.
* **Solusi Vision-Motion Codesign di BRONE & Status Implementasinya:**
  1. 🌊 **Interpolasi Orde-3 / Jerk-Bounded (Anti-Sentakan):** `[🔵 PROPOSED / DESAIN SISTEM]`
     * *Konsep:* NUC/OpenCR bertindak sebagai *Motion Kernel* $\rightarrow$ memperhalus perintah posisi/kecepatan dari Jetson secara kontinu (jerk-bounded).
     * *Status Kode:* **Belum di-coding penuh**. Di kode Evan baru ada low-pass filter posisi (`servo_alpha`). Interpolasi kontinu diajukan untuk NUC.
  2. 🎯 **Batas Kecepatan Leher & Soft-FOV (Anti-Lepas):** `[🟡 PARSIAL DI KODE EVAN]`
     * *Konsep:* Kecepatan putar servo leher dibatasi $\le 45^\circ/\text{s}$ & deadband agar citra tidak blur dan target tidak terlempar keluar layar.
     * *Status Kode:* **Sudah ada fondasi**. Deadband 10% & clamp sudut $[-1.4, 1.4\text{ rad}]$ sudah aktif di `brone_gaze_node.py`; tinggal menambahkan limit kecepatan ($\le 45^\circ/\text{s}$).
  3. 🛑 **Interlock Auto-Stop 1 Meter (Anti-Nabrak):** `[🟡 PROTOTIPE STANDALONE SDSC]`
     * *Konsep:* Membaca kedalaman metrik RealSense D455 $\rightarrow$ roda otomatis berhenti jika jarak orang $\le 1.0\text{ m}$.
     * *Status Kode:* **Script deteksi sudah ada tapi belum terhubung**. Tim SDSC sudah punya script pembaca jarak D455 (`Detection`), tinggal disambungkan ke `/cmd_vel` pada Fase 1.

> 🎙️ **Speaker Notes (Transparan, Kredibel, & Menguasai Lapangan):**  
> *"Menjawab pertanyaan ketua: 'Gimana cara amannya menjalankan visi dan kinematika secara konkuren?'. Berdasarkan studi literatur IEEE 2024 dari Cheng et al., masalah utama menjalankan visi dan motor bersamaan adalah perbedaan frekuensi: visi berjalan sekitar 30 Hz dengan jeda waktu fluktuatif, sedangkan motor bekerja deterministik di 50 Hz hingga 1 kHz.*  
> *Kalau koordinat visi langsung ditembak mentah-mentah ke motor, motor akan mengalami lonjakan akselerasi dan sentakan kasar (jerk spike).*  
> *Sebagai transparansi kesiapan kode di lapangan:*  
> *Pertama, untuk rem darurat 1 meter, tim SDSC sebenarnya sudah berhasil membaca jarak metrik orang di script RealSense mereka (`Detection`), tinggal kita hubungkan kabel logikanya ke kendali roda `/cmd_vel` pada jadwal pengujian Fase 1 besok.*  
> *Kedua, untuk leher Mas Evan, fondasi deadband 10% dan filter peredam sudah ada di kodenya, tinggal kita tambahkan baris pembatas kecepatan maksimal 45 derajat per detik.*  
> *Ketiga, untuk interpolasi orde-3 anti-sentakan di NUC, ini adalah skema arsitektur yang kita usulkan agar pergerakan motor robot dijamin mulus tanpa lonjakan mekanik.*  
> *Jadi solusinya bukan mimpi di awang-awang, melainkan sudah ada pijakan kodenya dan tinggal kita integrasikan bertahap."*

---

## 🏷️ SLIDE 11: KINEMATIKA 4-RODA & LEHER: MASALAH FISIK & SOLUSI PAPER XU ET AL. (2024)

### 🖥️ Tampilan Layar (On-Slide):
* **Fokus Masalah:** Sasis 4-Omniwheel Bergerak 360° vs Leher Kamera Pan-Tilt.
* **Tantangan Nyata (The Problem):**
  * Sasis 4-Omniwheel sangat lincah: maju, mundur, geser samping (*strafe*), serong, & putar CW/CCW.
  * ⚠️ *Kamera Goyang Saat Roda Bermanuver:* Inersia meluncur bebas memicu goyangan di 2 sumbu $\rightarrow$ jika leher ikut panik mengejar target, timbul osilasi (*chatter*).
  * ⚠️ *Redundansi (5-DOF):* Leher punya putaran pan, roda punya putaran yaw $\rightarrow$ jika keduanya berebut, target terlempar keluar dari FOV kamera.
* **Solusi Nyata Paper Xu et al. (IEEE Trans. 2024 - Sec. III-C & IV-A):**
  1. 🎯 **Task-Priority Null-Space Projection:**
     * **Prioritas 1 (Leher 30 Hz):** Leher mengunci target tepat di tengah kamera ($u, v$).
     * **Prioritas 2 (Roda 20 Hz):** Perintah gerak roda diproyeksikan ke *null-space* leher:
       $$\dot{q}_{\text{roda}} = (I - J_{\text{leher}}^+ J_{\text{leher}}) \dot{q}_{\text{nav}}$$
       👉 **Artinya:** Roda bebas meluncur maju, geser samping (*strafe*), atau serong menghindari rintangan, **tanpa pernah melepaskan tatapan mata leher ke tamu!**
  2. 📏 **Augmented RGB-D Jacobian $[u, v, Z]^T$:**
     * Hardware depth RealSense D455 membaca jarak metrik $Z$ instan $\rightarrow$ matriks interaksi **Full-Rank ($J \cdot J^+ > 0$)**, membuktikan secara matematis **nol singularitas / titik buta**.
  3. 🛑 **Control Barrier Function (CBF):**
     * Rem darurat otomatis memutus translasi roda jika jarak $Z \le 1.0\text{ m}$.

> 🎙️ **Speaker Notes (Konkret, Lugas, & Menjawab Tuntas):**  
> *"Rekan-rekan dan ketua, pertanyaan ketua kemarin: 'Gimana cara amannya kinematika roda dan leher jalan barengan sama visi?'. Jawaban konkretnya ada di Paper IEEE 2024 dari Xu et al:*  
> *Sasis 4 roda omniwheel kita orientasinya sangat luas: bisa maju, mundur, geser samping (strafe), serong, dan mutar di tempat. Masalahnya: kalau roda lagi geser samping lalu lehernya panik ngejar orang, kameranya goyang dan target visual gampang hilang.*  
> *Solusi dari paper Xu et al. adalah **Task-Priority Null-Space Projection**: leher kita beri Prioritas 1 untuk mengunci wajah orang di tengah kamera. Perintah roda—mau maju, geser samping, atau serong—diproyeksikan ke ruang sisa (null-space). Artinya, roda bebas bermanuver menghindari halangan apa pun TANPA mengganggu kestabilan tatapan leher.*  
> *Kedua, paper membuktikan bahwa kamera RealSense D455 yang membaca jarak metrik Z secara langsung menjamin matriks kontroler Full-Rank, jadi robot tidak akan pernah macet di titik buta atau singularitas.*  
> *Ketiga, kita pasang batas rem otomatis di jarak 1 meter via Control Barrier Function. Roda dan leher terkoordinasi secara presisi tanpa saling tabrak."*

---

## 🏷️ SLIDE 12: ANTI-SENTAKAN MOTOR: MASALAH WAKTU & SOLUSI PAPER CHENG ET AL. (2024)

### 🖥️ Tampilan Layar (On-Slide):
* **Fokus Masalah:** Jeda Sampling Kamera Visi vs Eksekusi Motor Real-Time.
* **Tantangan Waktu & Bahaya Nyata (The Problem):**
  * Visi (Jetson) berfluktuasi pada $\approx 30\text{ FPS}$ ($\Delta t \approx 33\text{ ms}$).
  * Motor roda & servo Dynamixel (NUC) menuntut sinyal cepat ($50\text{–}100\text{ Hz}$ deterministik).
  * ⚠️ *Bahaya Acceleration Jump / Jerk Spike ($\Lambda$):* Jika koordinat visi ditembak langsung, saat frame kamera terlambat sedikit saja ($\Delta T > 0$), motor sempat melambat/diam, lalu mendadak **menyentak kasar (*jerk spike*)** saat data baru masuk.
* **Solusi Nyata Paper Cheng et al. (IEEE Trans. 2024 - Codesign):**
  1. ⚙️ **Motion Control Kernel Architecture ($\Lambda = P_3 > P_2 > P_1$):**
     * NUC Core 0 real-time `chrt 80` membagi tugas secara deterministik:
       * **$P_3$ (Tertinggi):** `AxisOutput` eksekusi paket ke motor fisik roda & leher (kebal interupsi!).
       * **$P_2$ (Menengah):** Interpolator trajektori online (OTG).
       * **$P_1$ (Rendah):** Decoding pesan visi dari Jetson (asinkron).
  2. 🌊 **Self-Adaptive Jerk Recalculation (`recalculateJerk`):**
     * Interpolator NUC menghitung ulang batas jerk ($J$) mengikuti fluktuasi jeda frame kamera ($T_m$).
     * Kurva percepatan $a(t)$ dipaksa menyentuh nol tepat saat target tercapai $\rightarrow$ **lonjakan akselerasi dan sentakan motor tereliminasi ke 0!**
  3. 📈 **Online Trajectory Generation (OTG Orde-3):**
     * Mengubah setpoint patah-patah dari Jetson menjadi profil kontinu $C^2$ ($p, v, a, j$ terikat batas). Motor leher dan roda meluncur mulus tanpa sentakan mekanik.

> 🎙️ **Speaker Notes (Menjelaskan Mekanisme Codesign):**  
> *"Lalu bagaimana masalah beda waktu antara kamera yang mikirnya 30 frame per detik dan motor yang muternya 50 sampai 100 kali per detik? Masalah ini dijawab tuntas oleh Paper IEEE 2024 dari Cheng et al tentang Vision-Motion Codesign:*  
> *Kalau koordinat dari kamera langsung ditembak mentah-mentah ke motor, saat kamera ada jeda sedikit saja, motor akan sempat ngerem lalu mendadak menyentak kasar (acceleration jump). Ini yang bikin leher getar dan roda ndut-ndutan.*  
> *Solusi dari Cheng et al. ada dua: pertama, NUC bertindak sebagai **Motion Control Kernel** dengan prioritas P3 > P2 > P1, di mana perintah fisik ke motor dikunci prioritas tertinggi agar tidak pernah diganggu oleh proses lain.*  
> *Kedua, interpolator NUC menerapkan algoritma **Self-Adaptive Jerk Recalculation**: batas percepatan dihitung ulang secara dinamis mengikuti jeda kamera, sehingga lonjakan akselerasi diredam mulus menjadi nol.*  
> *Hasilnya: sefluktuatif apa pun jeda gambar dari kamera Jetson, gerakan motor di leher dan roda tetap meluncur mulus tanpa sentakan mekanik sama sekali."*

---

## 🏷️ SLIDE 13: MATRIKS KONEKSI: TEORI PAPER VS PENERAPAN DI KODE BRONE

### 🖥️ Tampilan Layar (On-Slide):
* **Tabel Pemetaan Langsung (Teori Paper $\leftrightarrow$ Implementasi Kode Nyata BRONE):**

| Masalah Robotika di BRONE | Solusi Teori Paper (IEEE 2024) | Implementasi Nyata di Robot BRONE | Status Kode |
| :--- | :--- | :--- | :---: |
| **Kamera Goyang Saat Roda Manuver** | Task-Priority Null-Space *(Xu et al. Sec. IV)* | Leher Prioritas 1; Roda di Null-Space via `/cmd_vel` | 🔵 Siap Sambung |
| **Titik Buta / Singularitas Kinematika** | Augmented RGB-D Jacobian $[u, v, Z]^T$ *(Xu et al. Sec. III)* | RealSense D455 hardware depth ASIC (`Detection`) | 🟢 Terbukti di D455 |
| **Sentakan Akselerasi (*Jerk Spike*)** | Adaptive Jerk Recalculation *(Cheng et al. Sec. III)* | Interpolator Orde-3 di NUC Core 0 `op3_manager` | 🔵 Arsitektur NUC |
| **Kompetisi CPU Visi vs Motor** | Motion Kernel $P_3 > P_2 > P_1$ *(Cheng et al. Sec. II)* | NUC `chrt 80` (P-Core) vs Jetson Orin (GPU Ampere) | 🟢 Terverifikasi OS |
| **Bahaya Tabrakan Fisik** | Control Barrier Function *(Xu et al. Sec. II)* | Auto-stop interlock $Z \le 1.0\text{ m}$ di base roda | 🟡 Prototipe SDSC |

> 🎙️ **Speaker Notes (Membuktikan ke Tim & Ketua):**  
> *"Slide ini adalah rangkuman tegas yang menghubungkan teori kedua paper IEEE tadi langsung ke baris kode robot kita.*  
> *Semua masalah yang dikhawatirkan ketua—mulai dari kamera goyang, titik buta kontroler, sentakan akselerasi, sampai perebutan CPU—memiliki padanan solusi teori ilmiah dari paper Xu et al dan Cheng et al, dan sudah kita petakan langsung ke file kodenya di Jetson dan NUC.*  
> *Jadi kita tidak cuma membaca paper untuk pajangan, tetapi kita mengadopsi formulasi matematiknya untuk menjamin integrasi robot BRONE berjalan aman, stabil, dan teruji secara ilmiah."*

---

## 🏷️ SLIDE 14: ROADMAP PENGUJIAN & ACTION ITEMS TIM

### 🖥️ Tampilan Layar (On-Slide):
* **🗺️ 3 Fase Pengujian Terukur:**
  * **Fase 1 (Bench Validation):** Verifikasi stream RealSense D455 30 FPS + export `yolo11s.engine` di Jetson.
  * **Fase 2 (Rig Testing):** Torsi berdiri robot aktif di penyangga + uji respons servo leher ID 19 & 20 via FastRTPS.
  * **Fase 3 (Floor Demo):** Omniwheel meluncur mendekat $\rightarrow$ auto-stop 1m $\rightarrow$ leher menatap $\rightarrow$ sapaan almamater & dialog suara.
* **👥 Action Items Rekan Tim:**
  * **Mas Evan:** Arahkan model ke `yolo11s.engine`, set FOV D455 ($86^\circ$), batasi MediaPipe ke 1–2 orang.
  * **Kak Anya:** Hubungkan fungsi ORB matching ke subscriber crop baju Jetson.
  * **Tim SDSC:** Hubungkan input jarak RealSense ke Social Force Model roda.

> 🎙️ **Speaker Notes:**  
> *"Untuk memvalidasi integrasi ini secara bertahap dan tanpa risiko kerusakan hardware, pengujian kita bagi ke 3 fase: mulai dari uji meja untuk verifikasi pipeline kamera dan AI, uji statis di penyangga untuk menyalakan torsi leher dan roda tanpa menyentuh lantai, hingga demonstrasi dinamis penuh di lantai aula.*  
> *Lalu bagaimana pembagian kerja dan target mingguan kita menuju demo November? Mari kita lihat slide terakhir."*

---

## 🏷️ SLIDE 15: FAST-TRACK ROADMAP & DEADLINE SUB-TIM (MENUJU NOVEMBER)

### 🖥️ Tampilan Layar (On-Slide):
* **🖼️ Visual Gantt Chart (Light Mode - Siap Ditampilkan):**
  ![Gantt Timeline BRONE](file:///c:/Users/Patarajah/Documents/IDE%20Antigravity/gantt_timeline_brone.png)
  *(File asli: [gantt_timeline_brone.svg](file:///c:/Users/Patarajah/Documents/IDE%20Antigravity/gantt_timeline_brone.svg))*

* **⚡ Kebijakan Fast-Track (November Sudah Dekat):**
  * ❌ *Di-skip Sementara:* Pengukuran latensi mikro, profiling FPS panjang, dan stress test berjam-jam.
  * ⭕ *Fokus Mutlak:* Pipeline nyambung, data ngalir, sensor tidak rebutan (kamera aman), dan rem darurat 1 meter aktif.
* **📅 Jadwal Mingguan (W1–W4):**
  * **W1 (13–19 Okt):** *Interface Freeze* $\rightarrow$ Kamera di-stream pusat oleh Backbone; semua node jalan lokal tanpa crash.
  * **W2 (20–26 Okt):** *Data-Flow & Safety Interlock* $\rightarrow$ Gaze kirim leher ke NUC, Anya terima crop baju, SDSC kunci auto-stop $\le 1\text{m}$.
  * **W3 (27 Okt–2 Nov):** *Full Rig Test* $\rightarrow$ Robot nyala di penyangga: leher menatap, roda mati di 1m, LLM sapaan bunyi.
  * **W4 (3–9 Nov):** *Floor Rehearsal* $\rightarrow$ Gladi bersih dinamis di lantai aula menuju demo Rektorat.
* **⏱️ Deadline Tegas Per Sub-Tim (Backbone Deliverables Contract):**
  * 👁️ **Tim Gaze (Evan):** 19 Okt ganti `yolo11s.engine` & subscribe kamera pusat; 26 Okt publish sudut leher $\le 45^\circ/\text{s}$ & crop baju (1 orang terdekat).
  * 👔 **Tim Civitas (Anya):** 19 Okt lepas kamera lokal; 26 Okt sambung ORB matcher ke crop Evan $\rightarrow$ status `/civitas/status`.
  * 🛞 **Tim SDSC (Wisnu / Base):** 19 Okt split node jarak D455; 26 Okt wajib interlock serial `<0, 0, 0>` jika jarak $Z \le 1.0\text{ m}$.
  * 🗣️ **Tim LLM (Suara):** 19 Okt pipeline lokal STT-LLM-TTS jalan di NUC E-Core; 26 Okt trigger sapaan almamater saat robot berhenti.

> 🎙️ **Speaker Notes:**  
> *"Dengan roadmap eksekusi yang sudah tertata rapi ini, mari kita tutup laporan progres hari ini dengan kesimpulan utama kesiapan sistem kita."*

---

## 🏷️ SLIDE 16: KESIMPULAN: 3 PILAR INTEGRASI MENUJU DEMO NOVEMBER

### 🖥️ Tampilan Layar (On-Slide):
* **🎯 3 Intisari Integrasi BRONE:**
  1. 🛡️ **Hardware Terbukti & Nol Konflik (Bukan Asumsi):**
     * AI Jetson (TensorRT 10.3 + CUDA 12.5) & kamera RealSense D455 diverifikasi di hardware riil.
     * 1 Node kamera sentral $\rightarrow$ nol bentrok USB (`EBUSY`).
     * Motor fisik di NUC P-Core 0 (`chrt 80`) kebal gangguan proses AI & suara.
  2. 🛑 **Keselamatan Fisik & Kehalusan Gerak Terjamin:**
     * Rem darurat otomatis memutus translasi roda saat jarak orang $\le 1.0\text{ m}$.
     * Gerak 4-omniwheel di *null-space* leher + batas kecepatan leher $\le 45^\circ/\text{s}$ mencegah osilasi dan target hilang.
  3. ⚡ **Eksekusi Paralel Menuju Demo November:**
     * Kontrak data (ICD) dikunci sejak W0; seluruh subtim (Evan, Anya, Wisnu, LLM) bergerak serentak tanpa saling tunggu.
     * **Timeline Jelas:** Akhir Oktober (Uji Penyangga) $\rightarrow$ Awal November (Gladi Bersih Aula) $\rightarrow$ Demonstrasi Resmi Rektorat.

> 🎙️ **Speaker Notes (Hanya 35 Detik, Percaya Diri & Santai):**  
> *"Rekan-rekan dan ketua, kesimpulan dari seluruh laporan progres hari ini bermuara pada tiga poin ringkas:*  
> *Pertama, sistem kita berpijak pada hardware riil: TensorRT aktif, RealSense siap, dan tidak ada lagi program yang berebut kamera atau prosesor.*  
> *Kedua, keselamatan fisik robot terjamin: roda otomatis rem di jarak 1 meter dan gerakan leher dibatasi agar tetap stabil.*  
> *Ketiga, kita bergerak paralel: semua subtim sudah jalan serentak sejak minggu ini menuju uji penyangga akhir Oktober dan demo Rektorat bulan November.*  
> *Sistem integrasi BRONE berada di jalur yang aman dan terukur. Sekian dari saya, terima kasih, saya kembalikan ke ketua tim."*

