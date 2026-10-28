"""Pengujian untuk kelas Petugas dan objek nilai NomorPegawai."""

from dataclasses import FrozenInstanceError

import pytest

from src.model.petugas import NomorPegawai, Petugas


def buat_petugas() -> Petugas:
    return Petugas("Fitri Nabila", "085375362713", "Admin", 100000)


def test_tambah_petugas() -> None:
    petugas = buat_petugas()
    assert petugas.nama_petugas == "Fitri Nabila"
    assert petugas.telepon == "085375362713"
    assert petugas.gaji_harian == 100000
    assert petugas.nomor_pegawai.nomor == "PGW001"


def test_hitung_gaji_petugas() -> None:
    assert buat_petugas().gaji_petugas(5) == 500000


def test_tampilkan_identitas_petugas() -> None:
    petugas = buat_petugas()
    assert petugas.tampilkan_identitas() == (
        "Fitri Nabila (Admin) nomor telepon: 085375362713, "
        "gaji harian: Rp100.000"
    )


def test_hubungi_petugas() -> None:
    assert buat_petugas().hubungi_petugas() == "Fitri Nabila - 085375362713"


def test_nama_petugas_tidak_memiliki_setter() -> None:
    petugas = buat_petugas()
    with pytest.raises(AttributeError):
        petugas.nama_petugas = "Nama Baru"  # type: ignore[misc]


def test_nomor_pegawai_beku_tidak_dapat_diubah() -> None:
    nomor = NomorPegawai("PGW001")
    with pytest.raises(FrozenInstanceError):
        nomor.nomor = "PGW002"  # type: ignore[misc]


def test_nomor_pegawai_kosong_ditolak() -> None:
    with pytest.raises(ValueError):
        NomorPegawai("")


def test_nomor_pegawai_dengan_simbol_ditolak() -> None:
    with pytest.raises(ValueError):
        NomorPegawai("PGW-001")


def test_telepon_tidak_valid_ditolak() -> None:
    petugas = buat_petugas()
    with pytest.raises(ValueError):
        petugas.telepon = "12345"
    assert petugas.telepon == "085375362713"


def test_gaji_nol_ditolak() -> None:
    petugas = buat_petugas()
    with pytest.raises(ValueError):
        petugas.gaji_harian = 0
    assert petugas.gaji_harian == 100000


def test_gaji_di_atas_batas_ditolak() -> None:
    with pytest.raises(ValueError):
        Petugas("Fitri Nabila", "085375362713", "Admin", 5_000_001)


def test_jumlah_hari_tidak_valid_ditolak() -> None:
    petugas = buat_petugas()
    with pytest.raises(ValueError):
        petugas.gaji_petugas(0)
