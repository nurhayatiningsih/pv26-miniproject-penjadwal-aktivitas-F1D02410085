from PySide6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QLineEdit, QComboBox, QPushButton,
    QTableWidget, QTableWidgetItem, QHeaderView,
    QGroupBox, QAbstractItemView, QMessageBox
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QColor, QKeyEvent, QCloseEvent


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("AuraPlan")
        self.resize(900, 620)
        self.setMinimumSize(420, 500)
        self._setup_ui()

    def _setup_ui(self):
        self._setup_menu_bar()
        
        central = QWidget()
        self.setCentralWidget(central)
        
        self.main_layout = QVBoxLayout(central)
        self.main_layout.setContentsMargins(15, 10, 15, 10)
        self.main_layout.setSpacing(10)
        
        self._setup_filter_bar()
        self._setup_table()
        self._setup_action_buttons()
        self._setup_student_info()
        self._setup_status_bar()

    def _setup_student_info(self):
        from utils.constants import STUDENT_NAME, STUDENT_NIM
        
        lbl_info = QLabel(f"👤 {STUDENT_NAME}  |  NIM: {STUDENT_NIM}")
        lbl_info.setObjectName("labelStudentFooter")
        lbl_info.setAlignment(Qt.AlignCenter)
        self.main_layout.addWidget(lbl_info)

    def _setup_menu_bar(self):
        menu_bar = self.menuBar()

        self.menu_file = menu_bar.addMenu("File")
        self.action_export_txt = self.menu_file.addAction("Export Jadwal ke .txt")
        self.menu_file.addSeparator()
        self.action_keluar = self.menu_file.addAction("Keluar")

        self.menu_edit = menu_bar.addMenu("Edit")
        self.action_find_replace = self.menu_edit.addAction("Cari & Ganti Deskripsi")
        self.menu_edit.addSeparator()
        self.action_ubah_font = self.menu_edit.addAction("Ubah Font Tabel")

        self.menu_bantuan = menu_bar.addMenu("Bantuan")
        self.action_tentang = self.menu_bantuan.addAction("Tentang Aplikasi")

    def _setup_filter_bar(self):
        group = QGroupBox("Filter & Pencarian")
        group.setObjectName("groupFilter")
        lay = QHBoxLayout(group)
        lay.setContentsMargins(12, 8, 12, 8)
        lay.setSpacing(8)

        lay.addWidget(QLabel("Cari:"))
        self.input_cari = QLineEdit()
        self.input_cari.setPlaceholderText("Ketik nama aktivitas…")
        self.input_cari.setClearButtonEnabled(True)
        lay.addWidget(self.input_cari)

        lay.addWidget(QLabel("Kategori:"))
        self.combo_kategori = QComboBox()
        self.combo_kategori.setMinimumWidth(110)
        lay.addWidget(self.combo_kategori)

        lay.addWidget(QLabel("Prioritas:"))
        self.combo_prioritas = QComboBox()
        self.combo_prioritas.setMinimumWidth(110)
        lay.addWidget(self.combo_prioritas)

        lay.addStretch()

        self.btn_cari = QPushButton("🔍 Cari")
        self.btn_cari.setObjectName("btnCari")
        self.btn_cari.setCursor(Qt.PointingHandCursor)
        lay.addWidget(self.btn_cari)

        self.btn_reset = QPushButton("Reset")
        self.btn_reset.setObjectName("btnReset")
        self.btn_reset.setCursor(Qt.PointingHandCursor)
        lay.addWidget(self.btn_reset)

        self.main_layout.addWidget(group)

    def _setup_table(self):
        group = QGroupBox("Daftar Aktivitas")
        group.setObjectName("groupTable")
        lay = QVBoxLayout(group)
        lay.setContentsMargins(12, 8, 12, 8)

        self.table = QTableWidget()
        self.table.setColumnCount(9)
        self.table.setHorizontalHeaderLabels([
            "No", "Nama Aktivitas", "Tanggal", "Waktu Mulai",
            "Waktu Selesai", "Kategori", "Prioritas", "Status", "Deskripsi"
        ])
        self.table.setAlternatingRowColors(True)
        self.table.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.table.setSelectionMode(QAbstractItemView.SingleSelection)
        self.table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.table.verticalHeader().setVisible(False)

        hdr = self.table.horizontalHeader()
        hdr.setSectionResizeMode(0, QHeaderView.ResizeToContents)
        hdr.setSectionResizeMode(1, QHeaderView.Stretch)
        hdr.setSectionResizeMode(2, QHeaderView.ResizeToContents)
        hdr.setSectionResizeMode(3, QHeaderView.ResizeToContents)
        hdr.setSectionResizeMode(4, QHeaderView.ResizeToContents)
        hdr.setSectionResizeMode(5, QHeaderView.ResizeToContents)
        hdr.setSectionResizeMode(6, QHeaderView.ResizeToContents)
        hdr.setSectionResizeMode(7, QHeaderView.ResizeToContents)
        hdr.setSectionResizeMode(8, QHeaderView.Stretch)

        lay.addWidget(self.table)
        self.main_layout.addWidget(group)

    def _setup_action_buttons(self):
        lay = QHBoxLayout()
        lay.setSpacing(8)

        self.btn_tambah = QPushButton("+ Tambah Aktivitas")
        self.btn_tambah.setObjectName("btnTambah")
        self.btn_tambah.setCursor(Qt.PointingHandCursor)

        self.btn_edit = QPushButton("✏  Edit")
        self.btn_edit.setObjectName("btnEdit")
        self.btn_edit.setCursor(Qt.PointingHandCursor)

        self.btn_hapus = QPushButton("🗑  Hapus")
        self.btn_hapus.setObjectName("btnHapus")
        self.btn_hapus.setCursor(Qt.PointingHandCursor)

        self.lbl_total = QLabel("Total: 0 aktivitas")
        self.lbl_total.setObjectName("labelTotal")

        lay.addWidget(self.btn_tambah)
        lay.addWidget(self.btn_edit)
        lay.addWidget(self.btn_hapus)
        lay.addStretch()
        lay.addWidget(self.lbl_total)
        
        self.main_layout.addLayout(lay)

    def _setup_status_bar(self):
        self.status_bar = self.statusBar()
        self.status_bar.showMessage("Siap")

    def populate_filter_combos(self, kategori_list, prioritas_list):
        self.combo_kategori.clear()
        self.combo_kategori.addItems(kategori_list)
        self.combo_prioritas.clear()
        self.combo_prioritas.addItems(prioritas_list)

    def update_table(self, rows, prioritas_colors, kategori_colors):
        self.table.setRowCount(len(rows))

        for r, item in enumerate(rows):
            cell_no = QTableWidgetItem(str(r + 1))
            cell_no.setTextAlignment(Qt.AlignCenter)
            cell_no.setData(Qt.UserRole, item["id"])
            self.table.setItem(r, 0, cell_no)

            self.table.setItem(r, 1, QTableWidgetItem(item.get("nama_aktivitas", "")))

            cell_tgl = QTableWidgetItem(item.get("tanggal_display", ""))
            cell_tgl.setTextAlignment(Qt.AlignCenter)
            self.table.setItem(r, 2, cell_tgl)

            cell_mulai = QTableWidgetItem(item.get("waktu_mulai", ""))
            cell_mulai.setTextAlignment(Qt.AlignCenter)
            self.table.setItem(r, 3, cell_mulai)

            cell_selesai = QTableWidgetItem(item.get("waktu_selesai", ""))
            cell_selesai.setTextAlignment(Qt.AlignCenter)
            self.table.setItem(r, 4, cell_selesai)

            kat = item.get("kategori", "")
            cell_kat = QTableWidgetItem(kat)
            cell_kat.setTextAlignment(Qt.AlignCenter)
            if kat in kategori_colors:
                color = QColor(kategori_colors[kat])
                color.setAlpha(210)
                cell_kat.setBackground(color)
                cell_kat.setForeground(Qt.white)
            self.table.setItem(r, 5, cell_kat)

            pri = item.get("prioritas", "")
            cell_pri = QTableWidgetItem(pri)
            cell_pri.setTextAlignment(Qt.AlignCenter)
            if pri in prioritas_colors:
                color = QColor(prioritas_colors[pri])
                color.setAlpha(210)
                cell_pri.setBackground(color)
                cell_pri.setForeground(Qt.white)
            self.table.setItem(r, 6, cell_pri)

            status = item.get("status", "Belum")
            cell_status = QTableWidgetItem(status)
            cell_status.setTextAlignment(Qt.AlignCenter)
            if status == "Sudah":
                cell_status.setForeground(QColor("#27AE60"))
                font = cell_status.font()
                font.setBold(True)
                cell_status.setFont(font)
            else:
                cell_status.setForeground(QColor("#95A5A6"))
            self.table.setItem(r, 7, cell_status)

            self.table.setItem(r, 8, QTableWidgetItem(item.get("deskripsi") or "-"))

        self.lbl_total.setText(f"Total: {len(rows)} aktivitas")

    def get_selected_id(self):
        row = self.table.currentRow()
        if row < 0:
            return None
        item = self.table.item(row, 0)
        return item.data(Qt.UserRole) if item else None

    def clear_table(self):
        self.table.setRowCount(0)
        self.lbl_total.setText("Total: 0 aktivitas")

    def keyPressEvent(self, event):
        if event.key() in (Qt.Key_Return, Qt.Key_Enter):
            self.input_cari.setFocus()
            self.input_cari.selectAll()
        elif event.key() == Qt.Key_Escape:
            self.input_cari.clear()
            self.combo_kategori.setCurrentText("Semua")
            self.combo_prioritas.setCurrentText("Semua")
        else:
            super().keyPressEvent(event)

    def closeEvent(self, event):
        reply = QMessageBox.question(
            self, "Konfirmasi Keluar",
            "Apakah Anda yakin ingin keluar dari aplikasi?\n\n"
            "Pastikan semua perubahan sudah disimpan.",
            QMessageBox.Yes | QMessageBox.No, QMessageBox.No
        )
        if reply == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()