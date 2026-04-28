from PySide6.QtWidgets import QDialog, QVBoxLayout, QLabel, QPushButton
from PySide6.QtCore import Qt


class DialogAbout(QDialog):
    def __init__(self, app_name, app_version, app_description, student_name, student_nim, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Tentang Aplikasi")
        self.setFixedSize(420, 300)
        self.setModal(True)
        self._build_ui(app_name, app_version, app_description, student_name, student_nim)

    def _build_ui(self, app_name, app_version, app_description, student_name, student_nim):
        lay = QVBoxLayout(self)
        lay.setSpacing(10)
        lay.setContentsMargins(30, 25, 30, 25)

        lbl_nama = QLabel(app_name)
        lbl_nama.setObjectName("labelAboutTitle")
        lbl_nama.setAlignment(Qt.AlignCenter)
        lay.addWidget(lbl_nama)

        lbl_ver = QLabel(f"Versi {app_version}")
        lbl_ver.setObjectName("labelAboutVersion")
        lbl_ver.setAlignment(Qt.AlignCenter)
        lay.addWidget(lbl_ver)

        sep = QLabel("─" * 42)
        sep.setObjectName("labelSeparator")
        sep.setAlignment(Qt.AlignCenter)
        lay.addWidget(sep)

        lbl_desc = QLabel(app_description)
        lbl_desc.setWordWrap(True)
        lbl_desc.setAlignment(Qt.AlignCenter)
        lay.addWidget(lbl_desc)

        lbl_mhs = QLabel(f"<b>Dibuat oleh:</b><br>{student_name}<br>NIM: {student_nim}")
        lbl_mhs.setObjectName("labelAboutStudent")
        lbl_mhs.setAlignment(Qt.AlignCenter)
        lay.addWidget(lbl_mhs)

        lay.addStretch()

        btn = QPushButton("Tutup")
        btn.setObjectName("btnTutup")
        btn.setCursor(Qt.PointingHandCursor)
        btn.clicked.connect(self.accept)
        lay.addWidget(btn, alignment=Qt.AlignCenter)