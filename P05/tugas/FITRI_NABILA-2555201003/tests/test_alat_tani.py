"""Pengujian untuk kelas AlatTani."""

import pytest
from src.model.alat_tani import AlatTani


def test_biaya_sewa_tiga_hari() -> None:
    alat = AlatTani("TR-01", "Traktor Roda Empat", 200000)
    assert alat.biaya_sewa(3) == 600000


def test_dua_objek_punya_data_sendiri() -> None:
    a = AlatTani("TR-01", "Traktor", 200000)
    b = AlatTani("PA-01", "Pompa", 80000)
    assert a.biaya_sewa(1) != b.biaya_sewa(1)


def test_keterangan_format_rupiah() -> None:
    alat = AlatTani("TR-01", "Traktor Roda Empat", 200000)
    assert alat.keterangan() == "[TR-01] Traktor Roda Empat — Rp200.000/hari"


def test_biaya_sewa_nol_hari() -> None:
    alat = AlatTani("PA-01", "Pompa Air", 80000)
    assert alat.biaya_sewa(0) == 0


def test_tarif_minus_ditolak_sejak_konstruktor() -> None:
    with pytest.raises(ValueError):
        AlatTani("TR-01", "Traktor", -5000)


def test_tarif_nol_ditolak_sejak_konstruktor() -> None:
    with pytest.raises(ValueError):
        AlatTani("TR-01", "Traktor", 0)


def test_tarif_minus_ditolak_lewat_setter() -> None:
    alat = AlatTani("TR-01", "Traktor", 200000)
    with pytest.raises(ValueError):
        alat.tarif_harian = -5000
    assert alat.tarif_harian == 200000


def test_tarif_tidak_wajar_ditolak() -> None:
    alat = AlatTani("TR-01", "Traktor", 200000)
    with pytest.raises(ValueError):
        alat.tarif_harian = 6_000_000


def test_kode_tidak_punya_setter() -> None:
    alat = AlatTani("TR-01", "Traktor", 200000)
    with pytest.raises(AttributeError):
        alat.kode = "TR-99"  # type: ignore[misc]


def test_nama_tidak_punya_setter() -> None:
    alat = AlatTani("TR-01", "Traktor", 200000)
    with pytest.raises(AttributeError):
        alat.nama = "Traktor Baru"  # type: ignore[misc]


def test_kode_kosong_ditolak() -> None:
    with pytest.raises(ValueError):
        AlatTani("   ", "Traktor", 200000)

def test_tarif_wajar_dipanggil_tanpa_objek() -> None:
    assert AlatTani.tarif_wajar(150_000) is True
    assert AlatTani.tarif_wajar(6_000_000) is False


def test_pencacah_naik_untuk_setiap_alat_baru() -> None:
    awal = AlatTani.jumlah_terdaftar()

    AlatTani("TR-90", "Traktor Uji", 100_000)
    AlatTani("TR-91", "Traktor Uji", 100_000)

    assert AlatTani.jumlah_terdaftar() == awal + 2


def test_konstruktor_dari_baris_csv() -> None:
    alat = AlatTani.dari_baris_csv("PA-01;Pompa Air;75000")

    assert alat.kode == "PA-01"
    assert alat.tarif_harian == 75_000


def test_baris_csv_tarif_bukan_angka_ditolak() -> None:
    with pytest.raises(ValueError):
        AlatTani.dari_baris_csv("PA-01;Pompa Air;tujuh puluh lima ribu")