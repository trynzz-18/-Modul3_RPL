
import hashlib
import hmac

from config.database import Database


class UserModel:

    def __init__(self):
        self.db = Database()
        self.conn = self.db.get_connection()

    # =====================================
    # HASH PASSWORD SHA-256
    # =====================================

    def hash_password(self, password):

        return hashlib.sha256(
            password.encode("utf-8")
        ).hexdigest()

    # =====================================
    # REGISTRASI PENGGUNA BARU
    # =====================================

    def register_user(self, username, password):

        if not self.conn:
            raise Exception("Koneksi database tidak tersedia!")

        cursor = None

        try:
            cursor = self.conn.cursor()

            # Mengubah password menjadi hash
            password_hash = self.hash_password(password)

            # Role pendaftaran otomatis anggota
            query = """
                INSERT INTO users
                (username, password_hash, role)
                VALUES (%s, %s, %s)
            """

            cursor.execute(
                query,
                (username, password_hash, "anggota")
            )

            self.conn.commit()

            return cursor.rowcount > 0

        except Exception as e:

            self.conn.rollback()

            # MySQL error 1062 = username duplikat
            if getattr(e, "errno", None) == 1062:
                raise ValueError(
                    "Username sudah digunakan. Silakan pilih username lain."
                )

            raise Exception(f"Gagal melakukan registrasi: {e}")

        finally:
            if cursor:
                cursor.close()

    # =====================================
    # AUTENTIKASI LOGIN
    # =====================================

    def login(self, username, password):

        if not self.conn:
            raise Exception("Koneksi database tidak tersedia!")

        cursor = None

        try:
            cursor = self.conn.cursor(dictionary=True)

            query = """
                SELECT id_user, username, password_hash, role
                FROM users
                WHERE username = %s
            """

            cursor.execute(query, (username,))

            user = cursor.fetchone()

            if user is None:
                return None

            # Hash password yang dimasukkan
            input_hash = self.hash_password(password)

            # Membandingkan hash password
            if hmac.compare_digest(
                input_hash,
                user["password_hash"]
            ):

                return {
                    "id_user": user["id_user"],
                    "username": user["username"],
                    "role": user["role"]
                }

            return None

        except Exception as e:
            raise Exception(f"Gagal melakukan autentikasi: {e}")

        finally:
            if cursor:
                cursor.close()
