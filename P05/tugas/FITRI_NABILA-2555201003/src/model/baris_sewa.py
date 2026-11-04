from src.model.alat_tani import AlatTani

class BarisSewa:
    """Satu alat dalam satu transaksi, beserta salinan keterangan saat itu."""
    def __init__(self, alat: AlatTani, jumlah_hari: int) -> None:
        if jumlah_hari <= 0:
            raise ValueError(
            f"jumlah hari harus lebih dari nol, diterima {jumlah_hari}")
        self._alat = alat # rujukan — agregasi
        self._jumlah_hari = jumlah_hari
        self._kode_alat = alat.kode # salinan
        self._nama_alat = alat.nama # salinan
        self._tarif_saat_sewa = alat.tarif_harian # salinan

    def subtotal(self) -> int:
        """Menghitung biaya baris ini berdasarkan tarif yang disalin."""
        return self._tarif_saat_sewa * self._jumlah_hari

    @property
    def kode_alat(self) -> str:
        return self._kode_alat

    @property
    def tarif_saat_sewa(self) -> int:
        return self._tarif_saat_sewa

    def baris_nota(self) -> str:
        return f"{self._nama_alat} {self._jumlah_hari} hr x Rp{self._tarif_saat_sewa}"