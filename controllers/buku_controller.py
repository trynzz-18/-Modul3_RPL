
from tkinter import messagebox

from models.buku_model import BukuModel
from views.buku_view import BukuView


class BukuController:

    def __init__(self, user_role):

        # =====================================
        # INISIALISASI MODEL DAN VIEW
        # =====================================

        self.user_role = user_role.lower()

        self.model = BukuModel()
        self.view = BukuView()

        # Menyimpan ID buku yang dipilih
        self.id_buku_terpilih = None

        # Mengatur judul aplikasi sesuai role
        self.view.title(
            f"Sistem Manajemen Perpustakaan - Mode: {self.user_role.upper()}"
        )

        # =====================================
        # PENGATURAN HAK AKSES PENGGUNA
        # =====================================

        if self.user_role == "admin":

            # Admin memiliki akses penuh
            self.view.btn_simpan.configure(
                state="normal"
            )

            self.view.btn_update.configure(
                state="normal"
            )

            self.view.btn_hapus.configure(
                state="normal"
            )

            self.view.entry_judul.configure(
                state="normal"
            )

            self.view.entry_penulis.configure(
                state="normal"
            )

            self.view.entry_tahun.configure(
                state="normal"
            )

            # Menghubungkan tombol CRUD
            self.view.btn_simpan.configure(
                command=self.simpan_data
            )

            self.view.btn_update.configure(
                command=self.update_data
            )

            self.view.btn_hapus.configure(
                command=self.hapus_data
            )

            # Menghubungkan pemilihan baris tabel
            self.view.tabel.bind(
                "<<TreeviewSelect>>",
                self.pilih_buku
            )

        elif self.user_role == "anggota":

            # Anggota hanya dapat melihat data
            self.view.btn_simpan.configure(
                state="disabled"
            )

            self.view.btn_update.configure(
                state="disabled"
            )

            self.view.btn_hapus.configure(
                state="disabled"
            )

            self.view.entry_judul.configure(
                state="disabled"
            )

            self.view.entry_penulis.configure(
                state="disabled"
            )

            self.view.entry_tahun.configure(
                state="disabled"
            )

        else:

            raise ValueError("Role pengguna tidak valid!")

        # Memuat data ketika aplikasi dibuka
        self.muat_data_tabel()

    # =====================================
    # PEMERIKSAAN HAK AKSES
    # =====================================

    def cek_hak_akses(self):

        if self.user_role != "admin":

            messagebox.showwarning(
                "Akses Ditolak",
                "Anda tidak memiliki izin untuk mengelola data buku!",
                parent=self.view
            )

            return False

        return True

    # =====================================
    # MENAMPILKAN DATA BUKU
    # =====================================

    def muat_data_tabel(self):

        try:

            # Mengosongkan isi tabel
            for item in self.view.tabel.get_children():
                self.view.tabel.delete(item)

            # Mengambil data buku aktif dari Model
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
                        buku["tahun_terbit"]
                    )
                )

        except Exception as e:

            messagebox.showerror(
                "Error",
                f"Gagal memuat data buku:\n{e}",
                parent=self.view
            )

    # =====================================
    # MEMILIH DATA BUKU
    # =====================================

    def pilih_buku(self, event=None):

        # Hanya Admin yang dapat memilih data
        if not self.cek_hak_akses():
            return

        selected = self.view.tabel.selection()

        if not selected:
            return

        # Mengambil nilai dari baris tabel
        values = self.view.tabel.item(
            selected[0],
            "values"
        )

        # Menyimpan ID buku yang dipilih
        self.id_buku_terpilih = int(values[0])

        # Memasukkan data ke form
        self.view.entry_judul.set_value(
            values[1]
        )

        self.view.entry_penulis.set_value(
            values[2]
        )

        self.view.entry_tahun.set_value(
            values[3]
        )

    # =====================================
    # MEMBERSIHKAN FORM
    # =====================================

    def bersihkan_form(self):

        # Mengembalikan input ke placeholder
        self.view.entry_judul.set_value("")

        self.view.entry_penulis.set_value("")

        self.view.entry_tahun.set_value("")

        # Menghapus pilihan tabel
        selected = self.view.tabel.selection()

        if selected:
            self.view.tabel.selection_remove(*selected)

        # Menghapus ID terpilih
        self.id_buku_terpilih = None

    # =====================================
    # VALIDASI INPUT
    # =====================================

    def ambil_input(self):

        # Mengambil data dari form
        judul = self.view.entry_judul.get().strip()

        pengarang = self.view.entry_penulis.get().strip()

        tahun = self.view.entry_tahun.get().strip()

        # Validasi form kosong
        if not judul or not pengarang or not tahun:

            messagebox.showwarning(
                "Peringatan",
                "Semua kolom harus diisi!",
                parent=self.view
            )

            return None

        # Validasi tahun
        if not tahun.isdigit():

            messagebox.showwarning(
                "Peringatan",
                "Tahun terbit harus berupa angka!",
                parent=self.view
            )

            return None

        return judul, pengarang, tahun

    # =====================================
    # MENYIMPAN DATA BUKU
    # =====================================

    def simpan_data(self):

        # Pemeriksaan hak akses
        if not self.cek_hak_akses():
            return

        # Mengambil dan memvalidasi input
        data = self.ambil_input()

        if data is None:
            return

        judul, pengarang, tahun = data

        try:

            # Penerbit tetap disimpan di database
            # meskipun tidak ditampilkan pada GUI
            berhasil = self.model.create_buku(
                judul,
                pengarang,
                "",
                tahun
            )

            if berhasil:

                self.muat_data_tabel()

                self.bersihkan_form()

                messagebox.showinfo(
                    "Sukses",
                    "Data buku berhasil disimpan!",
                    parent=self.view
                )

            else:

                messagebox.showerror(
                    "Error",
                    "Data buku gagal disimpan!",
                    parent=self.view
                )

        except Exception as e:

            messagebox.showerror(
                "Error",
                f"Gagal menyimpan data:\n{e}",
                parent=self.view
            )

    # =====================================
    # MEMPERBARUI DATA BUKU
    # =====================================

    def update_data(self):

        # Pemeriksaan hak akses
        if not self.cek_hak_akses():
            return

        # Memeriksa pilihan buku
        if self.id_buku_terpilih is None:

            messagebox.showwarning(
                "Peringatan",
                "Pilih data buku yang ingin diperbarui!",
                parent=self.view
            )

            return

        # Mengambil input
        data = self.ambil_input()

        if data is None:
            return

        judul, pengarang, tahun = data

        try:

            berhasil = self.model.update_buku(
                self.id_buku_terpilih,
                judul,
                pengarang,
                tahun
            )

            if berhasil:

                self.muat_data_tabel()

                self.bersihkan_form()

                messagebox.showinfo(
                    "Sukses",
                    "Data buku berhasil diperbarui!",
                    parent=self.view
                )

            else:

                messagebox.showwarning(
                    "Peringatan",
                    "Data buku tidak ditemukan!",
                    parent=self.view
                )

        except Exception as e:

            messagebox.showerror(
                "Error",
                f"Gagal memperbarui data:\n{e}",
                parent=self.view
            )

    # =====================================
    # MENGHAPUS DATA BUKU (SOFT DELETE)
    # =====================================

    def hapus_data(self):

        # Pemeriksaan hak akses
        if not self.cek_hak_akses():
            return

        # Memeriksa pilihan buku
        if self.id_buku_terpilih is None:

            messagebox.showwarning(
                "Peringatan",
                "Pilih data buku yang ingin dihapus!",
                parent=self.view
            )

            return

        # Menyimpan ID buku sebelum dihapus
        id_dihapus = self.id_buku_terpilih

        # Konfirmasi penghapusan
        konfirmasi = messagebox.askyesno(
            "Konfirmasi",
            f"Apakah Anda yakin ingin menghapus buku ID {id_dihapus}?",
            parent=self.view
        )

        if not konfirmasi:
            return

        try:

            # Menghapus melalui Model
            berhasil = self.model.delete_buku(
                id_dihapus
            )

            if berhasil:

                # Memperbarui tabel
                self.muat_data_tabel()

                # Membersihkan form
                self.bersihkan_form()

                messagebox.showinfo(
                    "Sukses",
                    "Data buku berhasil dihapus dari daftar koleksi!",
                    parent=self.view
                )

            else:

                messagebox.showwarning(
                    "Peringatan",
                    "Data buku tidak ditemukan atau sudah dihapus!",
                    parent=self.view
                )

        except Exception as e:

            messagebox.showerror(
                "Error Penghapusan",
                str(e),
                parent=self.view
            )

    # =====================================
    # MENJALANKAN APLIKASI
    # =====================================

    def run(self):

        self.view.mainloop()
