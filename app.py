import os
import cv2
from flask import Flask, render_template, request, url_for
from werkzeug.utils import secure_filename

from core.lsb_modifier import embed_message, extract_message
from utils.metrics import calculate_psnr, calculate_mse

app = Flask(__name__)

app.config['UPLOAD_FOLDER'] = 'static/uploads'

# Pastikan folder uploads tersedia
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/embed', methods=['POST'])
def embed():
    if 'image' not in request.files:
        return "Tidak ada file gambar", 400
        
    file = request.files['image']
    message = request.form.get('message')
    key = request.form.get('key')
    
    if file.filename == '':
        return "File belum dipilih", 400
        
    filename = secure_filename(file.filename)
    name, _ = os.path.splitext(filename)
    
    # Path file cover dan hasil stego
    cover_path = os.path.join(app.config['UPLOAD_FOLDER'], f"cover_{name}.png")
    stego_path = os.path.join(app.config['UPLOAD_FOLDER'], f"stego_{name}.png")
    
    # Simpan gambar cover
    file.save(cover_path)
    
    try:
        # Jalankan fungsi embedding
        embed_message(cover_path, stego_path, message, key)
        
        # Hitung Metrics
        img_awal = cv2.imread(cover_path)
        img_stego = cv2.imread(stego_path)
        
        mse_value = calculate_mse(img_awal, img_stego)
        
        try:
            psnr_value = calculate_psnr(img_awal, img_stego)
        except Exception:
            psnr_value = calculate_psnr(mse_value)
            
        # URL untuk frontend mengambil gambar (karena di dalam folder static)
        cover_image_url = url_for('static', filename=f'uploads/cover_{name}.png')
        result_image_url = url_for('static', filename=f'uploads/stego_{name}.png')
        
        return render_template(
            'index.html', 
            embed_success=True, 
            cover_image=cover_image_url,    
            result_image=result_image_url,  
            mse=f"{mse_value:.4f}", 
            psnr=f"{psnr_value:.2f}",
            active_tab='embed'
        )
    except Exception as e:
        return f"Gagal Embedding: {str(e)}", 500

@app.route('/extract', methods=['POST'])
def extract():
    if 'image_ext' not in request.files:
        return "Tidak ada file gambar", 400
        
    file = request.files['image_ext']
    key = request.form.get('key_ext')
    
    if file.filename == '':
        return "File belum dipilih", 400
        
    filename = secure_filename(file.filename)
    stego_path = os.path.join(app.config['UPLOAD_FOLDER'], f"to_extract_{filename}")
    
    file.save(stego_path)
    
    try:
        pesan_ditemukan = extract_message(stego_path, key)
        
        return render_template(
            'index.html', 
            extract_success=True, 
            extracted_text=pesan_ditemukan, 
            active_tab='extract'
        )
    except Exception as e:
        return f"Gagal Extraction: {str(e)}", 500

if __name__ == '__main__':
    app.run(debug=True)