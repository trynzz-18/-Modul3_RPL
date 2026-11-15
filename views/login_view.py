
import tkinter as tk


class LoginView(tk.Tk):

    def __init__(self):
        super().__init__()

        self.title("Login - Sistem Manajemen Perpustakaan")
        self.geometry("420x370")
        self.resizable(False, False)
        self.configure(bg="#f2f2f2")

        # Frame utama
        frame_utama = tk.Frame(
            self,
            bg="#dedede",
            padx=30,
            pady=25
        )

        frame_utama.pack(
            fill="both",
            expand=True,
            padx=20,
            pady=20
        )

        # Judul
        tk.Label(
            frame_utama,
            text="SISTEM PERPUSTAKAAN",
            font=("Arial", 17, "bold"),
            bg="#dedede",
            fg="#24568b"
        ).pack(pady=(5, 8))

        tk.Label(
            frame_utama,
            text="Silakan login untuk melanjutkan",
            font=("Arial", 10),
            bg="#dedede",
            fg="#555555"
        ).pack(pady=(0, 25))

        # Username
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
            pady=(6, 18),
            ipady=7
        )

        # Password
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
            pady=(6, 22),
            ipady=7
        )

        # Tombol Login
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

        self.entry_username.focus_set()
