from django.db import models

class TabelBuku(models.Model):
    judul = models.CharField(max_length=255)
    pengarang = models.CharField(max_length=255)
    kategori = models.CharField(max_length=100)
    penerbit = models.CharField(max_length=255)
    tahun_terbit = models.CharField(max_length=4, blank=True, null=True)
    rak = models.CharField(max_length=50, blank=True, null=True)
    stok = models.IntegerField(default=0)
    deskripsi = models.TextField(blank=True, null=True)

    class Meta:
        db_table = 'tabel_buku'


class TabelSiswa(models.Model):
    nama = models.CharField(max_length=255)
    kelas = models.CharField(max_length=50)
    nis = models.CharField(max_length=50, unique=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = 'tabel_siswa'


class TabelPeminjaman(models.Model):
    STATUS_CHOICES = [
        ('Dipinjam', 'Dipinjam'),
        ('Dikembalikan', 'Dikembalikan'),
        ('Terlambat', 'Terlambat'),
    ]
    tanggal_pinjam = models.DateField()
    jatuh_tempo = models.DateField()
    keperluan = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='Dipinjam')
    buku = models.ForeignKey(TabelBuku, on_delete=models.CASCADE)
    siswa = models.ForeignKey(TabelSiswa, on_delete=models.CASCADE)

    class Meta:
        db_table = 'tabel_peminjaman'