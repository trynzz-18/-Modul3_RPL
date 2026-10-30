
from unittest.mock import MagicMock, patch
from models.buku_model import BukuModel


def test_create_buku_berhasil():

    # Menginisialisasi Mock koneksi database
    mock_conn = MagicMock()
    mock_cursor = MagicMock()

    # Mengatur hasil operasi INSERT
    mock_cursor.rowcount = 1
    mock_conn.cursor.return_value = mock_cursor

    # Menggantikan koneksi database asli dengan Mock
    with patch("models.buku_model.Database") as mock_database:
        mock_database.return_value.get_connection.return_value = mock_conn

        # Membuat objek Model
        model = BukuModel()

    # Melakukan pengujian fungsi create_buku
    hasil = model.create_buku(
        "Buku Testing",
        "Penulis QA",
        "Penerbit QA",
        2026
    )

    # Memastikan hasil pengujian benar
    assert hasil is True

    # Memastikan perintah SQL dijalankan
    mock_cursor.execute.assert_called_once()

    # Memastikan perintah commit dijalankan
    mock_conn.commit.assert_called_once()
