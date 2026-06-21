import cv2
import random
from .crypto_utils import text_to_binary, binary_to_text, DELIMITER

# pembuatan posisi pesan yang disisipkan 
def get_shuffled_idx(seed, max_val):

    # pola pengacakan diseting sesuai dari kunci rahasia
    random.seed(seed)

    idx = list(range(max_val))

    # pengacakan sesuai pola seed
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
    print(img)
    flat_img = img.flatten()
    print(flat_img)

    # Validasi kapasitas gambar
    if msg_len > len(flat_img):
        raise ValueError("Pesan terlalu panjang untuk kapasitas gambar ini!")

    # urutan atau koordinat indeks acak yang berdasarkan secret_key
    idx = get_shuffled_idx(secret_key, len(flat_img))

    for i in range(msg_len):
        # Ambil posisi piksel idx
        tmp = idx[i]
        
        # Ambil bit ke-i dari pesan
        bit_pesan = int(binary_msg[i]) 
        
        # Eksekusi rumus Bitwise: Kosongkan LSB lalu sisipkan bit pesan
        '''
            and operator
            254 = 11111110
            cth : 10011011 & 11111110 = 10011010

            ini membuat 7 piksel pertama memepertahankan aslinya dan hanya mengubah paling kanan yakni yang paling kecil

            or operator
            hasil operator and tadi akan di or kan dengan bit pesan dengan posisi dibelakang bit asli
            cth : 10011010 | 00000001 = 10011011
        '''
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
        '''
            operasi and 1 berfungsi sebagai filter untuk mengetahui bit yang disisip sebelumnya
            cth: 10011011(bit yang disisip) & 00000001 = 00000001 = bit yang disisip = 1
                 10011010 & 00000001 = 00000000  = bit yang disisip = 0
        '''

        bit = flat_img[i] & 1

        # simpan hasil
        extracted_bits += str(bit)

        # Cek apakah bagian ujung biner = DELIMITER (menghentikan looping sepanjang pesan saja)
        if extracted_bits.endswith(DELIMITER):
            break

    # hapus delimiter
    clean_bits = extracted_bits[:-len(DELIMITER)]
    
    # biner ke teks
    return binary_to_text(clean_bits)