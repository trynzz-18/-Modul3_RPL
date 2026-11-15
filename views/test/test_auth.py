
import hashlib
from unittest.mock import MagicMock

from models.user_model import UserModel


def buat_user_model_mock():
    """Membuat UserModel tanpa membuka koneksi database asli."""
    model = UserModel.__new__(UserModel)
    model.conn = MagicMock()
    return model


def test_hash_password_sha256():
    """Memastikan password di-hash menggunakan SHA-256."""
    model = buat_user_model_mock()

    password = "admin123"
    hasil = model.hash_password(password)

    expected = hashlib.sha256(password.encode("utf-8")).hexdigest()

    assert hasil == expected
    assert len(hasil) == 64


def test_hash_password_konsisten():
    """Memastikan password yang sama menghasilkan hash yang sama."""
    model = buat_user_model_mock()

    hash_pertama = model.hash_password("admin123")
    hash_kedua = model.hash_password("admin123")

    assert hash_pertama == hash_kedua


def test_login_berhasil():
    """Memastikan login berhasil ketika password sesuai."""
    model = buat_user_model_mock()

    password_hash = hashlib.sha256(
        "admin123".encode("utf-8")
    ).hexdigest()

    cursor = model.conn.cursor.return_value
    cursor.fetchone.return_value = {
        "id_user": 1,
        "username": "petugas",
        "password_hash": password_hash,
        "role": "admin"
    }

    hasil = model.login("petugas", "admin123")

    assert hasil is not None
    assert hasil["username"] == "petugas"
    assert hasil["role"] == "admin"


def test_login_password_salah():
    """Memastikan login ditolak ketika password salah."""
    model = buat_user_model_mock()

    password_hash = hashlib.sha256(
        "admin123".encode("utf-8")
    ).hexdigest()

    cursor = model.conn.cursor.return_value
    cursor.fetchone.return_value = {
        "id_user": 1,
        "username": "petugas",
        "password_hash": password_hash,
        "role": "admin"
    }

    hasil = model.login("petugas", "passwordsalah")

    assert hasil is None


def test_login_username_tidak_ditemukan():
    """Memastikan login ditolak jika username tidak ditemukan."""
    model = buat_user_model_mock()

    cursor = model.conn.cursor.return_value
    cursor.fetchone.return_value = None

    hasil = model.login("pengguna_tidak_ada", "admin123")

    assert hasil is None
