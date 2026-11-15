
import tkinter as tk


class RegisterView(tk.Toplevel):

    def __init__(self, master):
        super().__init__(master)

        self.title("Register - Pendaftaran Anggota")
        self.geometry("420x450")
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
            text="REGISTRASI ANGGOTA",
            font=("Arial", 17, "bold"),
            bg="#dedede",
            fg="#198754"
        ).pack(pady=(5, 8))

        tk.Label(
            frame_utama,
            text="Buat akun baru perpustakaan",
            font=("Arial", 10),
            bg="#dedede",
            fg="#555555"
        ).pack(pady=(0, 20))

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
            pady=(5, 15),
            ipady=6
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
            pady=(5, 15),
            ipady=6
        )

        # Konfirmasi Password
        tk.Label(
            frame_utama,
            text="Konfirmasi Password",
            font=("Arial", 10, "bold"),
            bg="#dedede"
        ).pack(anchor="w")

        self.entry_konfirmasi = tk.Entry(
            frame_utama,
            font=("Arial", 11),
            show="*",
            relief="solid",
            bd=1
        )

        self.entry_konfirmasi.pack(
            fill="x",
            pady=(5, 20),
            ipady=6
        )

        # Informasi role
        tk.Label(
            frame_utama,
            text="Role akun baru: ANGGOTA",
            font=("Arial", 9, "bold"),
            bg="#dedede",
            fg="#24568b"
        ).pack(pady=(0, 12))

        # Tombol daftar
        self.btn_register = tk.Button(
            frame_utama,
            text="DAFTAR SEKARANG",
            font=("Arial", 10, "bold"),
            bg="#198754",
            fg="white",
            activebackground="#146c43",
            activeforeground="white",
            relief="flat",
            cursor="hand2"
        )

        self.btn_register.pack(
            fill="x",
            ipady=7
        )

        # Tombol kembali
        self.btn_kembali = tk.Button(
            frame_utama,
            text="Kembali ke Login",
            font=("Arial", 10),
            bg="#6c757d",
            fg="white",
            activebackground="#565e64",
            activeforeground="white",
            relief="flat",
            cursor="hand2"
        )

        self.btn_kembali.pack(
            fill="x",
            pady=(10, 0),
            ipady=6
        )

        self.entry_username.focus_set()
