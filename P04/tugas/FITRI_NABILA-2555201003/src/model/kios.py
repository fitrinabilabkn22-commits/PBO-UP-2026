"""Model produk untuk kios hasil pertanian."""

from typing import Final


class Kios:
    """Mewakili satu produk yang dijual oleh kios."""

    PEMISAH_BARIS: Final[str] = ";"
    MARGIN_MINIMUM: Final[int] = 10
    STOK_MINIMUM: Final[int] = 0

    _jumlah_terdaftar: int = 0

    def __init__(
        self,
        kode: str,
        nama: str,
        harga_modal: int,
        harga_jual: int,
        stok: int,
    ) -> None:
        kode_bersih = kode.strip()
        nama_bersih = nama.strip()

        if not kode_bersih:
            raise ValueError("Kode produk tidak boleh kosong.")
        if not nama_bersih:
            raise ValueError("Nama produk tidak boleh kosong.")
        if harga_modal <= 0:
            raise ValueError("Harga modal harus lebih dari 0.")
        if not self.harga_jual_wajar(harga_modal, harga_jual):
            raise ValueError(
                f"Harga jual harus minimal memiliki margin "
                f"{Kios.MARGIN_MINIMUM}% dari harga modal."
            )
        if stok < Kios.STOK_MINIMUM:
            raise ValueError("Stok tidak boleh kurang dari 0.")

        self._kode = kode_bersih
        self._nama = nama_bersih
        self._harga_modal = harga_modal
        self._harga_jual = harga_jual
        self._stok = stok

        Kios._jumlah_terdaftar += 1

    @property
    def kode(self) -> str:
        return self._kode

    @property
    def nama(self) -> str:
        return self._nama

    @property
    def harga_modal(self) -> int:
        return self._harga_modal

    @property
    def harga_jual(self) -> int:
        return self._harga_jual

    @property
    def stok(self) -> int:
        return self._stok

    def tambah_stok(self, jumlah: int) -> None:
        """Menambahkan stok produk."""
        if jumlah <= 0:
            raise ValueError("Jumlah penambahan stok harus lebih dari 0.")
        self._stok += jumlah

    def nilai_persediaan(self) -> int:
        """Menghitung nilai persediaan berdasarkan harga modal."""
        return self._harga_modal * self._stok

    def keterangan(self) -> str:
        """Menghasilkan keterangan produk."""
        return (
            f"[{self._kode}] {self._nama} | "
            f"Modal: {self.format_rupiah(self._harga_modal)} | "
            f"Jual: {self.format_rupiah(self._harga_jual)} | "
            f"Stok: {self._stok}"
        )

    @classmethod
    def dari_baris_csv(cls, baris: str) -> "Kios":
        """Membuat objek dari baris teks dengan pemisah titik koma."""
        bagian = baris.strip().split(cls.PEMISAH_BARIS)

        if len(bagian) != 5:
            raise ValueError(
                "Baris data harus berisi 5 bagian: "
                "kode;nama;harga_modal;harga_jual;stok."
            )

        kode, nama, modal_teks, jual_teks, stok_teks = bagian

        try:
            harga_modal = int(modal_teks.strip())
            harga_jual = int(jual_teks.strip())
            stok = int(stok_teks.strip())
        except ValueError as exc:
            raise ValueError("Harga dan stok harus berupa angka bulat.") from exc

        return cls(
            kode.strip(),
            nama.strip(),
            harga_modal,
            harga_jual,
            stok,
        )

    @staticmethod
    def harga_jual_wajar(harga_modal: int, harga_jual: int) -> bool:
        """Memeriksa apakah harga jual memenuhi margin minimum."""
        if harga_modal <= 0 or harga_jual <= 0:
            return False

        harga_minimum = (
            harga_modal * (100 + Kios.MARGIN_MINIMUM) // 100
        )
        return harga_jual >= harga_minimum

    @staticmethod
    def format_rupiah(nilai: int) -> str:
        """Mengubah angka menjadi format rupiah sederhana."""
        return f"Rp{nilai:,}".replace(",", ".")

    @classmethod
    def jumlah_terdaftar(cls) -> int:
        """Mengembalikan jumlah produk yang berhasil dibuat."""
        return cls._jumlah_terdaftar

    @classmethod
    def daftar_rapi(cls, produk: list["Kios"]) -> str:
        """Membuat daftar produk dengan kolom yang diratakan."""
        baris = [
            f"{'KODE':<10} {'NAMA':<20} {'HARGA JUAL':>15} {'STOK':>6}"
        ]

        for item in produk:
            baris.append(
                f"{item.kode:<10} {item.nama:<20} "
                f"{cls.format_rupiah(item.harga_jual):>15} {item.stok:>6}"
            )

        return "\n".join(baris)
