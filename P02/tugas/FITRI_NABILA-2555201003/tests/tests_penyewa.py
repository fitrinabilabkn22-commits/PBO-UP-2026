"""Pengujian untuk kelas AlatTani."""

from src.model.penyewa import Penyewa

def test_penyewa_identitas() -> None:
    penyewa = Penyewa("1406012509900001", "Budi Santoso", "Kuok", "0895-1243-5987")
    assert penyewa.identitas() == "Budi Santoso (1406012509900001) - Desa Kuok"

def test_pemyewa_kontak_ada_telepon() -> None:
    penyewa = Penyewa("1406012509900001", "Budi Santoso", "Kuok", "0895-1243-5987")
    assert penyewa.kontak() == "Budi Santoso (1406012509900001) - Desa Kuok"

def test_penyewa_kontak_tanpa_telepon() -> None:
    penyewa = Penyewa("1406012509900002", "Nuratna Fitri Hasanah", "Salo")
    assert penyewa.kontak() == "Nuratna Fitri Hasanah belum mencantumkan nomor telepon "
    