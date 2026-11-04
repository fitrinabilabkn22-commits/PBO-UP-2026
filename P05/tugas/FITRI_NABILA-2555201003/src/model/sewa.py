from src.model.baris_sewa import BarisSewa
from src.model.alat_tani import AlatTani
from src.model.penyewa import Penyewa


class Sewa:
    """Satu transaksi penyewaan: seorang penyewa dan alat yang disewanya."""

    BATAS_ALAT_PER_SEWA: int = 10

    def __init__(self, nomor: str, penyewa: Penyewa) -> None:
        if not nomor.strip():
            raise ValueError("nomor sewa tidak boleh kosong")
        self._nomor = nomor
        self._penyewa = penyewa # asosiasi
        self._baris: list[BarisSewa] = [] # komposisi
        
    @property    
    def baris(self) -> tuple[BarisSewa, ...]:
        """Dikembalikan sebagai tuple agar tidak dapat diubah dari luar."""
        return tuple(self._baris)
    
    def tambah_alat(self, alat: AlatTani, jumlah_hari: int) -> None:
        if len(self._baris) >= Sewa.BATAS_ALAT_PER_SEWA:
            raise ValueError("Jumlah alat yang disewa telah mencapai batas maksimum")
        for baris in self._baris:
            if baris.kode_alat == alat.kode:
                raise ValueError(f"alat {alat.kode} sudah ada dalam transaksi ini")
        self._baris.append(BarisSewa(alat, jumlah_hari)) # ← dibuat di sini

    def total(self) -> int:
        """Menjumlahkan seluruh subtotal baris."""
        return sum(baris.subtotal() for baris in self._baris)
    
    def nota(self) -> str:
        """Menyusun nota lengkap transaksi ini."""
        judul = f"NOTA SEWA {self._nomor}"
        kepada = self._penyewa.identitas()
        garis = "-" * 68
        isi = "\n".join(baris.baris_nota() for baris in self._baris)
        total = AlatTani.format_rupiah(self.total())
        return (f"{judul}\n{kepada}\n{garis}\n{isi}\n{garis}\n"
        f"{'TOTAL':<47}{total:>21}")

    def jumlah_alat(self) -> int:
        return len(self._baris)