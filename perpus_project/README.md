# Sistem Perpustakaan - Tugas Akhir Django CRUD

Aplikasi sistem perpustakaan yang dibangun menggunakan framework Django dengan fokus pada implementasi operasi CRUD, penggunaan PostgreSQL, serta eksekusi database query melalui Raw SQL.

## 🎯 Tujuan Pembelajaran
Proyek ini dikembangkan untuk mengasah kemampuan dalam:
*   Membangun aplikasi web dengan **Django**.
*   Manajemen database menggunakan **PostgreSQL**.
*   Implementasi operasi **CRUD** (Create, Read, Update, Delete).
*   Memahami relasi database **One-to-Many** dan **Many-to-Many** (Pivot Table).
*   Eksekusi query database menggunakan **Raw SQL** (`connection.cursor()`).
*   Integrasi antarmuka web menggunakan **Django Templates** dan CSS Framework.

## 📖 Deskripsi Aplikasi
Aplikasi ini memungkinkan admin perpustakaan untuk mengelola data penting:
1.  **Data Buku**: Mengelola koleksi buku, kategori, rak, dan stok.
2.  **Data Siswa**: Mengelola informasi anggota perpustakaan (siswa).
3.  **Data Peminjaman**: Mencatat transaksi peminjaman buku beserta status pengembaliannya.

## 🛠️ Tech Stack
*   **Backend**: Django (Python)
*   **Database**: PostgreSQL
*   **Query**: Raw SQL (tanpa ORM)
*   **Frontend**: Django Templates & [Tailwind CSS / Bootstrap]
*   **Version Control**: Git & GitHub

## 🗄️ Struktur Database
Aplikasi ini menggunakan tiga tabel utama dengan relasi sebagai berikut:
*   **Buku**: Menyimpan detail koleksi.
*   **Siswa**: Menyimpan profil anggota.
*   **Peminjaman**: Tabel penghubung (Pivot) yang menghubungkan Siswa dan Buku dengan status peminjaman.

## 📋 Fitur Utama

### Modul Buku
- **List Buku**: Menampilkan katalog lengkap.
- **Tambah/Edit/Hapus**: Manajemen data koleksi.
- **Validasi**: Memastikan data input akurat.

### Modul Siswa
- **Manajemen User**: Tambah, detail, dan edit data siswa.
- **Status Aktif**: Penanda keaktifan siswa (Boolean).

### Modul Peminjaman
- **Transaksi**: Mencatat peminjaman dengan dropdown dinamis.
- **Status Update**: Kemudahan mengubah status dari 'Dipinjam' menjadi 'Dikembalikan'.

## 🚀 Instalasi & Cara Menjalankan
1. Clone repositori ini:
```bash
   git clone [URL-REPOSITORI-KAMU]
Buat dan aktifkan virtual environment:

Bash
   python -m venv venv
   source venv/bin/activate  # Windows: venv\Scripts\activate
Install dependencies:

Bash
   pip install -r requirements.txt
Konfigurasi database PostgreSQL di settings.py.

Jalankan server:

Bash
   python manage.py runserver
👨‍💻 Pengembangan
Proyek ini dibuat sebagai syarat tugas akhir mata kuliah/pembelajaran untuk memenuhi kriteria implementasi Raw SQL pada Django.

Dibuat oleh: Abdurrohman


---

### Tips tambahan agar profil GitHub-mu makin oke:
1.  **Screenshot**: Tambahkan folder `assets/images` di dalam proyekmu, lalu masukkan screenshot tampilan dashboard, list buku, dan form peminjaman. Setelah itu, tampilkan di dalam `README.md` dengan format `![Alt Text](assets/images/screenshot.png)`.
2.  **Badge**: Kamu bisa menambahkan badge teknologi yang digunakan di bagian atas (seperti badge Django, PostgreSQL, dan Bootstrap) agar terlihat lebih modern.
3.  **Update "Ship IT Consistently"**: Sesuai moto profil GitHub-mu, pastikan setelah selesai membuat `README.md` ini, kamu melakukan `git add`, `git commit`, dan `git push` sebagai bukti konsistensi!