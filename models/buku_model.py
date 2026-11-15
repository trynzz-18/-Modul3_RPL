
from config.database import Database


class BukuModel:

    def __init__(self):
        self.db = Database()
        self.conn = self.db.get_connection()
        self.table_name = "buku"

    # =====================================
    # MENAMPILKAN DATA BUKU AKTIF
    # =====================================

    def get_all_buku(self):

        if not self.conn:
            raise Exception("Koneksi database tidak tersedia!")

        cursor = None

        try:
            cursor = self.conn.cursor(dictionary=True)

            query = """
                SELECT id_buku, judul, pengarang, penerbit, tahun_terbit
                FROM buku
                WHERE is_deleted = 0
                ORDER BY id_buku ASC
            """

            cursor.execute(query)

            return cursor.fetchall()

        except Exception as e:
            raise Exception(f"Gagal mengambil data buku: {e}")

        finally:
            if cursor:
                cursor.close()

    # =====================================
    # MENAMBAHKAN DATA BUKU
    # =====================================

    def create_buku(self, judul, pengarang, penerbit, tahun_terbit):

        if not self.conn:
            raise Exception("Koneksi database tidak tersedia!")

        cursor = None

        try:
            cursor = self.conn.cursor()

            query = """
                INSERT INTO buku
                (judul, pengarang, penerbit, tahun_terbit, is_deleted)
                VALUES (%s, %s, %s, %s, 0)
            """

            cursor.execute(
                query,
                (judul, pengarang, penerbit, tahun_terbit)
            )

            self.conn.commit()

            return cursor.rowcount > 0

        except Exception as e:
            self.conn.rollback()
            raise Exception(f"Gagal menyimpan data buku: {e}")

        finally:
            if cursor:
                cursor.close()

    # =====================================
    # MEMPERBARUI DATA BUKU
    # =====================================

    def update_buku(self, id_buku, judul, pengarang, tahun_terbit):

        if not self.conn:
            raise Exception("Koneksi database tidak tersedia!")

        cursor = None

        try:
            cursor = self.conn.cursor()

            query = """
                UPDATE buku
                SET judul = %s,
                    pengarang = %s,
                    tahun_terbit = %s
                WHERE id_buku = %s
                AND is_deleted = 0
            """

            cursor.execute(
                query,
                (judul, pengarang, tahun_terbit, id_buku)
            )

            self.conn.commit()

            # Memastikan buku masih tersedia
            cursor.execute(
                """
                SELECT id_buku
                FROM buku
                WHERE id_buku = %s
                AND is_deleted = 0
                """,
                (id_buku,)
            )

            return cursor.fetchone() is not None

        except Exception as e:
            self.conn.rollback()
            raise Exception(f"Gagal memperbarui data buku: {e}")

        finally:
            if cursor:
                cursor.close()

    # =====================================
    # MENGHAPUS DATA BUKU (SOFT DELETE)
    # =====================================

    def delete_buku(self, id_buku):

        if not self.conn:
            raise Exception("Koneksi database tidak tersedia!")

        cursor = None

        try:
            cursor = self.conn.cursor()

            query = """
                UPDATE buku
                SET is_deleted = 1
                WHERE id_buku = %s
                AND is_deleted = 0
            """

            cursor.execute(query, (id_buku,))

            berhasil = cursor.rowcount > 0

            self.conn.commit()

            return berhasil

        except Exception as e:
            self.conn.rollback()
            raise Exception(f"Gagal menghapus data buku: {e}")

        finally:
            if cursor:
                cursor.close()
