import sqlite3
import os

from utils.constants import DB_NAME


class DatabaseManager:
    def __init__(self, db_path=None):
        if db_path is None:
            base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            db_dir = os.path.join(base_dir, "database")
            os.makedirs(db_dir, exist_ok=True)
            db_path = os.path.join(db_dir, DB_NAME)
            
        self.db_path = db_path
        self._init_db()

    def _get_connection(self):
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn

    def _init_db(self):
        conn = self._get_connection()
        try:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS aktivitas (
                    id              INTEGER PRIMARY KEY AUTOINCREMENT,
                    nama_aktivitas  TEXT    NOT NULL,
                    tanggal         TEXT    NOT NULL,
                    waktu_mulai     TEXT    NOT NULL,
                    waktu_selesai   TEXT    NOT NULL,
                    kategori        TEXT    NOT NULL,
                    prioritas       TEXT    NOT NULL,
                    deskripsi       TEXT    DEFAULT '',
                    status          TEXT    DEFAULT 'Belum',
                    created_at      TEXT    DEFAULT (datetime('now','localtime'))
                )
            """)
            try:
                conn.execute("ALTER TABLE aktivitas ADD COLUMN status TEXT DEFAULT 'Belum'")
            except Exception:
                pass
            conn.commit()
        finally:
            conn.close()

    def create(self, data):
        conn = self._get_connection()
        try:
            cursor = conn.execute("""
                INSERT INTO aktivitas 
                (nama_aktivitas, tanggal, waktu_mulai, waktu_selesai, kategori, prioritas, deskripsi, status)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                data["nama_aktivitas"], data["tanggal"], data["waktu_mulai"],
                data["waktu_selesai"], data["kategori"], data["prioritas"], 
                data["deskripsi"], data["status"]
            ))
            conn.commit()
            return cursor.lastrowid
        finally:
            conn.close()

    def read_all(self):
        conn = self._get_connection()
        try:
            rows = conn.execute("""
                SELECT * FROM aktivitas 
                ORDER BY tanggal ASC, waktu_mulai ASC
            """).fetchall()
            return [dict(r) for r in rows]
        finally:
            conn.close()

    def read_by_id(self, aktivitas_id):
        conn = self._get_connection()
        try:
            row = conn.execute(
                "SELECT * FROM aktivitas WHERE id = ?", (aktivitas_id,)
            ).fetchone()
            return dict(row) if row else None
        finally:
            conn.close()

    def update(self, aktivitas_id, data):
        conn = self._get_connection()
        try:
            conn.execute("""
                UPDATE aktivitas 
                SET nama_aktivitas=?, tanggal=?, waktu_mulai=?, 
                    waktu_selesai=?, kategori=?, prioritas=?, deskripsi=?, status=?
                WHERE id=?
            """, (
                data["nama_aktivitas"], data["tanggal"], data["waktu_mulai"],
                data["waktu_selesai"], data["kategori"], data["prioritas"],
                data["deskripsi"], data["status"], aktivitas_id
            ))
            conn.commit()
        finally:
            conn.close()

    def delete(self, aktivitas_id):
        conn = self._get_connection()
        try:
            conn.execute("DELETE FROM aktivitas WHERE id = ?", (aktivitas_id,))
            conn.commit()
        finally:
            conn.close()

    def search(self, keyword="", kategori="Semua", prioritas="Semua"):
        conn = self._get_connection()
        try:
            query = "SELECT * FROM aktivitas WHERE 1=1"
            params = []

            if keyword:
                query += " AND nama_aktivitas LIKE ?"
                params.append(f"%{keyword}%")
            if kategori != "Semua":
                query += " AND kategori = ?"
                params.append(kategori)
            if prioritas != "Semua":
                query += " AND prioritas = ?"
                params.append(prioritas)

            query += " ORDER BY tanggal ASC, waktu_mulai ASC"
            rows = conn.execute(query, params).fetchall()
            return [dict(r) for r in rows]
        finally:
            conn.close()