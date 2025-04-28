from flask import Flask, request, jsonify, send_file, render_template
import os
import csv
import pytesseract
from werkzeug.utils import secure_filename
from ocr import extract_data_from_image

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads/'
app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg'}

# Tesseract OCRのパス設定
pytesseract.pytesseract.tesseract_cmd = (
    r"/opt/homebrew/bin/tesseract"  # macOS (Homebrew)
)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

@app.route('/')
def upload_form():
    return render_template('upload.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)
        extracted_data = extract_data_from_image(file_path)
        if not extracted_data:
            return jsonify({'error': 'No data extracted from image'}), 400
        csv_path = os.path.join(app.config['UPLOAD_FOLDER'], 'output.csv')
        with open(csv_path, 'w', newline='', encoding='utf-8') as csvfile:
            fieldnames = ['date', 'pt', 'name', 'namae']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(extracted_data)
        return jsonify({'data': extracted_data, 'csv': csv_path})
    return jsonify({'error': 'File type not allowed'}), 400

@app.route('/download/<filename>')
def download_file(filename):
    return send_file(os.path.join(app.config['UPLOAD_FOLDER'], filename), as_attachment=True)

if __name__ == '__main__':
    if not os.path.exists(app.config['UPLOAD_FOLDER']):
        os.makedirs(app.config['UPLOAD_FOLDER'])
    app.run(debug=True)
