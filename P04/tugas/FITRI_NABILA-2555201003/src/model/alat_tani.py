from typing import Final

"""Model domain: alat yang disewakan UPJA."""

class AlatTani:
    """Satu unit alat pertanian beserta tarif hariannya."""

    # --- Aturan usaha UPJA: berlaku sama bagi seluruh alat ---
    TARIF_MINIMUM: Final[int] = 10_000
    TARIF_MAKSIMUM: Final[int] = 5_000_000
    PERSEN_DENDA_HARIAN: Final[int] = 10
    PEMISAH_BARIS: Final[str] = ";"
    
    # --- Milik kelas, bukan milik objek: dibagi seluruh alat ---
    _jumlah_terdaftar: int = 0

    def __init__(self, kode: str, nama: str, tarif_harian: int) -> None:
        if not kode.strip():
            raise ValueError("kode alat tidak boleh kosong")
        self._kode = kode
        self._nama = nama
        self._tarif_harian = 0
        self.tarif_harian = tarif_harian
        AlatTani._jumlah_terdaftar += 1 # ← Pencacah dinaikkan di sini

    def biaya_sewa(self, jumlah_hari: int) -> int:
        """Menghitung biaya sewa untuk sejumlah hari tertentu."""
        return self._tarif_harian * jumlah_hari

    def keterangan(self) -> str:
        """Mengembalikan baris keterangan alat untuk daftar sewa."""
        rupiah = f"{self._tarif_harian:,}".replace(",", ".")
        return f"[{self._kode}] {self._nama} — Rp{rupiah}/hari"

    @staticmethod
    def tarif_wajar(nilai: int) -> bool:
        """Memeriksa kewajaran tarif tanpa perlu membuat alat lebih dulu."""
        return AlatTani.TARIF_MINIMUM <= nilai <= AlatTani.TARIF_MAKSIMUM
    
    @staticmethod
    def format_rupiah(nilai: int) -> str:
        """Mengubah angka menjadi tulisan rupiah bergaya Indonesia."""
        return "Rp" + f"{nilai:,}".replace(",", ".")

    @property
    def kode(self) -> str:
        """Kode alat. Tidak dapat diubah setelah alat dibuat."""
        return self._kode

    @property
    def nama(self) -> str:
        """Nama alat. Tidak dapat diubah setelah alat dibuat."""
        return self._nama

    @property
    def tarif_harian(self) -> int:
        """Tarif sewa per hari dalam rupiah."""
        return self._tarif_harian

    @tarif_harian.setter
    def tarif_harian(self, nilai: int) -> None:
        if not AlatTani.tarif_wajar(nilai):
            raise ValueError(
                f"tarif harus antara "
                f"{AlatTani.format_rupiah(AlatTani.TARIF_MINIMUM)} dan "
                f"{AlatTani.format_rupiah(AlatTani.TARIF_MAKSIMUM)}, "
                f"diterima {nilai}"
            )
        self._tarif_harian = nilai

    @classmethod
    def jumlah_terdaftar(cls) -> int:
        """Banyaknya alat yang sudah pernah dibuat."""
        return cls._jumlah_terdaftar

    @classmethod
    def dari_baris_csv(cls, baris: str) -> "AlatTani":
        """Membuat alat dari satu baris pendataan."""
        bagian = baris.strip().split(cls.PEMISAH_BARIS)
        if len(bagian) != 3:
            raise ValueError(
                f"baris harus berisi 3 bagian, diterima {len(bagian)}: '{baris}'"
            )
        kode, nama, tarif = bagian
        if not tarif.strip().isdigit():
            raise ValueError(f"tarif harus berupa angka, diterima '{tarif}'")
        return cls(kode.strip(), nama.strip(), int(tarif))

    def denda_keterlambatan(self, hari_terlambat: int) -> int:
        """Menghitung denda keterlambatan pengembalian alat."""
        if hari_terlambat < 0:
            raise ValueError(
                f"hari terlambat tidak boleh minus, diterima {hari_terlambat}"
            )
        per_hari = self._tarif_harian * AlatTani.PERSEN_DENDA_HARIAN // 100
        return per_hari * hari_terlambat