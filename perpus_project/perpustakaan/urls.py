from django.urls import path
from . import views

urlpatterns = [
    # Halaman Utama diubah menjadi Dashboard
    path('', views.dashboard, name='dashboard'), 

    # Routing Buku (Alamatnya sekarang menjadi /buku/)
    path('buku/', views.buku_list, name='buku_list'),
    path('buku/tambah/', views.buku_tambah, name='buku_tambah'),
    path('buku/detail/<int:id>/', views.buku_detail, name='buku_detail'),
    path('buku/edit/<int:id>/', views.buku_edit, name='buku_edit'),
    path('buku/hapus/<int:id>/', views.buku_hapus, name='buku_hapus'),

    # Routing Peminjaman
    path('peminjaman/', views.peminjaman_list, name='peminjaman_list'),
    path('peminjaman/tambah/', views.peminjaman_tambah, name='peminjaman_tambah'),
    path('peminjaman/kembali/<int:id>/', views.peminjaman_kembali, name='peminjaman_kembali'),

# URL Modul User (Revisi dari Siswa)
    path('user/', views.user_list, name='user_list'),
    path('user/tambah/', views.user_tambah, name='user_tambah'),
    path('user/detail/<int:id>/', views.user_detail, name='user_detail'),
    path('user/edit/<int:id>/', views.user_edit, name='user_edit'),
    path('user/hapus/<int:id>/', views.user_hapus, name='user_hapus'),
]