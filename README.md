# 📖 Aplikasi Resep Makanan Sederhana

Repository ini berisi proyek pengembangan aplikasi desktop sederhana berbasis GUI Python menggunakan Tkinter, yang berfungsi untuk memudahkan pengguna dalam mengelola resep makanan. Aplikasi ini dirancang dengan tujuan memberikan kemudahan dalam penambahan, pengeditan, pencarian, penghapusan, pengurutan resep, serta ekspor/impor data resep dalam format CSV.

---

## 🎯 Tujuan Program

Tujuan utama aplikasi ini adalah menyediakan platform sederhana, interaktif, dan efisien untuk mengelola kumpulan resep makanan. Dengan aplikasi ini, pengguna dapat dengan cepat melakukan manajemen resep pribadi maupun koleksi masakan lainnya secara digital, rapi, dan mudah diakses.

---

## 🚀 Fitur Program

Aplikasi ini memiliki fitur-fitur berikut:

1. **Tambah Resep Baru**

   * Menambahkan resep baru dengan detail judul, bahan, langkah-langkah, dan waktu pembuatan.
   * Validasi otomatis untuk menghindari duplikasi judul resep.

2. **Lihat Resep**

   * Menampilkan daftar resep yang terdaftar dengan jelas dan interaktif.
   * Menampilkan detail resep saat resep dipilih (judul, bahan, langkah-langkah, waktu).

3. **Edit Resep**

   * Mengubah detail resep yang sudah ada dengan validasi duplikasi judul.

4. **Hapus Resep**

   * Menghapus satu atau beberapa resep sekaligus dengan konfirmasi pengguna.
   * Dapat menghapus seluruh resep secara massal.

5. **Pencarian Resep**

   * Pencarian berdasarkan judul (mendukung pencarian fuzzy untuk mengatasi typo).
   * Pencarian berdasarkan bahan-bahan tertentu.
   * Filter berdasarkan durasi waktu maksimal pembuatan.

6. **Pengurutan Resep**

   * Urut berdasarkan nama atau waktu.
   * Pilihan pengurutan secara ascending (menaik) dan descending (menurun).

7. **Ekspor dan Impor Data**

   * Menyimpan semua resep ke dalam file CSV untuk backup atau sharing.
   * Memuat resep dari file CSV dengan validasi otomatis.

---

## ⚙️ Teknologi yang Digunakan

* **Python** (versi 3.x)
* **Tkinter** (untuk GUI)
* **CSV** (penyimpanan data eksternal)

---

## 🔍 Algoritma Utama

Aplikasi ini menerapkan dua algoritma utama:

### 📌 1. Algoritma Pencarian

* **Linear Search**: Mencari data resep berdasarkan nama atau bahan secara berurutan.
* **Fuzzy Search (Levenshtein Distance)**: Menangani typo saat mencari judul resep, memberikan saran hasil pencarian yang mendekati kata yang dimasukkan pengguna.

### 📌 2. Algoritma Pengurutan

* **Insertion Sort**: Mengurutkan resep berdasarkan nama atau waktu secara efisien, terutama ideal untuk jumlah data resep yang tidak terlalu besar.

---

## 📂 Struktur File dan Folder

Struktur repository ini adalah sebagai berikut:

```bash
.
├── REVISI YANG UDAH FIXS.py    # Kode program utama (file Python)
├── resep.csv                   # Contoh file CSV untuk ekspor/impor (opsional)
└── README.md                   # Dokumentasi lengkap aplikasi (file ini)
```

---

## 🧩 Penjelasan Kode Program

Struktur kode utama (`REVISI YANG UDAH FIXS.py`) terdiri dari beberapa bagian utama berikut:

### **1. Struktur Data**

* Menggunakan `namedtuple Recipe` untuk menyimpan data resep secara jelas.
* Penyimpanan dalam array statis terbatas (maksimal 40 resep).

### **2. Fungsi Utilitas**

* **`normalize_title()`**: Normalisasi judul resep untuk menghindari duplikasi.
* **`number_lines()`**: Penomoran otomatis bahan dan langkah resep.
* **`levenshtein()`**: Menghitung jarak edit untuk fitur fuzzy searching.

### **3. GUI dan Operasi Resep**

* Menambah, menyimpan, menghapus resep melalui GUI.
* Validasi input pengguna secara menyeluruh.

### **4. Pencarian & Pengurutan**

* Pencarian berdasarkan judul, bahan, dan waktu resep.
* Pengurutan berdasarkan nama atau waktu resep dengan algoritma insertion sort.

### **5. Impor & Ekspor Data**

* Fungsi ekspor (`export_csv`) dan impor (`load_csv`) data resep dalam file CSV.

---

## 📌 Cara Menjalankan Aplikasi

1. **Persyaratan**

   * Pastikan Python versi 3.x sudah terinstal.
   * Tidak memerlukan instalasi tambahan karena menggunakan pustaka bawaan Python.

2. **Menjalankan Program**

   * Unduh atau clone repository ini.
   * Buka terminal atau command prompt di direktori tempat menyimpan file.
   * Jalankan perintah:

     ```bash
     python "REVISI YANG UDAH FIXS.py"
     ```

3. **Menggunakan Aplikasi**

   * Gunakan fitur-fitur melalui tombol dan form yang tersedia di GUI aplikasi.
   * Ikuti petunjuk validasi untuk memasukkan data resep yang tepat.
   * Manfaatkan fitur ekspor/impor CSV untuk kemudahan backup dan sharing.

---

## 📸 Screenshot GUI Aplikasi

![image](https://github.com/user-attachments/assets/51bf1825-7a0a-480b-8d05-b58611f965f1)



---

## ✨ Keunggulan Aplikasi

* **Mudah Digunakan**: GUI yang intuitif dan interaktif.
* **Validasi Ketat**: Menghindari kesalahan input yang umum terjadi.
* **Pengelolaan Data Praktis**: Ekspor dan impor mudah melalui CSV.
* **Algoritma Efektif**: Implementasi fuzzy search dan insertion sort meningkatkan pengalaman pengguna.

---

## 🔖 Lisensi

Proyek ini bersifat open-source dan bebas digunakan atau dimodifikasi untuk keperluan edukasi dan non-komersial.

*(Tambahkan lisensi sesuai kebutuhan proyek Anda, misalnya MIT License.)*

---

## 🚧 Rencana Pengembangan Selanjutnya

* Menambahkan database lokal untuk penyimpanan yang lebih aman dan terstruktur.
* Integrasi dengan fitur berbagi resep secara online.
* Menambah fitur login dan autentikasi pengguna untuk keamanan data pribadi.

---

## 📫 Kontak Pengembang

Jika Anda memiliki saran, pertanyaan, atau masukan lebih lanjut, silakan menghubungi pengembang proyek:

* **Nama**: *(Tambahkan nama Anda)*
* **Email**: *(Tambahkan email Anda)*
* **GitHub**: *(Tambahkan link GitHub Anda)*

---

Terima kasih telah menggunakan aplikasi ini! Jangan lupa untuk memberikan ⭐️ jika Anda menyukai proyek ini. Selamat memasak! 🍳🥗😊

---

