from models.buku_model import BukuModel

model = BukuModel()

# 1. Menampilkan seluruh daftar buku sebelum diubah
print("*** Daftar Buku")
daftar_buku = model.get_all_buku()
for b in daftar_buku:
    print(f"[{b['id_buku']}] {b['judul']} {b['pengarang']} ({b['tahun_terbit']})")

# 2. Proses UPDATE data ID 5
print("\nMengubah data buku...")
model.update_buku(5, "Pengantar Sistem Informasi Lanjutan", "Kadir", 2026)
print("Data berhasil diubah!")

# 3. Proses DELETE data ID 5
print("\nMenghapus data buku...")
model.delete_buku(5)

# 4. Menampilkan seluruh daftar buku setelah dihapus
print("\nDaftar Buku")
daftar_buku_setelah = model.get_all_buku()
for b in daftar_buku_setelah:
    print(f"[{b['id_buku']}] {b['judul']} {b['pengarang']} ({b['tahun_terbit']})")