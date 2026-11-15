
from tkinter import messagebox

from models.buku_model import BukuModel
from views.buku_view import BukuView


class BukuController:

    def __init__(self, user_role, master, on_logout):

        # Informasi pengguna
        self.user_role = user_role.lower()
        self.on_logout = on_logout

        # Inisialisasi Model dan View
        self.model = BukuModel()
        self.view = BukuView(master)

        self.id_buku_terpilih = None

        # Judul berdasarkan role
        self.view.title(
            f"Sistem Manajemen Perpustakaan - Mode: "
            f"{self.user_role.upper()}"
        )

        # Menghubungkan tombol Logout
        self.view.btn_logout.configure(
            command=self.logout
        )

        # Tombol X menjalankan proses Logout
        self.view.protocol(
            "WM_DELETE_WINDOW",
            self.logout
        )

        # =====================================
        # PENGATURAN HAK AKSES
        # =====================================

        if self.user_role == "admin":

            self.view.btn_simpan.configure(
                state="normal",
                command=self.simpan_data
            )

            self.view.btn_update.configure(
                state="normal",
                command=self.update_data
            )

            self.view.btn_hapus.configure(
                state="normal",
                command=self.hapus_data
            )

            self.view.tabel.bind(
                "<<TreeviewSelect>>",
                self.pilih_buku
            )

        elif self.user_role == "anggota":

            # Anggota hanya dapat membaca data
            self.view.btn_simpan.configure(state="disabled")
            self.view.btn_update.configure(state="disabled")
            self.view.btn_hapus.configure(state="disabled")

            self.view.entry_judul.configure(state="disabled")
            self.view.entry_penulis.configure(state="disabled")
            self.view.entry_tahun.configure(state="disabled")

        else:
            self.view.destroy()
            raise ValueError("Role pengguna tidak valid!")

        # Memuat data buku
        self.muat_data_tabel()

    # =====================================
    # CEK HAK AKSES
    # =====================================

    def cek_hak_akses(self):

        if self.user_role != "admin":

            messagebox.showwarning(
                "Akses Ditolak",
                "Anda tidak memiliki izin mengelola data buku!",
                parent=self.view
            )

            return False

        return True

    # =====================================
    # MEMUAT DATA BUKU
    # =====================================

    def muat_data_tabel(self):

        try:
            # Membersihkan tabel
            for item in self.view.tabel.get_children():
                self.view.tabel.delete(item)

            # Mengambil buku aktif dari Model
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
    # MEMILIH BUKU
    # =====================================

    def pilih_buku(self, event=None):

        if not self.cek_hak_akses():
            return

        selected = self.view.tabel.selection()

        if not selected:
            return

        values = self.view.tabel.item(
            selected[0],
            "values"
        )

        self.id_buku_terpilih = int(values[0])

        self.view.entry_judul.set_value(values[1])
        self.view.entry_penulis.set_value(values[2])
        self.view.entry_tahun.set_value(values[3])

    # =====================================
    # MEMBERSIHKAN FORM
    # =====================================

    def bersihkan_form(self):

        self.id_buku_terpilih = None

        self.view.entry_judul.set_value("")
        self.view.entry_penulis.set_value("")
        self.view.entry_tahun.set_value("")

        selected = self.view.tabel.selection()

        if selected:
            self.view.tabel.selection_remove(*selected)

    # =====================================
    # VALIDASI FORM
    # =====================================

    def ambil_input(self):

        judul = self.view.entry_judul.get().strip()
        pengarang = self.view.entry_penulis.get().strip()
        tahun = self.view.entry_tahun.get().strip()

        if not judul or not pengarang or not tahun:

            messagebox.showwarning(
                "Peringatan",
                "Semua kolom harus diisi!",
                parent=self.view
            )

            return None

        if not tahun.isdigit():

            messagebox.showwarning(
                "Peringatan",
                "Tahun terbit harus berupa angka!",
                parent=self.view
            )

            return None

        return judul, pengarang, tahun

    # =====================================
    # SIMPAN DATA BUKU
    # =====================================

    def simpan_data(self):

        if not self.cek_hak_akses():
            return

        data = self.ambil_input()

        if data is None:
            return

        judul, pengarang, tahun = data

        try:
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
                str(e),
                parent=self.view
            )

    # =====================================
    # UPDATE DATA BUKU
    # =====================================

    def update_data(self):

        if not self.cek_hak_akses():
            return

        if self.id_buku_terpilih is None:

            messagebox.showwarning(
                "Peringatan",
                "Pilih buku yang ingin diperbarui!",
                parent=self.view
            )

            return

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
                str(e),
                parent=self.view
            )

    # =====================================
    # DELETE DATA BUKU
    # =====================================

    def hapus_data(self):

        if not self.cek_hak_akses():
            return

        if self.id_buku_terpilih is None:

            messagebox.showwarning(
                "Peringatan",
                "Pilih buku yang ingin dihapus!",
                parent=self.view
            )

            return

        id_dihapus = self.id_buku_terpilih

        konfirmasi = messagebox.askyesno(
            "Konfirmasi",
            f"Apakah Anda yakin ingin menghapus buku ID {id_dihapus}?",
            parent=self.view
        )

        if not konfirmasi:
            return

        try:
            berhasil = self.model.delete_buku(id_dihapus)

            if berhasil:

                self.muat_data_tabel()
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
    # LOGOUT
    # =====================================

    def logout(self):

        konfirmasi = messagebox.askyesno(
            "Konfirmasi Logout",
            "Apakah Anda yakin ingin keluar dari akun ini?",
            parent=self.view
        )

        if not konfirmasi:
            return

        # Tutup jendela aplikasi buku
        self.view.destroy()

        # Kembali ke halaman login
        if self.on_logout:
            self.on_logout()
