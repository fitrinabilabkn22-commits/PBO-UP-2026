"""Program utama untuk mendemonstrasikan enkapsulasi P03."""

from src.model.alamat import Alamat
from src.model.alat_tani import AlatTani
from src.model.penyewa import Penyewa


def main() -> None:
    alamat_budi = Alamat("Pulau Jambu", "Kuok", "Kuok")
    budi = Penyewa("1406012509900001", "Budi Santoso", alamat_budi, "0812-3456-7890")

    print(budi.identitas())
    print(f"Dusun {budi.alamat.dusun}, Desa {budi.alamat.desa}, Kec. {budi.alamat.kecamatan}")

    alat = AlatTani("TR-01", "Traktor Roda Dua Kubota", 150000)
    print(alat.keterangan())

    print("-- Percobaan menembus penjagaan")
    try:
        alat.tarif_harian = 0
    except ValueError as e:
        print(f"Ditolak (tarif nol): {e}")

    try:
        alat.tarif_harian = -5000
    except ValueError as e:
        print(f"Ditolak (tarif minus): {e}")

    print(f"Tarif tetap utuh: {alat.keterangan()}")


if __name__ == "__main__":
    main()