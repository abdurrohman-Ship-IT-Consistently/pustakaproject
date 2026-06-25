from django.contrib import messages # Letakkan ini di baris atas jika belum ada
from django.shortcuts import render, redirect
from django.db import connection

# Helper untuk mengubah hasil query tuple menjadi dictionary
def dictfetchall(cursor):
    "Mengembalikan semua baris dari cursor sebagai dictionary"
    columns = [col[0] for col in cursor.description]
    return [dict(zip(columns, row)) for row in cursor.fetchall()]

def dictfetchone(cursor):
    "Mengembalikan satu baris dari cursor sebagai dictionary"
    columns = [col[0] for col in cursor.description]
    row = cursor.fetchone()
    if row:
        return dict(zip(columns, row))
    return None

# ==================== 1. READ (LIST BUKU) ====================
def buku_list(request):
        with connection.cursor() as cursor:
            # Mengambil data sesuai kolom di mockup gambar Anda
            cursor.execute("SELECT id, judul, pengarang, kategori, penerbit, tahun_terbit, rak, stok FROM tabel_buku ORDER BY id DESC")
            daftar_buku = dictfetchall(cursor)
        
        return render(request, 'buku/list.html', {'daftar_buku': daftar_buku})

    # ==================== 2. CREATE (TAMBAH BUKU) ====================
def buku_tambah(request):
        if request.method == 'POST':
            judul = request.POST.get('judul')
            pengarang = request.POST.get('pengarang')
            kategori = request.POST.get('kategori')
            penerbit = request.POST.get('penerbit')
            tahun_terbit = request.POST.get('tahun_terbit')
            rak = request.POST.get('rak')
            stok = request.POST.get('stok')
            deskripsi = request.POST.get('deskripsi')

            # Raw SQL Insert
            with connection.cursor() as cursor:
                cursor.execute("""
                    INSERT INTO tabel_buku (judul, pengarang, kategori, penerbit, tahun_terbit, rak, stok, deskripsi)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                """, [judul, pengarang, kategori, penerbit, tahun_terbit, rak, stok, deskripsi])
            
            return redirect('buku_list')

        # Dropdown pilihan sesuai instruksi pada gambar
        pilihan_kategori = ['Novel', 'Sejarah', 'Pendidikan']
        pilihan_rak = ['Rak A-01', 'Rak A-02', 'Rak A-03', 'Rak A-04', 'Rak A-05']
        
        context = {
            'pilihan_kategori': pilihan_kategori,
            'pilihan_rak': pilihan_rak
        }
        return render(request, 'buku/tambah.html', context)

    # ==================== 3. READ (DETAIL BUKU) ====================
def buku_detail(request, id):
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM tabel_buku WHERE id = %s", [id])
            buku = dictfetchone(cursor)
            
        return render(request, 'buku/detail.html', {'buku': buku})

    # ==================== 4. UPDATE (EDIT BUKU) ====================
def buku_edit(request, id):
        with connection.cursor() as cursor:
            if request.method == 'POST':
                judul = request.POST.get('judul')
                pengarang = request.POST.get('pengarang')
                kategori = request.POST.get('kategori')
                penerbit = request.POST.get('penerbit')
                tahun_terbit = request.POST.get('tahun_terbit')
                rak = request.POST.get('rak')
                stok = request.POST.get('stok')
                deskripsi = request.POST.get('deskripsi')

                # Raw SQL Update
                cursor.execute("""
                    UPDATE tabel_buku 
                   SET judul=%s, pengarang=%s, kategori=%s, penerbit=%s, tahun_terbit=%s, rak=%s, stok=%s, deskripsi=%s
                    WHERE id=%s
                """, [judul, pengarang, kategori, penerbit, tahun_terbit, rak, stok, deskripsi, id])
                
                return redirect('buku_list')
            
            # Ambil data lama untuk ditampilkan di form edit
            cursor.execute("SELECT * FROM tabel_buku WHERE id = %s", [id])
            buku = dictfetchone(cursor)

        pilihan_kategori = ['Novel', 'Sejarah', 'Pendidikan']
        pilihan_rak = ['Rak A-01', 'Rak A-02', 'Rak A-03', 'Rak A-04', 'Rak A-05']

        context = {
            'buku': buku,
            'pilihan_kategori': pilihan_kategori,
            'pilihan_rak': pilihan_rak
        }
        return render(request, 'buku/edit.html', context)

    # ==================== 5. DELETE (HAPUS BUKU) ====================
def buku_hapus(request, id):
        if request.method == 'POST':
            with connection.cursor() as cursor:
                cursor.execute("DELETE FROM tabel_buku WHERE id = %s", [id])
            return redirect('buku_list')
            
        with connection.cursor() as cursor:
            cursor.execute("SELECT id, judul FROM tabel_buku WHERE id = %s", [id])
            buku = dictfetchone(cursor)
            
        return render(request, 'buku/hapus_konfirmasi.html', {'buku': buku})

# ==================== 1. READ (LIST PEMINJAMAN DENGAN SQL JOIN) ====================
def peminjaman_list(request):
    with connection.cursor() as cursor:
        # TAMBAHAN 1: Update otomatis status menjadi 'Terlambat' 
        # untuk buku yang masih 'Dipinjam' tapi sudah melewati tanggal jatuh tempo
        cursor.execute("""
            UPDATE tabel_peminjaman 
            SET status = 'Terlambat' 
            WHERE status = 'Dipinjam' AND jatuh_tempo < CURRENT_DATE
        """)

        # Menggabungkan 3 tabel (JOIN) untuk mendapatkan nama siswa dan judul buku secara akurat
        cursor.execute("""
            SELECT 
                p.id, 
                s.nama AS nama_siswa, 
                b.judul AS judul_buku, 
                p.tanggal_pinjam, 
                p.jatuh_tempo, 
                p.status 
            FROM tabel_peminjaman p
            JOIN tabel_siswa s ON p.siswa_id = s.id
            JOIN tabel_buku b ON p.buku_id = b.id
            ORDER BY p.id DESC
        """)
        daftar_peminjaman = dictfetchall(cursor)
        
    return render(request, 'peminjaman/list.html', {'daftar_peminjaman': daftar_peminjaman})

# ==================== 2. CREATE (TRANSAKSI PINJAM & VALIDASI STOK) ====================
def peminjaman_tambah(request):
    with connection.cursor() as cursor:
        if request.method == 'POST':
            siswa_id = request.POST.get('siswa_id')
            buku_id = request.POST.get('buku_id')
            tanggal_pinjam = request.POST.get('tanggal_pinjam')
            jatuh_tempo = request.POST.get('jatuh_tempo')
            keperluan = request.POST.get('keperluan')

            # VALIDASI: Ambil jumlah stok buku saat ini
            cursor.execute("SELECT stok, judul FROM tabel_buku WHERE id = %s", [buku_id])
            buku = dictfetchone(cursor)

            if buku and buku['stok'] <= 0:
                # Jika stok 0 atau habis, kirim pesan error ke halaman template
                messages.error(request, f"Gagal Pinjam! Stok untuk buku '{buku['judul']}' sudah habis.")
                return redirect('peminjaman_tambah')

            # JIKA STOK AMAN: 
            # A. Masukkan data ke tabel_peminjaman
            cursor.execute("""
                INSERT INTO tabel_peminjaman (siswa_id, buku_id, tanggal_pinjam, jatuh_tempo, keperluan, status)
                VALUES (%s, %s, %s, %s, %s, 'Dipinjam')
            """, [siswa_id, buku_id, tanggal_pinjam, jatuh_tempo, keperluan])

            # B. Potong stok buku tersebut di tabel_buku
            cursor.execute("UPDATE tabel_buku SET stok = stok - 1 WHERE id = %s", [buku_id])

            messages.success(request, "Transaksi peminjaman berhasil dicatat!")
            return redirect('peminjaman_list')

        # Untuk pemuatan halaman GET: Ambil daftar siswa aktif & buku yang tersedia untuk opsi Dropdown Select
        cursor.execute("SELECT id, nama FROM tabel_siswa WHERE is_active = TRUE ORDER BY nama ASC")
        daftar_siswa = dictfetchall(cursor)

        cursor.execute("SELECT id, judul, stok FROM tabel_buku WHERE stok > 0 ORDER BY judul ASC")
        daftar_buku = dictfetchall(cursor)

    context = {
        'daftar_siswa': daftar_siswa,
        'daftar_buku': daftar_buku
    }
    return render(request, 'peminjaman/tambah.html', context)

# ==================== 3. UPDATE (PENGEMBALIAN BUKU & PEMULIHAN STOK) ====================
def peminjaman_kembali(request, id):
    if request.method == 'POST':
        with connection.cursor() as cursor:
            # Cari tahu id buku yang dipinjam pada transaksi ini
            cursor.execute("SELECT buku_id, status FROM tabel_peminjaman WHERE id = %s", [id])
            transaksi = dictfetchone(cursor)

            # TAMBAHAN 2: Izinkan pengembalian untuk status 'Dipinjam' ATAU 'Terlambat'
            if transaksi and transaksi['status'] in ['Dipinjam', 'Terlambat']:
                # A. Update status peminjaman menjadi 'Dikembalikan'
                cursor.execute("UPDATE tabel_peminjaman SET status = 'Dikembalikan' WHERE id = %s", [id])
                
                # B. Tambah/Kembalikan stok buku di tabel_buku
                cursor.execute("UPDATE tabel_buku SET stok = stok + 1 WHERE id = %s", [transaksi['buku_id']])
                messages.success(request, "Buku telah sukses dikembalikan. Stok otomatis bertambah!")

        return redirect('peminjaman_list')
    # ==================== REVISI: MODUL USER (RAW SQL) ====================

# ==================== UPDATE JALUR TEMPLATE KE FOLDER USER ====================

def user_list(request):
    with connection.cursor() as cursor:
        cursor.execute("SELECT id, nama, kelas, nis, is_active FROM tabel_siswa ORDER BY id ASC")
        users = dictfetchall(cursor)
        
    # SEKARANG mengarah ke folder user/
    return render(request, 'user/list.html', {'users': users})


def user_detail(request, id):
    with connection.cursor() as cursor:
        cursor.execute("SELECT id, nama, kelas, nis, is_active FROM tabel_siswa WHERE id = %s", [id])
        row = cursor.fetchone()
    
    if not row:
        return redirect('user_list')
        
    user = {'id': row[0], 'nama': row[1], 'kelas': row[2], 'nis': row[3], 'is_active': row[4]}
    
    # SEKARANG mengarah ke folder user/
    return render(request, 'user/detail.html', {'user': user})


def user_tambah(request):
    error_message = None
    if request.method == 'POST':
        nama = request.POST.get('nama')
        kelas = request.POST.get('kelas')
        nis = request.POST.get('nis')
        is_active = request.POST.get('is_active') == 'True'

        if not nama or not kelas or not nis:
            error_message = "Semua field wajib diisi!"
        else:
            try:
                with connection.cursor() as cursor:
                    cursor.execute(
                        "INSERT INTO tabel_siswa (nama, kelas, nis, is_active) VALUES (%s, %s, %s, %s)",
                        [nama, kelas, nis, is_active]
                    )
                return redirect('user_list')
            except Exception:
                error_message = "Gagal menambah user. Pastikan NIS tidak duplikat!"

    # SEKARANG mengarah ke folder user/
    return render(request, 'user/form.html', {'error_message': error_message, 'action': 'Tambah'})


def user_edit(request, id):
    error_message = None
    with connection.cursor() as cursor:
        cursor.execute("SELECT id, nama, kelas, nis, is_active FROM tabel_siswa WHERE id = %s", [id])
        row = cursor.fetchone()
        
    if not row:
        return redirect('user_list')
        
    user = {'id': row[0], 'nama': row[1], 'kelas': row[2], 'nis': row[3], 'is_active': row[4]}

    if request.method == 'POST':
        nama = request.POST.get('nama')
        kelas = request.POST.get('kelas')
        nis = request.POST.get('nis')
        is_active = request.POST.get('is_active') == 'True'

        if not nama or not kelas or not nis:
            error_message = "Semua field wajib diisi!"
        else:
            try:
                with connection.cursor() as cursor:
                    cursor.execute(
                        "UPDATE tabel_siswa SET nama = %s, kelas = %s, nis = %s, is_active = %s WHERE id = %s",
                        [nama, kelas, nis, is_active, id]
                    )
                return redirect('user_list')
            except Exception:
                error_message = "Gagal memperbarui user. Pastikan NIS unik!"

    # SEKARANG mengarah ke folder user/
    return render(request, 'user/form.html', {'user': user, 'error_message': error_message, 'action': 'Edit'})


def user_hapus(request, id):
    if request.method == 'POST':
        with connection.cursor() as cursor:
            cursor.execute("DELETE FROM tabel_siswa WHERE id = %s", [id])
        return redirect('user_list')
        
    with connection.cursor() as cursor:
        cursor.execute("SELECT id, nama FROM tabel_siswa WHERE id = %s", [id])
        row = cursor.fetchone()
        
    if not row:
        return redirect('user_list')
        
    # SEKARANG mengarah ke folder user/
    return render(request, 'user/hapus.html', {'user': {'id': row[0], 'nama': row[1]}})
    
# ==================== REVISI LOGIK AGREGASI DASHBOARD (RAW SQL COMPLETION) ====================
def dashboard(request):
    with connection.cursor() as cursor:
        # 1. Hitung total seluruh UNIT buku yang ada di perpustakaan (SUM dari kolom stok)
        cursor.execute("SELECT COALESCE(SUM(stok), 0) FROM tabel_buku")
        total_buku = cursor.fetchone()[0]

        # 2. Hitung total JUDUL koleksi buku (COUNT baris)
        cursor.execute("SELECT COUNT(*) FROM tabel_buku")
        total_judul = cursor.fetchone()[0]

        # 3. Hitung buku yang sedang aktif dipinjam
        cursor.execute("SELECT COUNT(*) FROM tabel_peminjaman WHERE status = 'Dipinjam'")
        sedang_dipinjam = cursor.fetchone()[0]

        # 4. Hitung buku yang sudah sukses dikembalikan
        cursor.execute("SELECT COUNT(*) FROM tabel_peminjaman WHERE status = 'Dikembalikan'")
        sudah_dikembalikan = cursor.fetchone()[0]

        # 5. Ambil daftar judul buku beserta stoknya untuk visualisasi grafik distribusi
        cursor.execute("SELECT judul, stok FROM tabel_buku ORDER BY judul ASC")
        # Menggunakan helper dictfetchall yang sudah kita buat pada langkah sebelumnya
        distribusi_stok = dictfetchall(cursor)

    context = {
        'total_buku': total_buku,
        'total_judul': total_judul,
        'sedang_dipinjam': sedang_dipinjam,
        'sudah_dikembalikan': sudah_dikembalikan,
        'distribusi_stok': distribusi_stok
    }
    return render(request, 'dashboard.html', context)