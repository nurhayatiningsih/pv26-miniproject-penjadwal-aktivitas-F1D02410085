from PySide6.QtWidgets import QMessageBox, QFontDialog, QFileDialog

from utils.constants import (
    APP_NAME, APP_VERSION, APP_DESCRIPTION, 
    STUDENT_NAME, STUDENT_NIM,
    KATEGORI_OPTIONS, PRIORITAS_OPTIONS, FILTER_SEMUA, 
    PRIORITAS_COLORS, KATEGORI_COLORS
)
from database.db_manager import DatabaseManager
from models.aktivitas import validate_aktivitas, format_tanggal
from views.dialog_aktivitas import DialogAktivitas
from views.dialog_about import DialogAbout
from views.dialog_welcome import DialogWelcome
from views.dialog_find_replace import DialogFindReplace


class AktivitasController:
    def __init__(self, view):
        self.view = view
        self.db = DatabaseManager()
        self._connect_signals()
        self._init_view()
        self._show_welcome()
        self.load_data()

    def _connect_signals(self):
        v = self.view
        
        v.action_keluar.triggered.connect(v.close)
        v.action_tentang.triggered.connect(self._show_about)
        v.action_export_txt.triggered.connect(self._export_to_txt)
        v.action_ubah_font.triggered.connect(self._ubah_font)
        v.action_find_replace.triggered.connect(self._find_replace)

        v.btn_tambah.clicked.connect(self._on_tambah)
        v.btn_edit.clicked.connect(self._on_edit)
        v.btn_hapus.clicked.connect(self._on_hapus)
        v.btn_cari.clicked.connect(self.load_data)
        v.combo_kategori.currentTextChanged.connect(self.load_data)
        v.combo_prioritas.currentTextChanged.connect(self.load_data)
        v.btn_reset.clicked.connect(self._on_reset_filter)
        
        v.table.cellDoubleClicked.connect(lambda r, c: self._on_edit())

    def _init_view(self):
        self.view.populate_filter_combos(
            [FILTER_SEMUA] + KATEGORI_OPTIONS,
            [FILTER_SEMUA] + PRIORITAS_OPTIONS,
        )

    def load_data(self):
        keyword = self.view.input_cari.text().strip()
        kategori = self.view.combo_kategori.currentText()
        prioritas = self.view.combo_prioritas.currentText()

        if keyword or kategori != FILTER_SEMUA or prioritas != FILTER_SEMUA:
            data = self.db.search(keyword, kategori, prioritas)
        else:
            data = self.db.read_all()

        for item in data:
            item["tanggal_display"] = format_tanggal(item.get("tanggal", ""))

        self.view.update_table(data, PRIORITAS_COLORS, KATEGORI_COLORS)
        self.view.status_bar.showMessage(f"Menampilkan {len(data)} aktivitas")

    def _on_tambah(self):
        dlg = DialogAktivitas(
            parent=self.view, mode="tambah",
            kategori_options=KATEGORI_OPTIONS, 
            prioritas_options=PRIORITAS_OPTIONS
        )
        if dlg.exec() == DialogAktivitas.Accepted:
            data = dlg.get_data()
            ok, msg = validate_aktivitas(data)
            if not ok:
                QMessageBox.warning(self.view, "Validasi Gagal", msg)
                return
            try:
                self.db.create(data)
                self.load_data()
                self.view.status_bar.showMessage("Aktivitas berhasil ditambahkan!", 3000)
                QMessageBox.information(self.view, "Berhasil", "Aktivitas baru berhasil ditambahkan!")
            except Exception as e:
                QMessageBox.critical(self.view, "Error", f"Gagal menyimpan data:\n{e}")

    def _on_edit(self):
        sel_id = self.view.get_selected_id()
        if sel_id is None:
            QMessageBox.warning(self.view, "Peringatan", "Pilih satu aktivitas yang ingin diedit!")
            return

        data = self.db.read_by_id(sel_id)
        if data is None:
            QMessageBox.critical(self.view, "Error", "Data tidak ditemukan di database!")
            return

        dlg = DialogAktivitas(
            parent=self.view, mode="edit",
            kategori_options=KATEGORI_OPTIONS, 
            prioritas_options=PRIORITAS_OPTIONS
        )
        dlg.set_data(data)

        if dlg.exec() == DialogAktivitas.Accepted:
            new_data = dlg.get_data()
            ok, msg = validate_aktivitas(new_data)
            if not ok:
                QMessageBox.warning(self.view, "Validasi Gagal", msg)
                return
            try:
                self.db.update(sel_id, new_data)
                self.load_data()
                self.view.status_bar.showMessage("Aktivitas berhasil diperbarui!", 3000)
                QMessageBox.information(self.view, "Berhasil", "Data aktivitas berhasil diperbarui!")
            except Exception as e:
                QMessageBox.critical(self.view, "Error", f"Gagal mengupdate data:\n{e}")

    def _on_hapus(self):
        sel_id = self.view.get_selected_id()
        if sel_id is None:
            QMessageBox.warning(self.view, "Peringatan", "Pilih satu aktivitas yang ingin dihapus!")
            return

        data = self.db.read_by_id(sel_id)
        nama = data["nama_aktivitas"] if data else "ini"

        reply = QMessageBox.question(
            self.view, "Konfirmasi Hapus",
            f"Apakah Anda yakin ingin menghapus aktivitas\n<b>\"{nama}\"</b>?\n\n"
            f"Tindakan ini tidak dapat dibatalkan.",
            QMessageBox.Yes | QMessageBox.No, QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            try:
                self.db.delete(sel_id)
                self.load_data()
                self.view.status_bar.showMessage("Aktivitas berhasil dihapus!", 3000)
                QMessageBox.information(self.view, "Berhasil", "Aktivitas berhasil dihapus!")
            except Exception as e:
                QMessageBox.critical(self.view, "Error", f"Gagal menghapus data:\n{e}")

    def _on_reset_filter(self):
        self.view.input_cari.clear()
        self.view.combo_kategori.setCurrentText("Semua")
        self.view.combo_prioritas.setCurrentText("Semua")
        self.load_data()
        self.view.status_bar.showMessage("Filter direset", 2000)

    def _show_welcome(self):
        welcome = DialogWelcome(self.view)
        if welcome.exec() != DialogWelcome.Accepted:
            self.view.close()

    def _show_about(self):
        DialogAbout(
            app_name=APP_NAME, 
            app_version=APP_VERSION, 
            app_description=APP_DESCRIPTION,
            student_name=STUDENT_NAME, 
            student_nim=STUDENT_NIM, 
            parent=self.view
        ).exec()

    def _ubah_font(self):
        current_font = self.view.table.font()
        font, ok = QFontDialog.getFont(current_font, self.view, "Pilih Font Tabel")
        if ok:
            self.view.table.setFont(font)

    def _export_to_txt(self):
        file_path, _ = QFileDialog.getSaveFileName(
            self.view, "Export Jadwal", "jadwal_aktivitas.txt", "Text Files (*.txt)"
        )
        if not file_path:
            return

        data = self.db.read_all()
        try:
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(f"{'='*50}\n")
                f.write("  JADWAL AURAPLAN\n")
                f.write(f"{'='*50}\n\n")
                
                if not data:
                    f.write("Tidak ada aktivitas.\n")
                
                for i, item in enumerate(data, 1):
                    status = item.get("status", "Belum")
                    f.write(f"{i}. {item['nama_aktivitas']} [{'SUDAH' if status == 'Sudah' else 'BELUM'}]\n")
                    f.write(f"   Tanggal   : {item['tanggal']}\n")
                    f.write(f"   Waktu     : {item['waktu_mulai']} - {item['waktu_selesai']}\n")
                    f.write(f"   Kategori  : {item['kategori']} ({item['prioritas']})\n")
                    if item['deskripsi']:
                        f.write(f"   Deskripsi : {item['deskripsi']}\n")
                    f.write("-" * 50 + "\n")
                    
            self.view.status_bar.showMessage(f"Berhasil export ke {file_path}", 4000)
            QMessageBox.information(self.view, "Export Berhasil", f"Jadwal berhasil disimpan ke:\n{file_path}")
        except Exception as e:
            QMessageBox.critical(self.view, "Error", f"Gagal menyimpan file:\n{e}")

    def _find_replace(self):
        sel_id = self.view.get_selected_id()
        if sel_id is None:
            QMessageBox.warning(
                self.view, "Peringatan", 
                "Pilih satu aktivitas terlebih dahulu!\n"
                "Find & Replace akan mengubah teks di kolom 'Deskripsi'."
            )
            return

        dlg = DialogFindReplace(self.view)
        if dlg.exec() == DialogFindReplace.Accepted:
            kata_cari, kata_ganti = dlg.get_data()
            if not kata_cari:
                return
            
            data = self.db.read_by_id(sel_id)
            if data:
                deskripsi_lama = data.get("deskripsi", "")
                if kata_cari in deskripsi_lama:
                    deskripsi_baru = deskripsi_lama.replace(kata_cari, kata_ganti)
                    self.db.update(sel_id, {**data, "deskripsi": deskripsi_baru})
                    self.load_data()
                    QMessageBox.information(self.view, "Berhasil", "Teks di deskripsi berhasil diganti!")
                else:
                    QMessageBox.information(self.view, "Tidak Ditemukan", f'Teks "{kata_cari}" tidak ditemukan di deskripsi.')