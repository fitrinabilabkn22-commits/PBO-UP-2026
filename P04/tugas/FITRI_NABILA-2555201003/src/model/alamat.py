"""Model domain: alamat penyewa, objek nilai yang tidak dapat diubah."""

from dataclasses import dataclass

@dataclass(frozen=True)
class Alamat:
    """Alamat tempat tinggal penyewa. Sekali dibuat, tidak dapat diubah."""
    dusun: str
    desa: str
    kecamatan: str

    def __post_init__(self) -> None:
        if not self.desa.strip():
            raise ValueError("nama desa tidak boleh kosong")
        if not self.kecamatan.strip():
            raise ValueError("nama kecamatan tidak boleh kosong")

    def lengkap(self) -> str:
        """Mengembalikan alamat lengkap dalam satu baris."""
        return f"Dusun {self.dusun}, Desa {self.desa}, Kec. {self.kecamatan}"

    def singkat(self) -> str:
        """Mengembalikan desa dan kecamatan saja, untuk nota sewa."""
        return f"{self.desa}, {self.kecamatan}"