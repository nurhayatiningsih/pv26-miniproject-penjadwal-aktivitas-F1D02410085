from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, 
    QFormLayout, QLineEdit, QPushButton
)


class DialogFindReplace(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Cari & Ganti Deskripsi")
        self.setFixedSize(400, 180)
        self.setModal(True)
        self._build_ui()

    def _build_ui(self):
        lay = QVBoxLayout(self)
        form = QFormLayout()
        form.setSpacing(12)

        self.input_cari = QLineEdit()
        self.input_cari.setPlaceholderText("Kata yang dicari di deskripsi...")
        form.addRow("Cari:", self.input_cari)

        self.input_ganti = QLineEdit()
        self.input_ganti.setPlaceholderText("Diganti dengan...")
        form.addRow("Ganti:", self.input_ganti)

        lay.addLayout(form)
        lay.addStretch()

        btn_lay = QHBoxLayout()
        btn_lay.addStretch()

        self.btn_ganti = QPushButton("Ganti Semua")
        self.btn_ganti.setObjectName("btnSimpan")
        self.btn_ganti.setCursor(Qt.PointingHandCursor)
        self.btn_ganti.clicked.connect(self.accept)

        self.btn_batal = QPushButton("Batal")
        self.btn_batal.setObjectName("btnBatal")
        self.btn_batal.setCursor(Qt.PointingHandCursor)
        self.btn_batal.clicked.connect(self.reject)

        btn_lay.addWidget(self.btn_ganti)
        btn_lay.addWidget(self.btn_batal)
        lay.addLayout(btn_lay)

    def get_data(self):
        return self.input_cari.text().strip(), self.input_ganti.text().strip()