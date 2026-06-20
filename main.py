import os
import cv2
from core.lsb_modifier import embed_message, extract_message
from utils.metrics import calculate_psnr, calculate_mse

def main():
    # 1. Persiapan Folder & Path
    os.makedirs("assets", exist_ok=True)
    cover_path = "assets/cover_image.png"
    stego_path = "assets/stego_image.png"
    
    print("=== PROGRAM STEGANOGRAFI SCATTERED LSB ===")
    
    # Cek apakah gambar cover tersedia
    if not os.path.exists(cover_path):
        print(f"[ERROR] Gambar tidak ditemukan!")
        print(f"Pastikan lu udah masukin gambar dengan nama 'cover_image.png' ke dalam folder 'assets/'.")
        return

    # 2. Parameter Input
    # Silakan ubah pesan dan password ini sesuai kebutuhan
    pesan_rahasia = "Halo, ini adalah uji coba pesan rahasia dengan Scattered LSB. Target PSNR di atas 40 dB!"
    kunci_rahasia = "kunci_super_aman_123" 

    # 3. Proses Embedding
    print("\n[1] Memulai Proses Embedding...")
    try:
        embed_message(cover_path, stego_path, pesan_rahasia, kunci_rahasia)
        print("    [+] Pesan berhasil disisipkan!")
        print(f"    [+] Citra stego disimpan di: {stego_path}")
    except Exception as e:
        print(f"    [-] Gagal Embedding: {e}")
        return

    # 4. Proses Evaluasi (Menghitung MSE & PSNR)
    print("\n[2] Menghitung Kualitas Citra (Metrics)...")
    img_awal = cv2.imread(cover_path)
    img_stego = cv2.imread(stego_path)
    
    mse_value = calculate_mse(img_awal, img_stego)
    psnr_value = calculate_psnr(img_awal, img_stego)
    
    print(f"    [+] Nilai MSE  : {mse_value:.4f}")
    print(f"    [+] Nilai PSNR : {psnr_value:.2f} dB")
    
    if psnr_value > 40:
        print("    [!] Kesimpulan : Kualitas sangat baik (Visual tidak ada bedanya dengan gambar asli).")
    else:
        print("    [!] Kesimpulan : Terjadi banyak perubahan warna pada piksel.")

    # 5. Proses Extraction
    print("\n[3] Memulai Proses Extraction...")
    try:
        pesan_ditemukan = extract_message(stego_path, kunci_rahasia)
        print("    [+] Ekstraksi selesai!")
        print("-" * 50)
        print(f"PESAN DITEMUKAN: \n{pesan_ditemukan}")
        print("-" * 50)
    except Exception as e:
        print(f"    [-] Gagal Extraction: {e}")

if __name__ == "__main__":
    main()