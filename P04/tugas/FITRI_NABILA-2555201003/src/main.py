"""Program utama untuk mendemonstrasikan anggota kelas P04."""

from src.model.alat_tani import AlatTani


def main() -> None:
    print(f"Sebelum pendataan, alat terdaftar: {AlatTani.jumlah_terdaftar()}")

    alat1 = AlatTani("TR-01", "Traktor Roda Dua Kubota", 150000)
    print(f" {alat1.keterangan()}")

    alat2 = AlatTani("PA-01", "Pompa Air 3 Inci", 75000)
    print(f" {alat2.keterangan()}")

    _ = AlatTani.dari_baris_csv("TR-02;Traktor Rotary;200000")
    _ = AlatTani.dari_baris_csv("PA-02;Pompa Air 4 Inci;85000")

    print(f"Sesudah pendataan, alat terdaftar: {AlatTani.jumlah_terdaftar()}")

    print("--- Memeriksa tarif tanpa membuat objek ---")
    for calon in (5_000, 150_000, 6_000_000):
        status = "wajar" if AlatTani.tarif_wajar(calon) else "ditolak"
        print(f" {AlatTani.format_rupiah(calon)} → {status}")


if __name__ == "__main__":
    main()