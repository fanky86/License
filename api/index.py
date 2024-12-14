from flask import Flask, request, jsonify, Response
import os
import json
import uuid

app = Flask(__name__)

# Lokasi file untuk menyimpan key
KEYS_FILE = os.path.join(os.path.dirname(__file__), '../keys.json')

# Fungsi untuk memuat key dari file
def load_keys():
    if not os.path.exists(KEYS_FILE):
        return {}
    with open(KEYS_FILE, 'r') as file:
        return json.load(file)

# Fungsi untuk menyimpan key ke file
def save_keys(keys):
    with open(KEYS_FILE, 'w') as file:
        json.dump(keys, file, indent=4)

# Endpoint untuk menghasilkan key baru
@app.route('/generate', methods=['POST'])
def generate_key():
    data = request.get_json()
    device_id = data.get('device_id')

    if not device_id:
        return jsonify({'status': 'error', 'message': 'Device ID tidak diberikan!'}), 400

    keys = load_keys()

    # Jika device sudah memiliki key, kembalikan key yang ada
    if device_id in keys:
        return jsonify({'status': 'success', 'key': keys[device_id]}), 200

    # Buat key baru
    new_key = str(uuid.uuid4())
    keys[device_id] = new_key
    save_keys(keys)

    return jsonify({'status': 'success', 'key': new_key}), 201

# Endpoint untuk verifikasi key
@app.route('/verify', methods=['POST'])
def verify_key():
    data = request.get_json()
    device_id = data.get('device_id')
    key = data.get('key')

    if not device_id or not key:
        return jsonify({'status': 'error', 'message': 'Device ID atau key tidak diberikan!'}), 400

    keys = load_keys()

    # Verifikasi key
    if keys.get(device_id) == key:
        return jsonify({'status': 'success', 'message': 'Key valid!'}), 200
    else:
        return jsonify({'status': 'error', 'message': 'Key tidak valid!'}), 400

# Endpoint utama untuk tes
@app.route('/', methods=['GET'])
def home():
    return Response("API Key Generation and Verification\nUsage:\n- Generate: /generate (POST)\n- Verify: /verify (POST)", mimetype='text/plain')

# Ekspor app untuk Vercel
app = app
