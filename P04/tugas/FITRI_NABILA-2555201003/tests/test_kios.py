"""Pengujian untuk kelas Kios."""

import pytest

from src.model.kios import Kios


def test_produk_bisa_dibuat() -> None:
    produk = Kios("BR-01", "Beras", 100_000, 110_000, 10)
    assert produk.kode == "BR-01"
    assert produk.nama == "Beras"
    assert produk.stok == 10


def test_nama_dan_kode_dibersihkan() -> None:
    produk = Kios(" BR-01 ", " Beras ", 100_000, 110_000, 5)
    assert produk.kode == "BR-01"
    assert produk.nama == "Beras"


def test_harga_jual_wajar() -> None:
    assert Kios.harga_jual_wajar(100_000, 110_000) is True


def test_harga_jual_tidak_wajar() -> None:
    assert Kios.harga_jual_wajar(100_000, 109_000) is False


def test_harga_modal_nol_ditolak() -> None:
    with pytest.raises(ValueError):
        Kios("BR-01", "Beras", 0, 110_000, 5)


def test_harga_jual_di_bawah_margin_ditolak() -> None:
    with pytest.raises(ValueError):
        Kios("BR-01", "Beras", 100_000, 105_000, 5)


def test_stok_minus_ditolak() -> None:
    with pytest.raises(ValueError):
        Kios("BR-01", "Beras", 100_000, 110_000, -1)


def test_kode_kosong_ditolak() -> None:
    with pytest.raises(ValueError):
        Kios("   ", "Beras", 100_000, 110_000, 5)


def test_nama_kosong_ditolak() -> None:
    with pytest.raises(ValueError):
        Kios("BR-01", "   ", 100_000, 110_000, 5)


def test_tambah_stok() -> None:
    produk = Kios("BR-01", "Beras", 100_000, 110_000, 5)
    produk.tambah_stok(3)
    assert produk.stok == 8


def test_tambah_stok_nol_ditolak() -> None:
    produk = Kios("BR-01", "Beras", 100_000, 110_000, 5)
    with pytest.raises(ValueError):
        produk.tambah_stok(0)


def test_konstruktor_dari_baris_csv() -> None:
    produk = Kios.dari_baris_csv("BR-01;Beras;100000;110000;8")
    assert produk.kode == "BR-01"
    assert produk.harga_jual == 110_000
    assert produk.stok == 8


def test_csv_dengan_bagian_kurang_ditolak() -> None:
    with pytest.raises(ValueError):
        Kios.dari_baris_csv("BR-01;Beras;100000;110000")


def test_csv_harga_bukan_angka_ditolak() -> None:
    with pytest.raises(ValueError):
        Kios.dari_baris_csv("BR-01;Beras;seratus;110000;8")


def test_nilai_persediaan() -> None:
    produk = Kios("BR-01", "Beras", 100_000, 110_000, 8)
    assert produk.nilai_persediaan() == 800_000


def test_format_rupiah() -> None:
    assert Kios.format_rupiah(1_250_000) == "Rp1.250.000"


def test_keterangan_produk() -> None:
    produk = Kios("BR-01", "Beras", 100_000, 110_000, 8)
    assert "[BR-01] Beras" in produk.keterangan()


def test_pencacah_naik_dengan_selisih() -> None:
    awal = Kios.jumlah_terdaftar()
    Kios("BR-90", "Produk Uji 1", 10_000, 11_000, 1)
    Kios("BR-91", "Produk Uji 2", 10_000, 11_000, 1)
    assert Kios.jumlah_terdaftar() == awal + 2
