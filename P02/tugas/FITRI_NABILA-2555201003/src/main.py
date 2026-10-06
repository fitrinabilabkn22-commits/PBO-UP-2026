"""Titik masuk program. Satu-satunya berkas yang boleh mencetak."""

from src.model.alat_tani import AlatTani
from src.model.penyewa import Penyewa


def main() -> None:
    budi = Penyewa("1406012509900001", "Budi Santoso", "Kuok", "0812-3456-7890")
    siti = Penyewa("1406014403950002", "Siti Aminah", "Salo")
    
    traktor = AlatTani("TR-01", "Traktor Roda Dua Kubota", 150000)
    pompa = AlatTani("PA-01", "Pompa Air 3 Inci", 75000)

    print(budi.identitas())
    print(budi.kontak())
    print(siti.kontak())
    print(traktor.keterangan())


if __name__ == "__main__":
    main()