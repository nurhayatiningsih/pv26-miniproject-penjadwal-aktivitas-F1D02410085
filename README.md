# pv26-miniproject-penjadwal-aktivitas-F1D02410085
PENJADWAL AKTIVITAS
Nama aplikasi: AuraPlan

Deskripsi Singkat:
AuraPlan adalah aplikasi desktop berbasis GUI yang dirancang untuk membantu pengguna mengelola dan menjadwalkan aktivitas harian secara terstruktur. Aplikasi ini memungkapan pengguna untuk menambah, melihat, mengedit, menghapus, mengekspor jadwal ke file teks, serta mencari aktivitas berdasarkan kategori atau prioritas. 

Teknologi yang Digunakan:
Bahasa Pemrograman: Python 3.13
GUI Framework: PySide6 (Binding Qt untuk Python)
Database: SQLite (Database lokal tanpa konfigurasi server)
Styling: QSS (Qt Style Sheets - CSS untuk aplikasi Qt)

Cara Kerja Aplikasi:
 Saat pengguna membuka aplikasi, mereka tidak melihat kode Python sama sekali. Yang mereka lihat hanyalah tampilan visual. Inilah alur kerja yang terjadi:

Splashscreen Sambutan: Pengguna membuka aplikasi. Yang muncul pertama adalah jendela kecil di tengah layar tanpa tombol tutup frameless. Pengguna bisa menggeser jendela ini ke mana saja menggunakan mouse (Mouse Event). Setelah mengklik tombol "Masuk ke Aplikasi", jendela ini tertutup dan menghilang.
Jendela Utama Terbuka: Pengguna dihadapkan tampilan utama yang terbagi menjadi tiga bagian:
Bagian Atas (Filter): Terdapat kotak pencarian, dropdown kategori, tombol cari, dan tombol reset.
Bagian Tengah (Tabel Data): Menampilkan seluruh jadwal yang tersimpan dalam bentuk tabel warna-warni. Kolom "Status" langsung menunjukkan mana yang sudah selesai (hijau tebal) dan yang belum (abu-abu).
Bagian Bawah (Aksi & Identitas): Ada tiga tombol besar (Tambah, Edit, Hapus) untuk mengelola data, serta identitas mahasiswa di pojok kanan bawah yang tidak bisa diubah oleh siapa pun.
Menambah Data (Create): Pengguna menekan tombol "Tambah". Muncul jendela form terpisah (Dialog) yang mengunci jendela utama agar tidak bisa diklik dua kali. Pengguna mengisi 7 form input (Teks, Kalender, Jam, Dropdown, Teks Panjang, Checkbox). Saat menekan Simpan, jendela tertutup, validasi berjalan di belakang layar, dan tabel utama langsung diperbarui otomatis.
Mencari Data (Read/Search): Pengguna bisa memfilter data secara real-time dengan mengetik di kolom pencarian, memilih kategori di dropdown, atau menekan tombol "Cari".
Mengedit Data (Update): Pengguna mengklik dua kali pada satu baris tabel, membuka Dialog yang sudah terisi data lama, mengubah isinya, dan menyimpan kembali.
Menghapus Data (Delete): Pengguna memilih satu baris dan menekan "Hapus". Muncul jendela konfirmasi "Apakah Anda yakin?". Jika "Ya", data dihapus permanen dari tabel.
*Tambahan Utilitas (Nilai Plus): Pengguna bisa mengubah font tabel (QFontDialog) atau mengekspor seluruh jadwal menjadi file .txt (QFileDialog) dengan sekali klik tanpa menggunakan fitur pihak ketiga.

Cara Menjalankan/Menggunakan Aplikasi:
1. Membuka Aplikasi
Jalankan file main.py di VS Code (klik kanan lalu pilih Run > Run), atau buka file main.py lalu tekan F5.

2. Masuk ke Jendela Utama
Akan muncul layar kecil tanpa tombol close bawaan OS (Splashscreen). Geser layar tersebut menggunakan mouse. Klik tombol "Masuk ke Aplikasi" di tengah-tengah. Jendela utama akan terbuka menampilkan jadwal kosong.

3. Menggunakan Fitur Pencarian (Filter)
Di bagian atas, terdapat kotak "Filter & Pencarian".

Cari Manual: Ketik nama aktivitas di kolom pencarian lalu tekan tombol 🔍 Cari. Tabel akan langsung difilter secara otomatis.
Filter Dropdown: Pilih "Kategori" atau "Prioritas" di dropdown. Data langsung difilter tanpa tekan tombol apapun (Real-time Filtering).
Reset: Jika ingin mengembalikan semua tampilan ke awal, klik tombol Reset.
4. Menambah Jadwal (Create)
Klik tombol "+ Tambah Aktivitas". Akan muncul form dialog baru. Isikan semua kolom yang bertanda bintang merah (*).

DateEdit (Kalender): Klik ikon kalender untuk memilih tanggal.
TimeEdit (Jam): Klik panah atas/bawah untuk mengatur jam.
ComboBox: Klik dropdown untuk memilih Kategori dan Prioritas.
CheckBox: Centang "Teks Deskripsi" sebagai catatan opsional.
Simpan: Klik tombol hijau "Simpan". Data langsung muncul di tabel utama.
5. Melihat Detail Data (Read Detail)
Arahkan kursor ke salah satu baris di tabel, lalu klik dua kali (Double-click) pada baris tersebut. Form dialog "Edit Data Aktivitas" akan terbuka berisi data lama Anda. Anda bisa mengubah datanya lalu klik "Simpan" untuk memperbarui.