from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QFormLayout,
    QLineEdit, QDateEdit, QTimeEdit, QComboBox,
    QTextEdit, QPushButton, QLabel, QMessageBox, QCheckBox
)
from PySide6.QtCore import Qt, QDate, QTime


class DialogAktivitas(QDialog):
    def __init__(self, parent=None, mode="tambah", kategori_options=None, prioritas_options=None):
        super().__init__(parent)
        self.mode = mode
        self._kat_opts = kategori_options or []
        self._pri_opts = prioritas_options or []
        self._build_ui()

    def _build_ui(self):
        title = "Tambah Aktivitas Baru" if self.mode == "tambah" else "Edit Data Aktivitas"
        self.setWindowTitle(title)
        self.setMinimumWidth(420)
        self.setModal(True)

        root = QVBoxLayout(self)
        root.setSpacing(15)
        root.setContentsMargins(25, 20, 25, 20)

        lbl_title = QLabel(title)
        lbl_title.setObjectName("labelDialogTitle")
        lbl_title.setAlignment(Qt.AlignCenter)
        root.addWidget(lbl_title)

        self.check_selesai = QCheckBox("Tandai sebagai Sudah Dilakukan")
        self.check_selesai.setObjectName("checkBoxFilter")
        root.addWidget(self.check_selesai)

        form = QFormLayout()
        form.setSpacing(12)
        form.setLabelAlignment(Qt.AlignRight | Qt.AlignVCenter)

        self.input_nama = QLineEdit()
        self.input_nama.setPlaceholderText("Masukkan nama aktivitas…")
        form.addRow("Nama Aktivitas *:", self.input_nama)

        self.input_tanggal = QDateEdit()
        self.input_tanggal.setCalendarPopup(True)
        self.input_tanggal.setDisplayFormat("dd MMMM yyyy")
        self.input_tanggal.setDate(QDate.currentDate())
        form.addRow("Tanggal *:", self.input_tanggal)

        self.input_mulai = QTimeEdit()
        self.input_mulai.setDisplayFormat("HH:mm")
        self.input_mulai.setTime(QTime(8, 0))
        form.addRow("Waktu Mulai *:", self.input_mulai)

        self.input_selesai = QTimeEdit()
        self.input_selesai.setDisplayFormat("HH:mm")
        self.input_selesai.setTime(QTime(9, 0))
        form.addRow("Waktu Selesai *:", self.input_selesai)

        self.combo_kategori = QComboBox()
        self.combo_kategori.addItems(self._kat_opts)
        form.addRow("Kategori *:", self.combo_kategori)

        self.combo_prioritas = QComboBox()
        self.combo_prioritas.addItems(self._pri_opts)
        form.addRow("Prioritas *:", self.combo_prioritas)

        self.input_deskripsi = QTextEdit()
        self.input_deskripsi.setPlaceholderText("Catatan tambahan (opsional)…")
        self.input_deskripsi.setMaximumHeight(80)
        form.addRow("Deskripsi:", self.input_deskripsi)

        root.addLayout(form)

        lbl_info = QLabel("* Field wajib diisi")
        lbl_info.setObjectName("labelInfo")
        root.addWidget(lbl_info)

        btn_lay = QHBoxLayout()
        btn_lay.addStretch()

        self.btn_simpan = QPushButton("Simpan")
        self.btn_simpan.setObjectName("btnSimpan")
        self.btn_simpan.setCursor(Qt.PointingHandCursor)
        self.btn_simpan.setDefault(True)

        self.btn_batal = QPushButton("Batal")
        self.btn_batal.setObjectName("btnBatal")
        self.btn_batal.setCursor(Qt.PointingHandCursor)

        btn_lay.addWidget(self.btn_simpan)
        btn_lay.addWidget(self.btn_batal)
        root.addLayout(btn_lay)

        self.btn_simpan.clicked.connect(self._on_simpan)
        self.btn_batal.clicked.connect(self.reject)

    def _on_simpan(self):
        data = self.get_data()
        if not data["nama_aktivitas"].strip():
            QMessageBox.warning(self, "Validasi Gagal", "Nama aktivitas wajib diisi!")
            self.input_nama.setFocus()
            return
        if data["waktu_selesai"] <= data["waktu_mulai"]:
            QMessageBox.warning(self, "Validasi Gagal", "Waktu selesai harus setelah waktu mulai!")
            self.input_selesai.setFocus()
            return
        self.accept()

    def get_data(self):
        status = "Sudah" if self.check_selesai.isChecked() else "Belum"
        return {
            "nama_aktivitas": self.input_nama.text().strip(),
            "tanggal": self.input_tanggal.date().toString("yyyy-MM-dd"),
            "waktu_mulai": self.input_mulai.time().toString("HH:mm"),
            "waktu_selesai": self.input_selesai.time().toString("HH:mm"),
            "kategori": self.combo_kategori.currentText(),
            "prioritas": self.combo_prioritas.currentText(),
            "deskripsi": self.input_deskripsi.toPlainText().strip(),
            "status": status,
        }

    def set_data(self, data):
        self.input_nama.setText(data.get("nama_aktivitas", ""))
        
        if data.get("status") == "Sudah":
            self.check_selesai.setChecked(True)
        else:
            self.check_selesai.setChecked(False)

        tgl = data.get("tanggal", "")
        if tgl:
            try:
                y, m, d = (int(x) for x in tgl.split("-"))
                self.input_tanggal.setDate(QDate(y, m, d))
            except (ValueError, IndexError):
                self.input_tanggal.setDate(QDate.currentDate())

        wm = data.get("waktu_mulai", "")
        if wm:
            try:
                h, m = (int(x) for x in wm.split(":"))
                self.input_mulai.setTime(QTime(h, m))
            except (ValueError, IndexError):
                pass

        ws = data.get("waktu_selesai", "")
        if ws:
            try:
                h, m = (int(x) for x in ws.split(":"))
                self.input_selesai.setTime(QTime(h, m))
            except (ValueError, IndexError):
                pass

        idx = self.combo_kategori.findText(data.get("kategori", ""))
        if idx >= 0:
            self.combo_kategori.setCurrentIndex(idx)

        idx = self.combo_prioritas.findText(data.get("prioritas", ""))
        if idx >= 0:
            self.combo_prioritas.setCurrentIndex(idx)

        self.input_deskripsi.setPlainText(data.get("deskripsi", ""))