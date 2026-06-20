# Delimiter: Penanda akhir dari pesan (16-bit)
# Bisa diganti karakternya, tapi pastikan unik dan tidak gampang ketik natural
DELIMITER = "1111111111111110"

def text_to_binary(text):
    """
    Mengubah teks (string) menjadi satu baris panjang string biner.
    Contoh: 'A' -> '01000001'
    """
    # ord(char) mengubah huruf ke angka ASCII
    # format(angka, '08b') mengubah angka ke biner dan memastikan selalu 8 digit
    binary_msg = ''.join(format(ord(char), '08b') for char in text)
    
    # Tambahkan delimiter di akhir biner pesan
    return binary_msg + DELIMITER

def binary_to_text(binary_string):
    """
    Mengubah kembali string biner panjang menjadi teks.
    """
    chars = []
    
    # Looping melompat setiap 8 karakter (karena 1 huruf = 8 bit/1 byte)
    for i in range(0, len(binary_string), 8):
        # Ambil potongan 8 bit
        byte = binary_string[i:i+8]
        
        # Pastikan potongannya utuh 8 bit sebelum dikonversi
        if len(byte) == 8:
            # int(byte, 2) mengubah biner ke desimal
            # chr() mengubah desimal kembali ke karakter huruf
            chars.append(chr(int(byte, 2)))
            
    # Gabungkan array karakter menjadi satu string utuh
    return ''.join(chars)