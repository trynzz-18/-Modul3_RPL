from config.database import Database


class BukuModel:
    def __init__(self):
        self.db = Database()
        self.conn = self.db.get_connection()
        self.table_name = "buku"

    # Membaca seluruh data buku
    def get_all_buku(self):
        if self.conn:
            cursor = self.conn.cursor(dictionary=True)

            query = f"SELECT * FROM {self.table_name}"
            cursor.execute(query)

            result = cursor.fetchall()
            cursor.close()

            return result

        return []

    # Menambahkan data buku
    def create_buku(self, judul, pengarang, penerbit, tahun_terbit):
        if self.conn:
            cursor = self.conn.cursor()

            query = f"""
                INSERT INTO {self.table_name}
                (judul, pengarang, penerbit, tahun_terbit)
                VALUES (%s, %s, %s, %s)
            """

            cursor.execute(
                query,
                (judul, pengarang, penerbit, tahun_terbit)
            )

            self.conn.commit()
            berhasil = cursor.rowcount > 0
            cursor.close()

            return berhasil

        return False

    # Mengubah data buku
    def update_buku(self, id_buku, judul, penulis, tahun_terbit):
        if self.conn:
            cursor = self.conn.cursor()

            query = f"""
                UPDATE {self.table_name}
                SET judul = %s,
                    pengarang = %s,
                    tahun_terbit = %s
                WHERE id_buku = %s
            """

            cursor.execute(
                query,
                (judul, penulis, tahun_terbit, id_buku)
            )

            self.conn.commit()
            berhasil = cursor.rowcount > 0
            cursor.close()

            return berhasil

        return False

    # Menghapus data buku
    def delete_buku(self, id_buku):
        if self.conn:
            cursor = self.conn.cursor()

            query = f"""
                DELETE FROM {self.table_name}
                WHERE id_buku = %s
            """

            cursor.execute(query, (id_buku,))
            self.conn.commit()

            berhasil = cursor.rowcount > 0
            cursor.close()

            return berhasil

        return False
