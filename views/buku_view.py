
import tkinter as tk
from tkinter import ttk


class BukuView(tk.Tk):

    def __init__(self):
        super().__init__()

        self.title("Sistem Informasi Perpustakaan - Data Buku")
        self.geometry("750x500")
        self.resizable(False, False)

        # Judul aplikasi
        tk.Label(
            self,
            text="MANAJEMEN DATA BUKU",
            font=("Arial", 16, "bold")
        ).pack(pady=15)

        # Frame form
        frame_form = tk.Frame(self)
        frame_form.pack(pady=10)

        # Input judul
        tk.Label(frame_form, text="Judul Buku").grid(
            row=0, column=0, padx=10, pady=5, sticky="w"
        )
        self.entry_judul = tk.Entry(frame_form, width=40)
        self.entry_judul.grid(row=0, column=1, pady=5)

        # Input pengarang
        tk.Label(frame_form, text="Pengarang").grid(
            row=1, column=0, padx=10, pady=5, sticky="w"
        )
        self.entry_penulis = tk.Entry(frame_form, width=40)
        self.entry_penulis.grid(row=1, column=1, pady=5)

        # Input penerbit
        tk.Label(frame_form, text="Penerbit").grid(
            row=2, column=0, padx=10, pady=5, sticky="w"
        )
        self.entry_penerbit = tk.Entry(frame_form, width=40)
        self.entry_penerbit.grid(row=2, column=1, pady=5)

        # Input tahun terbit
        tk.Label(frame_form, text="Tahun Terbit").grid(
            row=3, column=0, padx=10, pady=5, sticky="w"
        )
        self.entry_tahun = tk.Entry(frame_form, width=40)
        self.entry_tahun.grid(row=3, column=1, pady=5)

        # Tombol simpan
        self.btn_simpan = tk.Button(
            self,
            text="Simpan Data",
            width=20,
            bg="#198754",
            fg="white"
        )
        self.btn_simpan.pack(pady=15)

        # Tabel buku
        frame_tabel = tk.Frame(self)
        frame_tabel.pack(fill="both", expand=True, padx=15, pady=10)

        kolom = (
            "id_buku",
            "judul",
            "pengarang",
            "penerbit",
            "tahun_terbit"
        )

        self.tabel = ttk.Treeview(
            frame_tabel,
            columns=kolom,
            show="headings"
        )

        self.tabel.heading("id_buku", text="ID")
        self.tabel.heading("judul", text="Judul")
        self.tabel.heading("pengarang", text="Pengarang")
        self.tabel.heading("penerbit", text="Penerbit")
        self.tabel.heading("tahun_terbit", text="Tahun")

        self.tabel.column("id_buku", width=45)
        self.tabel.column("judul", width=180)
        self.tabel.column("pengarang", width=140)
        self.tabel.column("penerbit", width=140)
        self.tabel.column("tahun_terbit", width=80)

        self.tabel.pack(fill="both", expand=True)
