from models.anggota_model import AnggotaModel

model = AnggotaModel()

# 1. Menampilkan daftar anggota sebelum ditambah
print("=== Daftar Anggota Perpustakaan ===")
daftar_anggota = model.get_all_anggota()
for a in daftar_anggota:
    print(f"[{a['id_anggota']}] {a['nama']} - {a['alamat']}")

# 2. Menambahkan data anggota baru
print("\nMenambahkan data anggota baru...")
if model.create_anggota("Trian Firmansa", "Makassar"):
    print("Data anggota berhasil disimpan!\n")

# 3. Menampilkan daftar anggota setelah ditambah
print("=== Daftar Anggota Perpustakaan ===")
daftar_anggota_setelah = model.get_all_anggota()
for a in daftar_anggota_setelah:
    print(f"[{a['id_anggota']}] {a['nama']} - {a['alamat']}")