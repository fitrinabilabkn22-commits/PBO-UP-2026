#!/usr/bin/env python3
"""
periksa_pbo.py — Pemeriksa disiplin berorientasi objek untuk tugas Python.

Dipakai mahasiswa sebelum mengumpulkan, dan dipakai dosen saat menilai.
Kode yang tidak lolos pemeriksa ini dinyatakan BELUM SELESAI, sebagaimana
kode Java yang tidak lolos compiler.

Pemakaian:
    python periksa_pbo.py src/                     # aturan dasar
    python periksa_pbo.py src/ --profil p06        # + aturan khas Pertemuan 6
    python periksa_pbo.py src/ --daftar-profil

Kode keluar: 0 bila lolos, 1 bila ada pelanggaran.

Prodi Teknik Informatika — Universitas Pahlawan Tuanku Tambusai
"""
from __future__ import annotations

import argparse
import ast
import sys
from dataclasses import dataclass, field
from pathlib import Path

# --------------------------------------------------------------------------
# Profil per pertemuan: syarat tambahan yang wajib muncul di kode mahasiswa.
# Kunci dipakai lewat --profil. Nilai None berarti syarat tidak diperiksa.
# --------------------------------------------------------------------------
PROFIL: dict[str, dict[str, object]] = {
    "dasar":  {"min_kelas": 1},
    "p02":    {"min_kelas": 2, "wajib_konstruktor": True},
    "p03":    {"min_kelas": 2, "wajib_property": True},
    "p04":    {"min_kelas": 2, "wajib_konstanta_kelas": True},
    "p05":    {"min_kelas": 4},
    "p06":    {"min_kelas": 3, "wajib_pewarisan": True, "wajib_override_dunder": True},
    "p07":    {"min_kelas": 3, "wajib_pewarisan": True},
    "p09":    {"min_kelas": 3, "wajib_abstraksi": True},
    "p10":    {"min_kelas": 3, "wajib_eksepsi_sendiri": True},
    "p11":    {"min_kelas": 3, "wajib_generik": True},
    "p12":    {"min_kelas": 3},
    "p13":    {"min_kelas": 4, "wajib_protocol": True, "larang_sql_di_model": True},
    "p14":    {"min_kelas": 4, "wajib_uji": True},
    "proyek": {"min_kelas": 4, "wajib_pewarisan": True, "wajib_abstraksi": True,
               "wajib_property": True, "larang_sql_di_model": True, "wajib_uji": True},
}

DUNDER_OVERRIDE = {"__str__", "__repr__", "__eq__", "__hash__", "__lt__", "__len__"}


@dataclass
class Temuan:
    berkas: str
    baris: int
    kode: str
    pesan: str

    def __str__(self) -> str:
        return f"  {self.berkas}:{self.baris}  [{self.kode}] {self.pesan}"


@dataclass
class Rekap:
    """Fakta yang dikumpulkan dari seluruh berkas, untuk uji tingkat proyek."""
    jumlah_kelas: int = 0
    ada_pewarisan: bool = False
    ada_property: bool = False
    ada_abstraksi: bool = False
    ada_protocol: bool = False
    ada_eksepsi_sendiri: bool = False
    ada_konstruktor: bool = False
    ada_konstanta_kelas: bool = False
    ada_generik: bool = False
    dunder_dioverride: set[str] = field(default_factory=set)
    berkas_uji: int = 0
    fungsi_uji: int = 0


class PemeriksaBerkas(ast.NodeVisitor):
    """Menelusuri satu berkas dan mencatat pelanggaran serta fakta."""

    def __init__(self, nama: str, rekap: Rekap, larang_sql_di_model: bool) -> None:
        self.nama = nama
        self.rekap = rekap
        self.larang_sql = larang_sql_di_model
        self.temuan: list[Temuan] = []
        self._tumpukan_kelas: list[str] = []
        self._nama_model = nama.replace("\\", "/").split("/")
        self._di_lapisan_model = "model" in self._nama_model or "domain" in self._nama_model

    # ---------------------------------------------------------------- bantu
    def lapor(self, simpul: ast.AST, kode: str, pesan: str) -> None:
        self.temuan.append(Temuan(self.nama, getattr(simpul, "lineno", 0), kode, pesan))

    @staticmethod
    def _nama_dekorator(dek: ast.expr) -> str:
        if isinstance(dek, ast.Name):
            return dek.id
        if isinstance(dek, ast.Attribute):
            return dek.attr
        if isinstance(dek, ast.Call):
            return PemeriksaBerkas._nama_dekorator(dek.func)
        return ""

    @staticmethod
    def _nama_basis(b: ast.expr) -> str:
        if isinstance(b, ast.Name):
            return b.id
        if isinstance(b, ast.Attribute):
            return b.attr
        if isinstance(b, ast.Subscript):
            return PemeriksaBerkas._nama_basis(b.value)
        return ""

    # ------------------------------------------------- aturan tingkat modul
    def periksa_tingkat_modul(self, pohon: ast.Module) -> None:
        """PBO-001: tidak boleh ada kode prosedural yang menggantung di modul."""
        for simpul in pohon.body:
            if isinstance(simpul, (ast.Import, ast.ImportFrom, ast.ClassDef,
                                   ast.FunctionDef, ast.AsyncFunctionDef)):
                continue
            if isinstance(simpul, ast.Expr) and isinstance(simpul.value, ast.Constant) \
                    and isinstance(simpul.value.value, str):
                continue  # docstring modul
            if isinstance(simpul, ast.If) and self._adalah_penjaga_main(simpul):
                continue
            if isinstance(simpul, ast.AnnAssign) and isinstance(simpul.target, ast.Name):
                if simpul.target.id.isupper():
                    continue  # konstanta modul beranotasi, diizinkan
                self.lapor(simpul, "PBO-002",
                           f"variabel modul '{simpul.target.id}' harus menjadi atribut kelas, "
                           "atau ditulis HURUF_BESAR bila memang konstanta")
                continue
            if isinstance(simpul, ast.Assign):
                target = simpul.targets[0]
                nm = target.id if isinstance(target, ast.Name) else "<?>"
                if isinstance(target, ast.Name) and nm.isupper():
                    self.lapor(simpul, "PBO-003",
                               f"konstanta modul '{nm}' wajib beranotasi tipe, "
                               f"contoh: {nm}: Final[int] = ...")
                else:
                    self.lapor(simpul, "PBO-002",
                               f"variabel modul '{nm}' harus menjadi atribut kelas")
                continue
            self.lapor(simpul, "PBO-001",
                       "kode berjalan di tingkat modul; bungkus dalam kelas atau method, "
                       "atau letakkan di blok if __name__ == '__main__'")

    @staticmethod
    def _adalah_penjaga_main(simpul: ast.If) -> bool:
        uji = simpul.test
        return (isinstance(uji, ast.Compare)
                and isinstance(uji.left, ast.Name) and uji.left.id == "__name__"
                and len(uji.comparators) == 1
                and isinstance(uji.comparators[0], ast.Constant)
                and uji.comparators[0].value == "__main__")

    # ------------------------------------------------------------- kunjungan
    def visit_ClassDef(self, simpul: ast.ClassDef) -> None:
        self.rekap.jumlah_kelas += 1
        dekorator = {self._nama_dekorator(d) for d in simpul.decorator_list}
        basis = {self._nama_basis(b) for b in simpul.bases}

        if not ast.get_docstring(simpul):
            self.lapor(simpul, "PBO-010", f"kelas '{simpul.name}' tanpa docstring")
        if not simpul.name[:1].isupper():
            self.lapor(simpul, "PBO-011",
                       f"nama kelas '{simpul.name}' harus PascalCase")

        if basis - {"object", "ABC", "Protocol", "Enum", "Exception", "ValueError"}:
            self.rekap.ada_pewarisan = True
        if "ABC" in basis or any(
            self._nama_dekorator(d) == "abstractmethod"
            for m in simpul.body if isinstance(m, ast.FunctionDef) for d in m.decorator_list
        ):
            self.rekap.ada_abstraksi = True
        if "Protocol" in basis:
            self.rekap.ada_protocol = True
        if basis & {"Exception", "ValueError", "RuntimeError"} or simpul.name.endswith("Error"):
            self.rekap.ada_eksepsi_sendiri = True
        if any(isinstance(b, ast.Subscript) for b in simpul.bases):
            self.rekap.ada_generik = True

        beku = any(
            isinstance(d, ast.Call) and self._nama_dekorator(d) == "dataclass"
            and any(k.arg == "frozen" and getattr(k.value, "value", False) for k in d.keywords)
            for d in simpul.decorator_list
        )

        # Nama yang punya @property atau @nama.setter: penugasan self.nama = ...
        # di __init__ sah karena melewati setter, bukan menembus enkapsulasi.
        properti: set[str] = set()
        for anggota in simpul.body:
            if isinstance(anggota, ast.FunctionDef):
                for d in anggota.decorator_list:
                    if self._nama_dekorator(d) in {"property", "setter", "cached_property"}:
                        properti.add(anggota.name)

        self._tumpukan_kelas.append(simpul.name)
        for anggota in simpul.body:
            if isinstance(anggota, ast.AnnAssign) and isinstance(anggota.target, ast.Name):
                if anggota.target.id.isupper():
                    self.rekap.ada_konstanta_kelas = True
                elif not beku and "dataclass" not in dekorator \
                        and not anggota.target.id.startswith("_"):
                    self.lapor(anggota, "PBO-020",
                               f"atribut kelas '{anggota.target.id}' terbuka; "
                               "gunakan awalan garis bawah dan @property")
            if isinstance(anggota, ast.FunctionDef):
                nm = anggota.name
                if nm == "__init__":
                    self.rekap.ada_konstruktor = True
                if nm in DUNDER_OVERRIDE:
                    self.rekap.dunder_dioverride.add(nm)
                if any(self._nama_dekorator(d) == "property" for d in anggota.decorator_list):
                    self.rekap.ada_property = True
                self._periksa_anotasi(anggota, dalam_kelas=True, beku=beku)
                if not beku and nm == "__init__":
                    self._periksa_atribut_init(anggota, dekorator, properti)
        self.generic_visit(simpul)
        self._tumpukan_kelas.pop()

    def visit_FunctionDef(self, simpul: ast.FunctionDef) -> None:
        if not self._tumpukan_kelas:
            if simpul.name.startswith("test_"):
                self.rekap.fungsi_uji += 1
            else:
                self._periksa_anotasi(simpul, dalam_kelas=False, beku=False)
        self.generic_visit(simpul)

    def visit_Global(self, simpul: ast.Global) -> None:
        self.lapor(simpul, "PBO-004",
                   f"pernyataan global '{', '.join(simpul.names)}' tidak diizinkan")

    def visit_ExceptHandler(self, simpul: ast.ExceptHandler) -> None:
        if simpul.type is None:
            self.lapor(simpul, "PBO-030",
                       "except telanjang menangkap segalanya; sebutkan jenis eksepsinya")
        badan = simpul.body
        if len(badan) == 1 and isinstance(badan[0], ast.Pass):
            self.lapor(simpul, "PBO-031",
                       "eksepsi ditelan tanpa penanganan; tangani atau lempar ulang")
        self.generic_visit(simpul)

    def visit_Call(self, simpul: ast.Call) -> None:
        if self.larang_sql and self._di_lapisan_model:
            f = simpul.func
            nm = f.attr if isinstance(f, ast.Attribute) else (f.id if isinstance(f, ast.Name) else "")
            if nm in {"execute", "executemany", "connect", "cursor"}:
                self.lapor(simpul, "PBO-040",
                           "akses basis data di lapisan model; pindahkan ke repository")
            if nm == "print" and self._tumpukan_kelas:
                self.lapor(simpul, "PBO-041",
                           "print di kelas domain; tampilan adalah tugas lapisan antarmuka")
        self.generic_visit(simpul)

    # --------------------------------------------------------------- rincian
    def _periksa_anotasi(self, fn: ast.FunctionDef, *, dalam_kelas: bool, beku: bool) -> None:
        a = fn.args
        semua = list(a.posonlyargs) + list(a.args) + list(a.kwonlyargs)
        if dalam_kelas and semua and semua[0].arg in {"self", "cls"}:
            semua = semua[1:]
        for arg in semua:
            if arg.annotation is None:
                self.lapor(fn, "PBO-050",
                           f"parameter '{arg.arg}' pada '{fn.name}' tanpa anotasi tipe")
        if fn.returns is None and fn.name != "__init__":
            self.lapor(fn, "PBO-051", f"'{fn.name}' tanpa anotasi tipe kembalian")
        if fn.name == "__init__" and fn.returns is None:
            self.lapor(fn, "PBO-051", "'__init__' wajib beranotasi -> None")

    def _periksa_atribut_init(self, fn: ast.FunctionDef, dekorator: set[str],
                              properti: set[str]) -> None:
        if "dataclass" in dekorator:
            return
        for simpul in ast.walk(fn):
            if isinstance(simpul, (ast.Assign, ast.AnnAssign)):
                sasaran = simpul.targets if isinstance(simpul, ast.Assign) else [simpul.target]
                for t in sasaran:
                    if isinstance(t, ast.Attribute) and isinstance(t.value, ast.Name) \
                            and t.value.id == "self" and not t.attr.startswith("_") \
                            and t.attr not in properti:
                        self.lapor(simpul, "PBO-021",
                                   f"atribut 'self.{t.attr}' terbuka; tulis 'self._{t.attr}' "
                                   "dan sediakan @property bila perlu dibaca dari luar")


def periksa_berkas(jalur: Path, rekap: Rekap, larang_sql: bool) -> list[Temuan]:
    sumber = jalur.read_text(encoding="utf-8")
    try:
        pohon = ast.parse(sumber, filename=str(jalur))
    except SyntaxError as e:
        return [Temuan(jalur.name, e.lineno or 0, "PBO-000", f"gagal diurai: {e.msg}")]
    p = PemeriksaBerkas(str(jalur), rekap, larang_sql)
    if jalur.name.startswith("test_") or "tests" in jalur.parts:
        rekap.berkas_uji += 1
    else:
        p.periksa_tingkat_modul(pohon)
    p.visit(pohon)
    return p.temuan


def periksa_syarat_profil(profil: dict[str, object], r: Rekap) -> list[Temuan]:
    t: list[Temuan] = []
    def gagal(kode: str, pesan: str) -> None:
        t.append(Temuan("<proyek>", 0, kode, pesan))

    minimum = int(profil.get("min_kelas", 1))  # type: ignore[arg-type]
    if r.jumlah_kelas < minimum:
        gagal("PBO-100", f"ditemukan {r.jumlah_kelas} kelas, minimum {minimum}")
    syarat = [
        ("wajib_konstruktor", r.ada_konstruktor, "PBO-101", "tidak ada kelas dengan __init__"),
        ("wajib_property", r.ada_property, "PBO-102", "tidak ada @property; enkapsulasi belum ditunjukkan"),
        ("wajib_konstanta_kelas", r.ada_konstanta_kelas, "PBO-103", "tidak ada konstanta tingkat kelas"),
        ("wajib_pewarisan", r.ada_pewarisan, "PBO-104", "tidak ada pewarisan antar kelas"),
        ("wajib_abstraksi", r.ada_abstraksi, "PBO-105", "tidak ada ABC atau @abstractmethod"),
        ("wajib_protocol", r.ada_protocol, "PBO-106", "tidak ada typing.Protocol sebagai kontrak"),
        ("wajib_eksepsi_sendiri", r.ada_eksepsi_sendiri, "PBO-107", "tidak ada kelas eksepsi buatan sendiri"),
        ("wajib_generik", r.ada_generik, "PBO-108", "tidak ada penggunaan tipe generik"),
    ]
    for kunci, terpenuhi, kode, pesan in syarat:
        if profil.get(kunci) and not terpenuhi:
            gagal(kode, pesan)
    if profil.get("wajib_override_dunder") and not (r.dunder_dioverride & {"__str__", "__eq__"}):
        gagal("PBO-109", "belum ada penulisan ulang __str__ maupun __eq__")
    if profil.get("wajib_uji"):
        if r.berkas_uji == 0:
            gagal("PBO-110", "tidak ada berkas pengujian (test_*.py)")
        elif r.fungsi_uji < 5:
            gagal("PBO-111", f"hanya {r.fungsi_uji} fungsi uji, minimum 5")
    return t


def main() -> int:
    ap = argparse.ArgumentParser(description="Pemeriksa disiplin PBO untuk kode Python.")
    ap.add_argument("sasaran", nargs="?", default="src", help="berkas atau folder yang diperiksa")
    ap.add_argument("--profil", default="dasar", help="profil aturan per pertemuan")
    ap.add_argument("--daftar-profil", action="store_true", help="tampilkan profil tersedia")
    arg = ap.parse_args()

    if arg.daftar_profil:
        for k, v in PROFIL.items():
            print(f"{k:9s} {v}")
        return 0
    if arg.profil not in PROFIL:
        print(f"Profil '{arg.profil}' tidak dikenal. Pakai --daftar-profil.", file=sys.stderr)
        return 2

    akar = Path(arg.sasaran)
    berkas = [akar] if akar.is_file() else sorted(akar.rglob("*.py"))
    berkas = [b for b in berkas if "__pycache__" not in b.parts]
    if not berkas:
        print(f"Tidak ada berkas .py di '{akar}'.", file=sys.stderr)
        return 2

    profil = PROFIL[arg.profil]
    rekap = Rekap()
    temuan: list[Temuan] = []
    for b in berkas:
        temuan += periksa_berkas(b, rekap, bool(profil.get("larang_sql_di_model")))
    temuan += periksa_syarat_profil(profil, rekap)

    print(f"Pemeriksa disiplin PBO  \u00b7  profil: {arg.profil}  \u00b7  {len(berkas)} berkas")
    print(f"Kelas ditemukan: {rekap.jumlah_kelas}   fungsi uji: {rekap.fungsi_uji}")
    print("-" * 68)
    if not temuan:
        print("LOLOS. Tidak ada pelanggaran disiplin berorientasi objek.")
        return 0
    for t in sorted(temuan, key=lambda x: (x.berkas, x.baris)):
        print(t)
    print("-" * 68)
    print(f"TIDAK LOLOS: {len(temuan)} pelanggaran. Perbaiki lalu jalankan ulang.")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
