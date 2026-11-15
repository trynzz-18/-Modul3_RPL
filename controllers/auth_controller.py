
import tkinter.messagebox as messagebox

from models.user_model import UserModel
from views.login_view import LoginView
from views.register_view import RegisterView
from controllers.buku_controller import BukuController


class AuthController:

    def __init__(self):

        # Inisialisasi Model dan Login View
        self.model = UserModel()
        self.view = LoginView()

        # Menyimpan jendela Register
        self.register_view = None

        # Menyimpan Controller aplikasi buku
        self.buku_controller = None

        # Menghubungkan tombol Login
        self.view.btn_login.configure(
            command=self.proses_login
        )

        # Menghubungkan tombol Register
        self.view.btn_register.configure(
            command=self.buka_register
        )

        # Enter untuk Login
        self.view.entry_password.bind(
            "<Return>",
            lambda event: self.proses_login()
        )

        # Menutup aplikasi melalui tombol X
        self.view.protocol(
            "WM_DELETE_WINDOW",
            self.tutup_aplikasi
        )

    # =====================================
    # PROSES LOGIN
    # =====================================

    def proses_login(self):

        username = self.view.entry_username.get().strip()
        password = self.view.entry_password.get()

        if not username or not password:

            messagebox.showwarning(
                "Peringatan",
                "Username dan Password wajib diisi!",
                parent=self.view
            )
            return

        try:

            # Verifikasi akun melalui UserModel
            user = self.model.login(
                username,
                password
            )

            if user is None:

                messagebox.showerror(
                    "Login Gagal",
                    "Username atau Password salah!",
                    parent=self.view
                )

                self.view.entry_password.delete(0, "end")
                self.view.entry_password.focus_set()
                return

            # Validasi Role
            if user["role"] not in ("admin", "anggota"):

                messagebox.showerror(
                    "Akses Ditolak",
                    "Role pengguna tidak dikenali!",
                    parent=self.view
                )
                return

            messagebox.showinfo(
                "Login Berhasil",
                f"Selamat datang, {user['username']}!\n"
                f"Role: {user['role'].upper()}",
                parent=self.view
            )

            # Menyembunyikan Login ketika masuk aplikasi
            self.view.withdraw()

            try:

                # Membuka aplikasi sesuai Role
                self.buku_controller = BukuController(
                    user_role=user["role"],
                    master=self.view,
                    on_logout=self.kembali_ke_login
                )

            except Exception:
                self.view.deiconify()
                self.view.lift()
                self.view.focus_force()

                self.buku_controller = None
                raise

        except Exception as e:

            messagebox.showerror(
                "Kesalahan Sistem",
                f"Gagal melakukan login:\n{e}",
                parent=self.view
            )

    # =====================================
    # MEMBUKA HALAMAN REGISTER
    # =====================================

    def buka_register(self):

        # Jika Register sudah terbuka, tampilkan kembali
        if self.register_view is not None:

            try:
                if self.register_view.winfo_exists():
                    self.register_view.lift()
                    self.register_view.focus_force()
                    return
            except Exception:
                self.register_view = None

        try:

            # Membuka Register tanpa menutup Login
            self.register_view = RegisterView(self.view)

            # Menghubungkan tombol Daftar
            self.register_view.btn_register.configure(
                command=self.proses_register
            )

            # Menghubungkan tombol Kembali
            self.register_view.btn_kembali.configure(
                command=self.kembali_dari_register
            )

            # Tombol X kembali ke Login
            self.register_view.protocol(
                "WM_DELETE_WINDOW",
                self.kembali_dari_register
            )

            # Mengatur jendela Register
            self.register_view.transient(self.view)

            self.register_view.grab_set()
            self.register_view.lift()
            self.register_view.focus_force()

        except Exception as e:

            self.register_view = None

            messagebox.showerror(
                "Error Register",
                f"Gagal membuka halaman registrasi:\n{e}",
                parent=self.view
            )

    # =====================================
    # PROSES REGISTRASI
    # =====================================

    def proses_register(self):

        username = self.register_view.entry_username.get().strip()
        password = self.register_view.entry_password.get()
        konfirmasi = self.register_view.entry_konfirmasi.get()

        # Validasi input kosong
        if not username or not password or not konfirmasi:

            messagebox.showwarning(
                "Peringatan",
                "Semua kolom registrasi harus diisi!",
                parent=self.register_view
            )
            return

        # Validasi Username
        if len(username) < 4:

            messagebox.showwarning(
                "Peringatan",
                "Username minimal 4 karakter!",
                parent=self.register_view
            )
            return

        if any(char.isspace() for char in username):

            messagebox.showwarning(
                "Peringatan",
                "Username tidak boleh mengandung spasi!",
                parent=self.register_view
            )
            return

        # Validasi Password
        if len(password) < 6:

            messagebox.showwarning(
                "Peringatan",
                "Password minimal 6 karakter!",
                parent=self.register_view
            )
            return

        # Validasi Konfirmasi Password
        if password != konfirmasi:

            messagebox.showerror(
                "Registrasi Gagal",
                "Konfirmasi password tidak cocok!",
                parent=self.register_view
            )

            self.register_view.entry_konfirmasi.delete(0, "end")
            self.register_view.entry_konfirmasi.focus_set()
            return

        try:

            # Menyimpan akun baru ke database
            berhasil = self.model.register_user(
                username,
                password
            )

            if berhasil:

                messagebox.showinfo(
                    "Registrasi Berhasil",
                    "Akun berhasil dibuat!\n"
                    "Silakan login menggunakan akun baru.",
                    parent=self.register_view
                )

                # Menutup jendela Register
                self.register_view.grab_release()
                self.register_view.destroy()
                self.register_view = None

                # Mengisi username pada halaman Login
                self.view.entry_username.delete(0, "end")
                self.view.entry_username.insert(0, username)

                # Mengosongkan password
                self.view.entry_password.delete(0, "end")

                # Menampilkan Login kembali
                self.view.deiconify()
                self.view.lift()
                self.view.focus_force()

                self.view.entry_password.focus_set()

            else:

                messagebox.showerror(
                    "Registrasi Gagal",
                    "Akun gagal dibuat!",
                    parent=self.register_view
                )

        except ValueError as e:

            messagebox.showwarning(
                "Username Tidak Tersedia",
                str(e),
                parent=self.register_view
            )

        except Exception as e:

            messagebox.showerror(
                "Kesalahan Sistem",
                f"Gagal melakukan registrasi:\n{e}",
                parent=self.register_view
            )

    # =====================================
    # KEMBALI DARI REGISTER KE LOGIN
    # =====================================

    def kembali_dari_register(self):

        if self.register_view is not None:

            try:
                self.register_view.grab_release()
                self.register_view.destroy()

            except Exception:
                pass

            self.register_view = None

        # Menampilkan halaman Login
        self.view.deiconify()
        self.view.lift()
        self.view.focus_force()
        self.view.entry_username.focus_set()

    # =====================================
    # LOGOUT
    # =====================================

    def kembali_ke_login(self):

        # Membersihkan data Login
        self.view.entry_username.delete(0, "end")
        self.view.entry_password.delete(0, "end")

        # Menampilkan Login
        self.view.deiconify()
        self.view.lift()
        self.view.focus_force()

        self.view.entry_username.focus_set()

        # Menghapus sesi Controller sebelumnya
        self.buku_controller = None

    # =====================================
    # MENUTUP SELURUH APLIKASI
    # =====================================

    def tutup_aplikasi(self):

        if self.register_view is not None:

            try:
                self.register_view.grab_release()
                self.register_view.destroy()

            except Exception:
                pass

            self.register_view = None

        self.view.destroy()

    # =====================================
    # MENJALANKAN APLIKASI
    # =====================================

    def run(self):

        self.view.mainloop()
