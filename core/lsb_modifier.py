import cv2
import random
from .crypto_utils import text_to_binary, binary_to_text, DELIMITER

def get_shuffled_indices(seed, max_val):
    """
    Fungsi untuk menghasilkan daftar indeks piksel acak berdasarkan sebuah kunci (seed).
    Kunci yang sama akan selalu menghasilkan pola acakan yang sama.
    """
    random.seed(seed)
    indices = list(range(max_val))
    random.shuffle(indices)
    return indices

def embed_message(cover_path, stego_path, message, secret_key):
    """
    Proses menyisipkan pesan ke dalam gambar.
    """
    # Baca gambar
    img = cv2.imread(cover_path)
    if img is None:
        raise ValueError("Gambar Cover tidak ditemukan! Pastikan path benar.")

    # Konversi pesan teks ke biner (sudah termasuk delimiter)
    binary_msg = text_to_binary(message)
    msg_len = len(binary_msg)

    # Ratakan matriks 3D menjadi array 1D agar gampang diakses lewat indeks
    flat_img = img.flatten()

    # Validasi kapasitas gambar
    if msg_len > len(flat_img):
        raise ValueError("Pesan terlalu panjang untuk kapasitas gambar ini!")

    # Bangkitkan urutan indeks acak menggunakan secret_key
    indices = get_shuffled_indices(secret_key, len(flat_img))

    # Looping sebanyak panjang bit pesan
    for i in range(msg_len):
        idx = indices[i] # Ambil posisi piksel acak
        bit_pesan = int(binary_msg[i]) # Ambil bit ke-i dari pesan
        
        # Eksekusi rumus Bitwise: Kosongkan LSB lalu sisipkan bit pesan
        flat_img[idx] = (flat_img[idx] & 254) | bit_pesan

    # Kembalikan bentuk array 1D ke dimensi matriks gambar semula (Tinggi x Lebar x RGB)
    stego_img = flat_img.reshape(img.shape)

    # Simpan hasil (harus format lossless seperti PNG)
    cv2.imwrite(stego_path, stego_img)
    return True

def extract_message(stego_path, secret_key):
    """
    Proses mengekstrak pesan dari gambar stego.
    """
    # Baca gambar stego
    img = cv2.imread(stego_path)
    if img is None:
        raise ValueError("Gambar Stego tidak ditemukan!")

    flat_img = img.flatten()

    # Bangkitkan urutan indeks acak yang sama persis dengan saat embedding
    indices = get_shuffled_indices(secret_key, len(flat_img))

    extracted_bits = ""
    
    # Baca bit dari piksel-piksel acak tersebut
    for idx in indices:
        # Eksekusi rumus Bitwise untuk menarik LSB
        bit = flat_img[idx] & 1
        extracted_bits += str(bit)

        # Cek apakah bagian ujung biner yang terkumpul cocok dengan DELIMITER
        if extracted_bits.endswith(DELIMITER):
            break

    # Hilangkan delimiter dari string biner yang didapat
    clean_bits = extracted_bits[:-len(DELIMITER)]
    
    # Konversi kembali biner ke teks
    return binary_to_text(clean_bits)