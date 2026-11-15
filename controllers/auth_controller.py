
import tkinter.messagebox as messagebox

from models.user_model import UserModel
from views.login_view import LoginView
from controllers.buku_controller import BukuController


class AuthController:

    def __init__(self):

        # Inisialisasi Model dan View
        self.model = UserModel()
        self.view = LoginView()

        # Menghubungkan tombol Login
        self.view.btn_login.configure(
            command=self.proses_login
        )

    # =====================================
    # PROSES LOGIN
    # =====================================

    def proses_login(self):

        # Mengambil input dari View
        username = self.view.entry_username.get().strip()
        password = self.view.entry_password.get()

        # Validasi form kosong
        if not username or not password:

            messagebox.showwarning(
                "Peringatan",
                "Username dan Password wajib diisi!",
                parent=self.view
            )

            return

        try:

            # Verifikasi akun melalui Model
            user = self.model.login(
                username,
                password
            )

            if user:

                messagebox.showinfo(
                    "Login Berhasil",
                    f"Selamat datang, {user['username']}!\n"
                    f"Role: {user['role'].upper()}",
                    parent=self.view
                )

                # Menutup jendela Login
                self.view.destroy()

                # Membuka aplikasi berdasarkan role pengguna
                app_utama = BukuController(
                    user_role=user['role']
                )

                app_utama.run()

            else:

                messagebox.showerror(
                    "Login Gagal",
                    "Username atau Password salah!",
                    parent=self.view
                )

                self.view.entry_password.delete(0, "end")
                self.view.entry_password.focus_set()

        except Exception as e:

            messagebox.showerror(
                "Kesalahan Sistem",
                f"Gagal melakukan login:\n{e}",
                parent=self.view
            )

    # =====================================
    # MENJALANKAN APLIKASI LOGIN
    # =====================================

    def run(self):

        self.view.mainloop()
