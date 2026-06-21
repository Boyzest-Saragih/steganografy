import os
import cv2
from core.lsb_modifier import embed_message, extract_message
from utils.metrics import calculate_psnr, calculate_mse

def main():
    # 1. Persiapan Folder & Path
    os.makedirs("assets", exist_ok=True)
    cover_path = "assets/cover_image.png"
    stego_path = "assets/stego_image.png"
    
    if not os.path.exists(cover_path):
        return


    pesan_rahasia = "ayam ayam, kripto gacor"
    kunci_rahasia = "kunci_super_aman_123" 

    # 3. Proses Embedding
    try:
        embed_message(cover_path, stego_path, pesan_rahasia, kunci_rahasia)
        print(f"Citra stego disimpan di: {stego_path}")
    except Exception as e:
        print(f"Gagal Embedding: {e}")
        return

    print("PSNR")
    img_awal = cv2.imread(cover_path)
    img_stego = cv2.imread(stego_path)
    
    mse_value = calculate_mse(img_awal, img_stego)
    psnr_value = calculate_psnr(img_awal, img_stego)
    
    print(f" Nilai MSE  : {mse_value:.4f}")
    print(f" Nilai PSNR : {psnr_value:.2f} dB")
    
    if psnr_value > 40:
        print("Kualitas sangat baik")
    else:
        print("Terjadi banyak perubahan warna pada piksel")

    try:
        pesan_ditemukan = extract_message(stego_path, kunci_rahasia)
        print(f"PESAN DITEMUKAN: \n{pesan_ditemukan}")
    except Exception as e:
        print(f"Gagal Extraction: {e}")

if __name__ == "__main__":
    main()