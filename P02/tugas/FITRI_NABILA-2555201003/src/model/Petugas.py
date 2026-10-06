"""Model domain: petugas UPJA yang melayani penyewaan."""


class Petugas:
    """"Petugas UPJA beserta tarif operasionalnya."""

    def __init__(self, id_petugas: str, nama: str, jabatan: str = "Operator", tarif_harian: int = 100000) -> None:
        self._id_petugas = id_petugas
        self._nama = nama
        self._jabatan = jabatan
        self._tarif_harian = tarif_harian

    def honor_petugas(self, jumlah_hari: int) -> int:
        """"Menghitung total honor petugas berdasarkan jumlah hari kerja."""
        return self._tarif_harian * jumlah_hari

    def identitas(self) -> str:
        """Mengembalikan baris identitas singkat petugas."""
        return f"[{self._id_petugas}] {self._nama} ({self._jabatan})"