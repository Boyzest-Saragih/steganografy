import cv2
import random
from .crypto_utils import text_to_binary, binary_to_text, DELIMITER

# pembuatan posisi pesan yang disisipkan 
def get_shuffled_idx(seed, max_val):
    random.seed(seed)
    idx = list(range(max_val))
    random.shuffle(idx)
    return idx

# penyisipan pesan ke gambar
def embed_message(cover_path, stego_path, message, secret_key):

    # read gambar
    img = cv2.imread(cover_path)

    # Konversi pesan ke biner
    binary_msg = text_to_binary(message)
    msg_len = len(binary_msg)

    # Ratakan matriks 3D menjadi array 1D agar gampang diakses lewat indeks
    flat_img = img.flatten()

    # Validasi kapasitas gambar
    if msg_len > len(flat_img):
        raise ValueError("Pesan terlalu panjang untuk kapasitas gambar ini!")

    # urutan indeks acak menggunakan secret_key
    idx = get_shuffled_idx(secret_key, len(flat_img))

    for i in range(msg_len):
        # Ambil posisi piksel acak
        tmp = idx[i]
        
        # Ambil bit ke-i dari pesan
        bit_pesan = int(binary_msg[i]) 
        
        # Eksekusi rumus Bitwise: Kosongkan LSB lalu sisipkan bit pesan
        flat_img[tmp] = (flat_img[tmp] & 254) | bit_pesan

    # Kembalikan array 1D ke dimensi matriks gambar semula
    stego_img = flat_img.reshape(img.shape)

    # Simpan hasil
    cv2.imwrite(stego_path, stego_img)
    return True

# ekstrak gambar hasil penyisipan
def extract_message(stego_path, secret_key):

    img = cv2.imread(stego_path)
    flat_img = img.flatten()

    # urutan indeks acak menggunakan secret_key yang sama saat proses penyispan
    idx = get_shuffled_idx(secret_key, len(flat_img))

    extracted_bits = ""
    
    # Baca bit dari piksel-piksel acak tersebut
    for i in idx:
        # Eksekusi rumus Bitwise untuk menarik LSB
        bit = flat_img[i] & 1
        extracted_bits += str(bit)

        # Cek apakah bagian ujung biner = DELIMITER
        if extracted_bits.endswith(DELIMITER):
            break

    # Hilangkan delimiter
    clean_bits = extracted_bits[:-len(DELIMITER)]
    
    # biner ke teks
    return binary_to_text(clean_bits)