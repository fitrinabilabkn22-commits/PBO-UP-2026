"""Pengujian untuk kelas Penyewa dan Alamat."""

import dataclasses
import pytest
from src.model.alamat import Alamat
from src.model.penyewa import Penyewa


def test_penyewa_identitas() -> None:
    alamat = Alamat("Salo Timur", "Salo", "Salo")
    penyewa = Penyewa("1406012509900001", "Fitri Nabila", alamat, "0853-7536-2713")
    assert penyewa.identitas() == "Fitri Nabila (1406012509900001) — Salo, Salo"


def test_penyewa_kontak_ada_telepon() -> None:
    alamat = Alamat("Salo Timur", "Salo", "Salo")
    penyewa = Penyewa("1406012509900001", "Fitri Nabila", alamat, "0853-7536-2713")
    assert penyewa.kontak() == "Fitri Nabila dapat dihubungi di 0853-7536-2713"


def test_penyewa_kontak_tanpa_telepon() -> None:
    alamat = Alamat("Salo Timur", "Salo", "Salo")
    penyewa = Penyewa("1406014403950002", "Putri Nabila", alamat)
    assert penyewa.kontak() == "Putri Nabila belum mencantumkan nomor telepon"


def test_nik_kurang_dari_16_digit_ditolak() -> None:
    alamat = Alamat("Salo Timur", "Salo", "Salo")
    with pytest.raises(ValueError):
        Penyewa("12345", "Fitri Nabila", alamat)


def test_nik_mengandung_huruf_ditolak() -> None:
    alamat = Alamat("Salo Timur", "Salo", "Salo")
    with pytest.raises(ValueError):
        Penyewa("140601250990000A", "Fitri Nabila", alamat)


def test_nik_tidak_punya_setter() -> None:
    alamat = Alamat("Salo Timur", "Salo", "Salo")
    penyewa = Penyewa("1406012509900001", "Fitri Nabila", alamat)
    with pytest.raises(AttributeError):
        penyewa.nik = "1406012509900002"  # type: ignore[misc]


def test_telepon_tidak_sah_ditolak() -> None:
    alamat = Alamat("Salo Timur", "Salo", "Salo")
    penyewa = Penyewa("1406012509900001", "Fitri Nabila", alamat)
    with pytest.raises(ValueError):
        penyewa.telepon = "123"


def test_alamat_desa_kosong_ditolak() -> None:
    with pytest.raises(ValueError):
        Alamat("Salo Timur", "  ", "Kuok")


def test_alamat_kecamatan_kosong_ditolak() -> None:
    with pytest.raises(ValueError):
        Alamat("Salo Timur", "Salo", "  ")


def test_alamat_tidak_dapat_diubah() -> None:
    alamat = Alamat("Salo Timur", "Salo", "Salo")
    with pytest.raises(dataclasses.FrozenInstanceError):
        alamat.desa = "Salo"  # type: ignore[misc]