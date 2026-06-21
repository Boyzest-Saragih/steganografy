# Delimiter: Penanda akhir dari pesan (16-bit)
DELIMITER = "1111111111111110"

def text_to_binary(text):
    # mengubah huruf ke angka ASCII lalu ke Biner 8 digit
    binary_msg = ''.join(format(ord(char), '08b') for char in text)
    
    # add delimiter di akhir biner pesan
    return binary_msg + DELIMITER

def binary_to_text(binary_string):

    chars = []
    
    # Looping 1 huruf = 8 bit/1 byte
    for i in range(0, len(binary_string), 8):
        # Ambil potongan 8 bit
        byte = binary_string[i:i+8]
        
        if len(byte) == 8:
            #  biner ke desimal ke huruf
            chars.append(chr(int(byte, 2)))
            
    return ''.join(chars)