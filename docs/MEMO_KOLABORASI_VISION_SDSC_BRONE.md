# 📢 MEMO TEKNIS & KESEPAKATAN KOLABORASI: SINERGI VISION 🤝 KINEMATIKA BASE BRONE
## *Integrasi Visual Servoing, Kontrak Topik ROS 2, & Sintesis Dua Paper IEEE Transactions 2024*

---

> **Kepada:** Seluruh Tim Pengembang BRONE (Mas Evan, Kak Anya, Wisnu & Tim SDSC, Tim LLM, Ketua Tim)  
> **Dari:** Systems, Middleware, OS & Integration Engineer  
> **Tujuan:** Menyatukan Alur Kerja Antara Sistem Penglihatan (Vision) & Sistem Penggerak (Kinematika Base) Menuju Demo Rektorat November 2026  
> **Rujukan Teori Kontrol:** *Xu et al. (IEEE Trans. 2024)* & *Cheng et al. (IEEE Trans. 2024)*  

---

### 1. LATAR BELAKANG: MENGAPA VISION & KINEMATIKA SALING TERHUBUNG?

Di robot humanoid beroda seperti BRONE, **kamera leher (Vision)** dan **roda omniwheel (Kinematika)** tidak bisa bekerja sendiri-sendiri secara terisolasi. Jika bekerja sendiri-sendiri tanpa sinkronisasi, akan timbul 3 kendala sistematis di lapangan:
1. **Target Kabur dari Layar (*Loss of FOV*):** Jika roda SDSC meluncur atau berbelok terlalu menyentak, kamera di kepala robot akan terhentak, dan wajah target orang akan terlempar keluar dari bidang pandang kamera (*Field of View*). Akibatnya, tracking wajah Mas Evan langsung terputus!
2. **Sentakan Mekanik Roda (*Frequency Mismatch*):** Kamera visi memproses citra pada frekuensi 25–30 FPS (yang fluktuatif), sedangkan motor roda SDSC membutuhkan aliran data stabil di 20 Hz. Jika data visi langsung dikirim mentah ke roda tanpa penghalusan, roda akan bergerak patah-patah (*jerking*).
3. **Pengereman Aman 1.0 Meter (*Safety Interlock*):** Roda SDSC membutuhkan data jarak metrik riil kedalaman ($Z$) dari kamera agar bisa berhenti secara presisi tepat 1 meter di depan tamu tanpa risiko menabrak.

---

### 2. DUA RUJUKAN ILMIAH IEEE TRANSACTIONS 2024 (SOLUSI BERSAMA)

Untuk menyelesaikan ketiga kendala di atas secara elegan dan berstandar internasional, kita mengadopsi prinsip dari dua literatur kontrol robotika IEEE 2024 paling mutakhir:

* 📄 **Paper 1: Xu, Wang, & Gao (IEEE Trans. 2024)**  
  *"What Matters in Constructing a Visual Servoing Scheme: A Review of Key Issues and Solutions"*  
  * **Pelajaran Penting:** Menerapkan batasan aman virtual (*Soft-FOV Barrier*) agar pergerakan leher selalu menjaga target orang di $15\%$ area tengah layar, serta memanfaatkan koordinat 3D teraugmentasi $[u, v, Z]^T$ dari kamera depth agar sistem stabil bebas singularitas.
* 📄 **Paper 2: Cheng, Li, Zhou, dkk. (IEEE Trans. 2024)**  
  *"Vision-Motion Codesign for Low-Level Trajectory Generation in Visual Servoing Systems"*  
  * **Pelajaran Penting:** Meredam fluktuasi sampling visi dengan *Online Trajectory Smoothing* (interpolasi kurva kontinu) sehingga kecepatan motor roda dan leher tidak mengalami sentakan akselerasi (*zero-jerk spike*).

> **💡 Catatan Khusus untuk Mas Evan & Tim SDSC:**  
> Dua paper IEEE 2024 ini sangat bergengsi jika dikutip di Bab 2 (Tinjauan Pustaka) dan Bab 4 (Pengujian Sistem) skripsi/laporan tugas akhir, karena membuktikan bahwa robot BRONE dibangun di atas landasan ilmiah visual servoing termutakhir.

---

### 3. PEMBAGIAN PERAN & APA YANG DIAMBIL TIAP TIM DARI PAPER

#### A. Untuk Tim Vision (Mas Evan - Gaze Lead)
1. **Aturan Soft-FOV:** Jaga agar titik pusat wajah orang selalu dipertahankan di area tengah frame kamera.
2. **Pembatasan Kecepatan Putar Leher (*Velocity Clamping*):** Batasi pergerakan servo leher maksimal $45^\circ/\text{s}$ agar tidak timbul *motion blur*.
3. **Graceful Position Hold:** Jika target tertutup sesaat ($< 1.5\text{ detik}$), leher menahan posisi terakhir (jangan langsung sentak kembali ke nol).
4. **Kontrak Data:** Terbitkan koordinat metrik orang ke topik `/brone/target_person`. Parameter FOV ($78^\circ$ Brio $\to 86^\circ$ D455) disimpan di file YAML bersih agar skripsi aman 100%.

#### B. Untuk Tim Kinematika (Wisnu & Tim SDSC)
1. **Langganan Metadata:** Node navigasi roda cukup berlangganan topik `/brone/target_person` (bebas dari komputasi video yang berat).
2. **Peredaman Sentakan (*Trajectory Smoothing*):** Perintah kecepatan roda dihaluskan agar pergerakan 4-omniwheel meluncur mulus.
3. **Safety Interlock Auto-Stop 1.0 Meter (WAJIB):** Saat jarak terukur $Z \le 1.0\text{ meter}$, kontroler memutus translasi roda (`linear.x = 0`, `linear.y = 0`). Robot berhenti total dan menyapa tamu.

#### C. Untuk Tim Civitas Akademika (Kak Anya)
1. **Modular Subscriber:** Mengubah skrip pencocokan jas almamater UB menjadi fungsi subscriber yang menerima citra crop area dada ($160 \times 160$ px).
2. **Kontrak Output:** Terbitkan hasil deteksi string ke topik `/brone/perception/civitas` (`"MAHASISWA_UB"`, `"DOSEN"`, `"TAMU"`).

#### D. Untuk Systems & OS Engineer (Saya)
1. **Hardware Abstraction Layer (HAL):** Menyediakan driver kamera di level OS (Logitech Brio saat ini $\leftrightarrow$ RealSense D455 besok) dengan topik standar `/camera/color/image_raw`.
2. **Isolasi CPU & Latensi Jaringan:** Mengunci alokasi core CPU di Jetson & NUC agar tidak saling ganggu, serta menjamin latensi pengiriman pesan ROS 2 FastRTPS $< 2\text{ ms}$.
3. **Udev Rules & Launch Orkestrasi:** Menghapus kebutuhan `sudo` di OpenCR dan menyediakan master launch file untuk kemudahan demo.

---

### 4. MATRIKS KONTRAK DATA ROS 2 (INTERFACE CONTROL DOCUMENT)

Seluruh integrasi kita terkunci secara baku pada 5 topik utama berikut:

| Nama Topik | Tipe Pesan | Publisher | Subscriber | Fungsi Sistem |
| :--- | :--- | :--- | :--- | :--- |
| `/camera/color/image_raw` | `sensor_msgs/Image` | **OS Camera Driver** | Mas Evan, Kak Anya | Aliran citra video utama (30 FPS) |
| `/brone/target_person` | `geometry_msgs/PointStamped` | **Mas Evan (Gaze)** | Tim SDSC (Base) | Koordinat posisi tamu $[X, Y, Z]$ |
| `/robotis/head_control/set_joint_states` | `sensor_msgs/JointState` | **Mas Evan (Gaze)** | OS Controller (NUC) | Perintah sudut pan/tilt leher robot |
| `/cmd_vel` | `geometry_msgs/Twist` | **Tim SDSC (Base)** | Base OpenCR | Kecepatan roda base omniwheel (20 Hz) |
| `/brone/perception/civitas` | `std_msgs/String` | **Kak Anya (Civitas)** | NUC (State Machine) | Trigger status sapaan suara robot |

---

### 5. LANGKAH AKSI BERSAMA (ACTION PLAN MINGGU INI)

1. **Konsolidasi Baseline:** Mas Evan mendokumentasikan nilai parameter terbaik Brio & mengeluarkan konfigurasi ke YAML.
2. **Penyelarasan Topik:** Tim SDSC mencoba *subscribe* ke topik `/brone/target_person` dummy untuk menguji respon auto-stop 1.0 meter.
3. **Briefing Santai di Lab (15–20 Menit):** Kita samakan persepsi format pesan dan jadwal pengujian di meja lab.

*Mari kita wujudkan robot BRONE yang cerdas, halus pergerakannya, dan membanggakan di demonstrasi rektorat November 2026!*
