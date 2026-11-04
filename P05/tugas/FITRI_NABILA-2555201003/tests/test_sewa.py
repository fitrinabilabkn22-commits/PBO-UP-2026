import pytest
from src.model.penyewa import Penyewa
from src.model.sewa import Sewa
from src.model.baris_sewa import BarisSewa
from src.model.alat_tani import AlatTani

def buat_penyewa() -> Penyewa:
    from src.model.penyewa import Penyewa
    from src.model.alamat import Alamat
    alamat_budi = Alamat("Salo Timur", "Salo", "Salo")
    return Penyewa("1406012509900001", "Budi Santoso", alamat_budi)

def test_salinan_tidak_ikut_berubah_saat_tarif_alat_naik() -> None:
    alat = AlatTani("TR-01", "Traktor", 150_000)
    baris = BarisSewa(alat, 3)
    alat.tarif_harian = 175_000
    assert baris.tarif_saat_sewa == 150_000
    assert baris.subtotal() == 450_000

def test_komposisi_tidak_dapat_dibongkar_dari_luar() -> None:
    sewa = Sewa("SW-001", buat_penyewa())
    sewa.tambah_alat(AlatTani("TR-01", "Traktor", 150_000), 3)
    with pytest.raises(AttributeError):
        sewa.baris.append(None) # type: ignore[attr-defined]
    assert sewa.jumlah_alat() == 1

def test_penyewa_tetap_hidup_setelah_sewa_dihapus() -> None:
    budi = buat_penyewa()
    sewa = Sewa("SW-001", budi)
    del sewa
    assert budi._nama == "Budi Santoso"