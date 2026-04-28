from datetime import datetime


def validate_aktivitas(data):
    field_labels = {
        "nama_aktivitas": "Nama Aktivitas",
        "tanggal":        "Tanggal",
        "waktu_mulai":    "Waktu Mulai",
        "waktu_selesai":  "Waktu Selesai",
        "kategori":       "Kategori",
        "prioritas":      "Prioritas",
    }

    for field, label in field_labels.items():
        if not data.get(field, "").strip():
            return False, f"Field '{label}' wajib diisi!"

    try:
        datetime.strptime(data["tanggal"], "%Y-%m-%d")
    except ValueError:
        return False, "Format tanggal tidak valid!"

    try:
        t_mulai = datetime.strptime(data["waktu_mulai"], "%H:%M")
        t_selesai = datetime.strptime(data["waktu_selesai"], "%H:%M")
    except ValueError:
        return False, "Format waktu tidak valid!"

    if t_selesai <= t_mulai:
        return False, "Waktu selesai harus setelah waktu mulai!"

    return True, ""


def format_tanggal(tanggal_str):
    if not tanggal_str:
        return ""
        
    bulan_id = {
        1: "Januari", 2: "Februari", 3: "Maret", 4: "April",
        5: "Mei", 6: "Juni", 7: "Juli", 8: "Agustus",
        9: "September", 10: "Oktober", 11: "November", 12: "Desember",
    }
    
    try:
        dt = datetime.strptime(tanggal_str, "%Y-%m-%d")
        return f"{dt.day:02d} {bulan_id[dt.month]} {dt.year}"
    except ValueError:
        return tanggal_str