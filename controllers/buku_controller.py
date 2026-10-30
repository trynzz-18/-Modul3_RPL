
from tkinter import messagebox
from models.buku_model import BukuModel
from views.buku_view import BukuView


class BukuController:

    def __init__(self):
        # Inisialisasi Model dan View
        self.model = BukuModel()
        self.view = BukuView()

        # Menghubungkan tombol Simpan
        self.view.btn_simpan.configure(command=self.simpan_data)

        # Memuat data saat aplikasi dibuka
        self.muat_data_tabel()

    def muat_data_tabel(self):
        # Mengosongkan tabel
        for item in self.view.tabel.get_children():
            self.view.tabel.delete(item)

        # Mengambil data dari database
        data_buku = self.model.get_all_buku()

        # Memasukkan data ke tabel
        for buku in data_buku:
            self.view.tabel.insert(
                "",
                "end",
                values=(
                    buku["id_buku"],
                    buku["judul"],
                    buku["pengarang"],
                    buku["penerbit"],
                    buku["tahun_terbit"]
                )
            )

    def simpan_data(self):
        # Mengambil data dari form
        judul = self.view.entry_judul.get()
        pengarang = self.view.entry_penulis.get()
        penerbit = self.view.entry_penerbit.get()
        tahun = self.view.entry_tahun.get()

        # Validasi form kosong
        if not judul or not pengarang or not penerbit or not tahun:
            messagebox.showwarning(
                "Peringatan",
                "Semua kolom form harus diisi!"
            )
            return

        # Menyimpan data melalui Model
        berhasil = self.model.create_buku(
            judul,
            pengarang,
            penerbit,
            tahun
        )

        if berhasil:
            messagebox.showinfo(
                "Sukses",
                "Data buku berhasil disimpan!"
            )

            # Membersihkan form
            self.view.entry_judul.delete(0, "end")
            self.view.entry_penulis.delete(0, "end")
            self.view.entry_penerbit.delete(0, "end")
            self.view.entry_tahun.delete(0, "end")

            # Memuat ulang tabel
            self.muat_data_tabel()

        else:
            messagebox.showerror(
                "Error",
                "Terjadi kesalahan saat menyimpan data."
            )

    def run(self):
        # Menjalankan aplikasi
        self.view.mainloop()
