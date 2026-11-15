
import tkinter.messagebox as messagebox

from models.user_model import UserModel
from views.login_view import LoginView
from controllers.buku_controller import BukuController


class AuthController:

    def __init__(self):

        # Inisialisasi Model dan Login View
        self.model = UserModel()
        self.view = LoginView()

        # Menyimpan controller aplikasi buku
        self.buku_controller = None

        # Menghubungkan tombol Login
        self.view.btn_login.configure(
            command=self.proses_login
        )

        # Enter untuk login
        self.view.entry_password.bind(
            "<Return>",
            lambda event: self.proses_login()
        )

        # Menutup aplikasi ketika X Login ditekan
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

        # Validasi input
        if not username or not password:

            messagebox.showwarning(
                "Peringatan",
                "Username dan Password wajib diisi!",
                parent=self.view
            )

            return

        try:

            # Verifikasi melalui UserModel
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

            # Validasi role
            if user["role"] not in ("admin", "anggota"):

                messagebox.showerror(
                    "Akses Ditolak",
                    "Role pengguna tidak dikenali!",
                    parent=self.view
                )

                return

            # Menampilkan pesan login berhasil
            messagebox.showinfo(
                "Login Berhasil",
                f"Selamat datang, {user['username']}!\n"
                f"Role: {user['role'].upper()}",
                parent=self.view
            )

            # Menyembunyikan jendela Login
            self.view.withdraw()

            try:

                # Membuka aplikasi sesuai role
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
    # KEMBALI KE LOGIN SETELAH LOGOUT
    # =====================================

    def kembali_ke_login(self):

        # Membersihkan input login
        self.view.entry_username.delete(0, "end")
        self.view.entry_password.delete(0, "end")

        # Menampilkan kembali halaman Login
        self.view.deiconify()
        self.view.lift()
        self.view.focus_force()

        self.view.entry_username.focus_set()

        # Menghapus referensi controller sebelumnya
        self.buku_controller = None

    # =====================================
    # MENUTUP APLIKASI
    # =====================================

    def tutup_aplikasi(self):

        self.view.destroy()

    # =====================================
    # MENJALANKAN APLIKASI
    # =====================================

    def run(self):

        self.view.mainloop()
