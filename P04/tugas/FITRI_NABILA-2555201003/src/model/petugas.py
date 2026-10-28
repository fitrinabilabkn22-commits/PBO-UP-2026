"""Model domain: petugas UPJA yang bertugas melayani penyewaan."""

from dataclasses import dataclass


@dataclass(frozen=True)
class NomorPegawai:
    """Objek nilai nomor pegawai yang tidak dapat diubah setelah dibuat."""

    nomor: str

    def __post_init__(self) -> None:
        if not self.nomor.strip():
            raise ValueError("nomor pegawai tidak boleh kosong")
        if not self.nomor.isalnum():
            raise ValueError("nomor pegawai hanya boleh berisi huruf dan angka")


class Petugas:
    """Identitas petugas UPJA beserta gaji operasionalnya."""

    def __init__(
        self,
        nama_petugas: str,
        no_telepon: str,
        jabatan: str = "Admin",
        gaji_harian: int = 50000,
        nomor_pegawai: str = "PGW001",
    ) -> None:
        if not nama_petugas.strip():
            raise ValueError("nama petugas tidak boleh kosong")

        self._nama_petugas = nama_petugas
        self._nomor_pegawai = NomorPegawai(nomor_pegawai)
        self._no_telepon = "-"
        self._gaji_harian = 0
        self._jabatan = jabatan
        self.telepon = no_telepon
        self.gaji_harian = gaji_harian

    # Baca-saja: nama merupakan identitas petugas dan tidak diubah melalui property.
    @property
    def nama_petugas(self) -> str:
        """Nama petugas yang tidak dapat diubah melalui property."""
        return self._nama_petugas

    # Baca-saja: nomor pegawai adalah objek nilai beku sebagai identitas tetap.
    @property
    def nomor_pegawai(self) -> NomorPegawai:
        """Nomor pegawai yang dibungkus dalam objek nilai beku."""
        return self._nomor_pegawai

    # Baca-tulis terjaga: nomor telepon dapat berubah, tetapi harus valid.
    @property
    def telepon(self) -> str:
        """Nomor telepon petugas."""
        return self._no_telepon

    @telepon.setter
    def telepon(self, nilai: str) -> None:
        bersih = nilai.replace("-", "").replace(" ", "")
        if nilai == "-":
            self._no_telepon = "-"
            return
        if not bersih.isdigit() or len(bersih) < 10 or len(bersih) > 15:
            raise ValueError("nomor telepon harus terdiri dari 10 sampai 15 digit")
        self._no_telepon = nilai

    # Baca-tulis terjaga: gaji dapat disesuaikan, tetapi harus dalam rentang wajar.
    @property
    def gaji_harian(self) -> int:
        """Gaji petugas per hari dalam rupiah."""
        return self._gaji_harian

    @gaji_harian.setter
    def gaji_harian(self, nilai: int) -> None:
        if isinstance(nilai, bool) or not isinstance(nilai, int):
            raise ValueError("gaji harian harus berupa bilangan bulat")
        if nilai <= 0:
            raise ValueError("gaji harian harus lebih dari nol")
        if nilai > 5_000_000:
            raise ValueError("gaji harian tidak wajar")
        self._gaji_harian = nilai

    def gaji_petugas(self, jumlah_hari: int) -> int:
        if isinstance(jumlah_hari, bool) or not isinstance(jumlah_hari, int):
            raise ValueError("jumlah hari harus berupa bilangan bulat")
        if jumlah_hari <= 0:
            raise ValueError("jumlah hari harus lebih dari nol")
        return self._gaji_harian * jumlah_hari

    def tampilkan_identitas(self) -> str:
        format_gaji = "Rp{:,}".format(self._gaji_harian).replace(",", ".")
        return (
            f"{self._nama_petugas} ({self._jabatan}) nomor telepon: "
            f"{self._no_telepon}, gaji harian: {format_gaji}"
        )

    def hubungi_petugas(self) -> str:
        return f"{self._nama_petugas} - {self._no_telepon}"
