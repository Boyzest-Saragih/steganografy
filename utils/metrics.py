import numpy as np
import math

def calculate_mse(img_awal, img_stego):
    # Mengubah tipe matriks ke float 
    err = np.sum((img_awal.astype("float") - img_stego.astype("float")) ** 2)
    
    # Menghitung total baris x kolom x channel (RGB = 3)
    total_pixels = img_awal.shape[0] * img_awal.shape[1] * img_awal.shape[2]
    
    err /= float(total_pixels)
    
    return err

def calculate_psnr(img_awal, img_stego):
    mse = calculate_mse(img_awal, img_stego)
    
    # Kalau MSE 0, logikanya tidak ada noise sama sekali
    if mse == 0:
        return float('inf') 
    
    max_pixel = 255.0

    psnr = 10 * math.log10(max_pixel / math.sqrt(mse))
    
    return psnr