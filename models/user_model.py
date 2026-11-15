
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

        password_hash = hashlib.sha256(
            password.encode("utf-8")
        ).hexdigest()

        return password_hash

    # =====================================
    # VERIFIKASI LOGIN
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

            # Hash password yang dimasukkan pengguna
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
