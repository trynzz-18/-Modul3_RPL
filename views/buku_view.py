
import tkinter as tk
from tkinter import ttk


class PlaceholderEntry(tk.Entry):

    def __init__(self, master, placeholder, **kwargs):
        super().__init__(master, **kwargs)

        self.placeholder = placeholder
        self.placeholder_active = True

        self.insert(0, placeholder)
        self.config(fg="#888888")

        self.bind("<FocusIn>", self.focus_in)
        self.bind("<FocusOut>", self.focus_out)

    def focus_in(self, event=None):

        if self.placeholder_active:
            self.delete(0, tk.END)
            self.config(fg="#222222")
            self.placeholder_active = False

    def focus_out(self, event=None):

        if not super().get().strip():
            self.show_placeholder()

    def show_placeholder(self):

        self.delete(0, tk.END)
        self.insert(0, self.placeholder)
        self.config(fg="#888888")
        self.placeholder_active = True

    def get(self):

        if self.placeholder_active:
            return ""

        return super().get()

    def set_value(self, value):

        self.delete(0, tk.END)

        if value is None or str(value) == "":
            self.show_placeholder()
        else:
            self.insert(0, str(value))
            self.config(fg="#222222")
            self.placeholder_active = False


class BukuView(tk.Tk):

    def __init__(self):

        super().__init__()

        self.title("Sistem Manajemen Perpustakaan - Mode: ADMIN")
        self.geometry("980x560")
        self.resizable(False, False)
        self.configure(bg="#f2f2f2")

        # =====================================
        # FRAME UTAMA
        # =====================================

        frame_utama = tk.Frame(
            self,
            bg="#f2f2f2"
        )

        frame_utama.pack(
            fill="both",
            expand=True,
            padx=4,
            pady=8
        )

        # =====================================
        # PANEL KIRI - FORM DATA BUKU
        # =====================================

        frame_form = tk.Frame(
            frame_utama,
            bg="#dedede",
            width=315
        )

        frame_form.pack(
            side="left",
            fill="y",
            padx=(0, 12)
        )

        frame_form.pack_propagate(False)

        tk.Label(
            frame_form,
            text="Form Data Buku",
            font=("Arial", 15, "bold"),
            bg="#dedede",
            fg="#333333"
        ).pack(pady=(22, 34))

        # Input judul
        self.entry_judul = PlaceholderEntry(
            frame_form,
            "Masukkan Judul Buku",
            font=("Arial", 11),
            relief="solid",
            bd=1
        )

        self.entry_judul.pack(
            fill="x",
            padx=18,
            pady=(0, 22),
            ipady=6
        )

        # Input penulis
        self.entry_penulis = PlaceholderEntry(
            frame_form,
            "Masukkan Nama Penulis",
            font=("Arial", 11),
            relief="solid",
            bd=1
        )

        self.entry_penulis.pack(
            fill="x",
            padx=18,
            pady=(0, 22),
            ipady=6
        )

        # Input tahun
        self.entry_tahun = PlaceholderEntry(
            frame_form,
            "Tahun Terbit (Misal: 2024)",
            font=("Arial", 11),
            relief="solid",
            bd=1
        )

        self.entry_tahun.pack(
            fill="x",
            padx=18,
            pady=(0, 28),
            ipady=6
        )

        # Tombol simpan
        self.btn_simpan = tk.Button(
            frame_form,
            text="Simpan Data",
            font=("Arial", 11),
            bg="green",
            fg="white",
            activebackground="#006400",
            activeforeground="white",
            relief="flat",
            cursor="hand2"
        )

        self.btn_simpan.pack(
            fill="x",
            padx=18,
            pady=(0, 12),
            ipady=7
        )

        # Tombol update
        self.btn_update = tk.Button(
            frame_form,
            text="Perbarui Data (Update)",
            font=("Arial", 11),
            bg="#24568b",
            fg="white",
            activebackground="#174574",
            activeforeground="white",
            relief="flat",
            cursor="hand2"
        )

        self.btn_update.pack(
            fill="x",
            padx=18,
            pady=(0, 12),
            ipady=7
        )

        # Tombol hapus
        self.btn_hapus = tk.Button(
            frame_form,
            text="Hapus Data (Delete)",
            font=("Arial", 11),
            bg="#c0392b",
            fg="white",
            activebackground="#922b21",
            activeforeground="white",
            relief="flat",
            cursor="hand2"
        )

        self.btn_hapus.pack(
            fill="x",
            padx=18,
            pady=(0, 12),
            ipady=7
        )

        # =====================================
        # PANEL KANAN - DAFTAR KOLEKSI BUKU
        # =====================================

        frame_daftar = tk.Frame(
            frame_utama,
            bg="#dedede"
        )

        frame_daftar.pack(
            side="left",
            fill="both",
            expand=True
        )

        tk.Label(
            frame_daftar,
            text="Daftar Koleksi Buku",
            font=("Arial", 15, "bold"),
            bg="#dedede",
            fg="#333333"
        ).pack(pady=(22, 34))

        # Frame tabel
        frame_tabel = tk.Frame(
            frame_daftar,
            bg="white"
        )

        frame_tabel.pack(
            fill="both",
            expand=True,
            padx=15,
            pady=(0, 15)
        )

        # Style tabel
        style = ttk.Style()
        style.theme_use("clam")

        style.configure(
            "Treeview",
            font=("Arial", 10),
            rowheight=26,
            background="white",
            fieldbackground="white"
        )

        style.configure(
            "Treeview.Heading",
            font=("Arial", 10),
            background="#eeeeee"
        )

        # Kolom tabel
        kolom = (
            "id_buku",
            "judul",
            "pengarang",
            "tahun_terbit"
        )

        self.tabel = ttk.Treeview(
            frame_tabel,
            columns=kolom,
            show="headings",
            selectmode="browse"
        )

        self.tabel.heading("id_buku", text="ID")
        self.tabel.heading("judul", text="Judul Buku")
        self.tabel.heading("pengarang", text="Penulis")
        self.tabel.heading("tahun_terbit", text="Tahun")

        self.tabel.column(
            "id_buku",
            width=65,
            anchor="center"
        )

        self.tabel.column(
            "judul",
            width=230,
            anchor="w"
        )

        self.tabel.column(
            "pengarang",
            width=200,
            anchor="w"
        )

        self.tabel.column(
            "tahun_terbit",
            width=100,
            anchor="center"
        )

        # Scrollbar
        scrollbar = ttk.Scrollbar(
            frame_tabel,
            orient="vertical",
            command=self.tabel.yview
        )

        self.tabel.configure(
            yscrollcommand=scrollbar.set
        )

        self.tabel.pack(
            side="left",
            fill="both",
            expand=True
        )

        scrollbar.pack(
            side="right",
            fill="y"
        )
