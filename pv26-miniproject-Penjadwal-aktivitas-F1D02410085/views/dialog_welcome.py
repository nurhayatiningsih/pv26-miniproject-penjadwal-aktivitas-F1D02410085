from PySide6.QtWidgets import QDialog, QVBoxLayout, QLabel, QPushButton, QFrame
from PySide6.QtCore import Qt
from PySide6.QtGui import QMouseEvent


class DialogWelcome(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.Dialog)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self._drag_pos = None
        self._build_ui()

    def _build_ui(self):
        self.setFixedSize(400, 300)
        lay = QVBoxLayout(self)

        frame = QFrame()
        frame.setObjectName("welcomeFrame")
        frame_lay = QVBoxLayout(frame)
        frame_lay.setContentsMargins(30, 40, 30, 30)

        lbl_title = QLabel("✨ AuraPlan ✨")
        lbl_title.setObjectName("welcomeTitle")
        lbl_title.setAlignment(Qt.AlignCenter)

        lbl_sub = QLabel("AuraPlan - Penjadwal Harian\nKelola waktumu dengan lebih baik!")
        lbl_sub.setObjectName("welcomeSub")
        lbl_sub.setAlignment(Qt.AlignCenter)
        lbl_sub.setWordWrap(True)

        self.btn_masuk = QPushButton("Masuk ke Aplikasi")
        self.btn_masuk.setObjectName("btnMasuk")
        self.btn_masuk.setCursor(Qt.PointingHandCursor)

        lbl_hint = QLabel("💡 Geser layar ini untuk bergerak")
        lbl_hint.setObjectName("welcomeHint")
        lbl_hint.setAlignment(Qt.AlignCenter)

        frame_lay.addWidget(lbl_title)
        frame_lay.addWidget(lbl_sub)
        frame_lay.addStretch()
        frame_lay.addWidget(self.btn_masuk)
        frame_lay.addWidget(lbl_hint)
        lay.addWidget(frame)

        self.btn_masuk.clicked.connect(self.accept)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self._drag_pos = event.globalPosition().toPoint() - self.frameGeometry().topLeft()
            event.accept()

    def mouseMoveEvent(self, event):
        if event.buttons() == Qt.LeftButton and self._drag_pos:
            self.move(event.globalPosition().toPoint() - self._drag_pos)
            event.accept()

    def mouseReleaseEvent(self, event):
        self._drag_pos = None
        event.accept()