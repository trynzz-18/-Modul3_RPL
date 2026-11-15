
import tkinter as tk


class LoginView(tk.Tk):

    def __init__(self):
        super().__init__()

        # Konfigurasi jendela
        self.title("Login - Sistem Manajemen Perpustakaan")
        self.geometry("440x500")
        self.resizable(False, False)
        self.configure(bg="#f2f2f2")

        # Frame utama
        frame_utama = tk.Frame(
            self,
            bg="#dedede",
            padx=30,
            pady=20
        )

        frame_utama.pack(
            fill="both",
            expand=True,
            padx=15,
            pady=15
        )

        # =====================================
        # JUDUL APLIKASI
        # =====================================

        tk.Label(
            frame_utama,
            text="SISTEM PERPUSTAKAAN",
            font=("Arial", 17, "bold"),
            bg="#dedede",
            fg="#24568b"
        ).pack(pady=(8, 5))

        tk.Label(
            frame_utama,
            text="Silakan login untuk melanjutkan",
            font=("Arial", 10),
            bg="#dedede",
            fg="#555555"
        ).pack(pady=(0, 22))

        # =====================================
        # INPUT USERNAME
        # =====================================

        tk.Label(
            frame_utama,
            text="Username",
            font=("Arial", 10, "bold"),
            bg="#dedede"
        ).pack(anchor="w")

        self.entry_username = tk.Entry(
            frame_utama,
            font=("Arial", 11),
            relief="solid",
            bd=1
        )

        self.entry_username.pack(
            fill="x",
            pady=(6, 15),
            ipady=7
        )

        # =====================================
        # INPUT PASSWORD
        # =====================================

        tk.Label(
            frame_utama,
            text="Password",
            font=("Arial", 10, "bold"),
            bg="#dedede"
        ).pack(anchor="w")

        self.entry_password = tk.Entry(
            frame_utama,
            font=("Arial", 11),
            show="*",
            relief="solid",
            bd=1
        )

        self.entry_password.pack(
            fill="x",
            pady=(6, 20),
            ipady=7
        )

        # =====================================
        # TOMBOL LOGIN
        # =====================================

        self.btn_login = tk.Button(
            frame_utama,
            text="LOGIN",
            font=("Arial", 11, "bold"),
            bg="#24568b",
            fg="white",
            activebackground="#174574",
            activeforeground="white",
            relief="flat",
            cursor="hand2"
        )

        self.btn_login.pack(
            fill="x",
            ipady=8
        )

        # =====================================
        # TEKS REGISTRASI
        # =====================================

        tk.Label(
            frame_utama,
            text="Belum memiliki akun?",
            font=("Arial", 10),
            bg="#dedede",
            fg="#555555"
        ).pack(pady=(17, 7))

        # =====================================
        # TOMBOL REGISTER
        # =====================================

        self.btn_register = tk.Button(
            frame_utama,
            text="REGISTER / DAFTAR",
            font=("Arial", 11, "bold"),
            bg="#c0392b",
            fg="white",
            activebackground="#922b21",
            activeforeground="white",
            relief="flat",
            cursor="hand2"
        )

        self.btn_register.pack(
            fill="x",
            ipady=8
        )

        # Enter untuk login
        self.entry_password.bind(
            "<Return>",
            lambda event: self.btn_login.invoke()
        )

        # Fokus awal
        self.entry_username.focus_set()
