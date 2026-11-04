"""Model domain: petani yang menyewa alat dari UPJA."""

from src.model.alamat import Alamat

class Penyewa:
    """Identitas seorang petani yang menyewa alat dari UPJA."""

    def __init__(self, nik: str, nama: str, alamat: Alamat, telepon: str = "-") -> None:
        if len(nik) != 16 or not nik.isdigit():
            raise ValueError(f"NIK harus 16 digit angka, diterima '{nik}'")
        self._nik = nik
        self._nama = nama
        self._alamat = alamat
        self.telepon = telepon

    @property
    def nik(self) -> str:
        """NIK penyewa. Melekat seumur hidup, tidak dapat diubah."""
        return self._nik

    @property
    def alamat(self) -> Alamat:
        """Alamat penyewa. Objeknya sendiri tidak dapat diubah isinya."""
        return self._alamat

    @property
    def telepon(self) -> str:
        """Nomor telepon penyewa."""
        return self._telepon

    @telepon.setter
    def telepon(self, nilai: str) -> None:
        bersih = nilai.replace("-", "").replace(" ", "")
        if bersih == "" or bersih == "-":
            self._telepon = "-"
            return
        if not bersih.isdigit() or len(bersih) < 10:
            raise ValueError(f"nomor telepon tidak sah, diterima '{nilai}'")
        self._telepon = nilai

    def identitas(self) -> str:
        return f"{self._nama} ({self._nik}) — {self._alamat.singkat()}"

    def kontak(self) -> str:
        """Mengembalikan keterangan cara menghubungi penyewa."""
        if self._telepon == "-":
            return f"{self._nama} belum mencantumkan nomor telepon"
        return f"{self._nama} dapat dihubungi di {self._telepon}"