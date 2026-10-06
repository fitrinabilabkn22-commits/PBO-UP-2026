"""Pengujian untuk kelas Petugas."""

from src.model.Petugas import Petugas

def test_dua_objek_petugas_menyimpan_data_masing_masing() -> None:
    petugas_a = Petugas("PT-01", "Budi Santoso", "Operator", 120000)
    petugas_b = Petugas("PT-02", "Siti Aminah", "Admin", 100000)

    assert petugas_a.identitas() != petugas_b.identitas()
    assert petugas_a.honor_petugas(2) != petugas_b.honor_petugas(2)

def test_honor_petugas_tiga_hari() -> None:
    petugas = Petugas("PT-01", "Budi Santoso", "Operator", 120000)
    assert petugas.honor_petugas(3) == 360000

def test_parameter_berdefault() -> None:
    petugas = Petugas("PT-03", "Eko")
    assert petugas.identitas() == "[PT-03] Eko (Operator)"
    assert petugas.honor_petugas(1) == 100000