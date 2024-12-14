from flask import Flask, request, jsonify
import os

app = Flask(__name__)

# Fungsi untuk membaca daftar key dari file
def load_keys():
    try:
        with open(os.path.join(os.path.dirname(__file__), '../keys.txt'), 'r') as file:
            keys = file.read().splitlines()  # Membaca file dan memisahkan per baris
            return keys
    except FileNotFoundError:
        return []

# Endpoint untuk verifikasi key
@app.route('/verify', methods=['POST'])
def verify_key():
    data = request.get_json()
    key = data.get('key')

    if not key:
        return jsonify({'status': 'error', 'message': 'Key tidak diberikan!'}), 400

    valid_keys = load_keys()

    if key in valid_keys:
        return jsonify({'status': 'success', 'message': 'Key valid!'}), 200
    else:
        return jsonify({'status': 'error', 'message': 'Key tidak valid!'}), 400

# Endpoint utama untuk tes
@app.route('/', methods=['GET'])
def home():
    return "API Verifikasi Key Aktif!"

# Ekspor app untuk Vercel
app = app
