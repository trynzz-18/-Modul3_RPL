import mysql.connector


class Database:
    def __init__(self):
        self.host = "localhost"
        self.user = "root"
        self.password = ""
        self.database = "perpustakaan"
        self.conn = None

    def get_connection(self):
        try:
            self.conn = mysql.connector.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                database=self.database
            )

            print("Koneksi ke database berhasil!")
            return self.conn

        except mysql.connector.Error as err:
            print(f"Error koneksi database: {err}")
            return None