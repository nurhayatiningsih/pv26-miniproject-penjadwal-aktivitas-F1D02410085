import sys
import os

from PySide6.QtWidgets import QApplication
from PySide6.QtCore import QFile, QTextStream

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from views.main_window import MainWindow
from controllers.aktivitas_controller import AktivitasController


def load_stylesheet(app):
    qss_path = os.path.join(os.path.dirname(__file__), "styles", "style.qss")
    qss_file = QFile(qss_path)
    
    if qss_file.open(QFile.ReadOnly | QFile.Text):
        stream = QTextStream(qss_file)
        app.setStyleSheet(stream.readAll())
        qss_file.close()
        
    return True


def main():
    app = QApplication(sys.argv)
    app.setApplicationName("AuraPlan")
    
    load_stylesheet(app)
    
    view = MainWindow()
    AktivitasController(view)
    view.show()
    
    sys.exit(app.exec())


if __name__ == "__main__":
    main()