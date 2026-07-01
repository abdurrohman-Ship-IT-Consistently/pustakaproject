// Tunggu sampai seluruh HTML selesai dimuat
document.addEventListener('DOMContentLoaded', function() {
    const menuBtn = document.getElementById('menu-btn');
    const closeBtn = document.getElementById('close-btn');
    const sidebar = document.getElementById('sidebar');
    const overlay = document.getElementById('overlay');

    // Cek apakah elemen ada sebelum memasang event listener
    if (menuBtn && closeBtn && sidebar && overlay) {
        function toggleSidebar() {
            sidebar.classList.toggle('-translate-x-full');
            overlay.classList.toggle('hidden');
        }

        menuBtn.addEventListener('click', toggleSidebar);
        closeBtn.addEventListener('click', toggleSidebar);
        overlay.addEventListener('click', toggleSidebar);
        console.log("Sidebar JS berhasil dimuat!");
    } else {
        console.error("Elemen sidebar tidak ditemukan di HTML!");
    }
});