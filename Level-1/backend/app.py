import os
import uuid
import time
import sqlite3
from flask import Flask, request, jsonify
from flask_cors import CORS
from werkzeug.utils import secure_filename

app = Flask(__name__)
# Enable CORS so the React frontend can communicate with this API
CORS(app)

DB_FILE = 'database.db'
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def init_db():
    conn = sqlite3.connect(DB_FILE, timeout=10)
    c = conn.cursor()
    c.execute("""
    CREATE TABLE IF NOT EXISTS id_cards (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        job_id TEXT UNIQUE,
        name TEXT,
        department TEXT,
        image_path TEXT,
        status TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)
    conn.commit()
    conn.close()

# Initialize the database table when the app starts
init_db()

def get_db_connection():
    conn = sqlite3.connect(DB_FILE, timeout=10)
    conn.row_factory = sqlite3.Row
    return conn

def process_print_job(job_id):
    """Simulates the printing process synchronously."""
    # Simulate processing delay
    time.sleep(2)
    
    # Update status to Printed
    conn = get_db_connection()
    c = conn.cursor()
    c.execute("UPDATE id_cards SET status = 'Printed' WHERE job_id = ?", (job_id,))
    conn.commit()
    conn.close()

@app.route('/api/upload', methods=['POST'])
def upload_data():
    if 'image' not in request.files:
        return jsonify({"error": "No image provided"}), 400
    
    file = request.files['image']
    name = request.form.get('name')
    department = request.form.get('department')
    
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400
        
    if not name or not department:
        return jsonify({"error": "Name and department are required"}), 400

    if file:
        job_id = str(uuid.uuid4())
        filename = secure_filename(file.filename)
        unique_filename = f"{job_id}_{filename}"
        filepath = os.path.join(UPLOAD_FOLDER, unique_filename)
        
        # Save the actual file to disk (not base64)
        file.save(filepath)

        # 1. Save record (Pending)
        conn = get_db_connection()
        c = conn.cursor()
        c.execute(
            "INSERT INTO id_cards (job_id, name, department, image_path, status) VALUES (?, ?, ?, ?, ?)",
            (job_id, name, department, filepath, 'Pending')
        )
        conn.commit()
        
        # 2. Update to Processing
        c.execute("UPDATE id_cards SET status = 'Processing' WHERE job_id = ?", (job_id,))
        conn.commit()
        conn.close()
        
        # 3. Run processing function (simulate delay)
        process_print_job(job_id)
        
        return jsonify({
            "message": "ID Card processed successfully",
            "job_id": job_id,
            "status": "Printed"
        }), 200

@app.route('/api/status', methods=['GET'])
def get_status():
    conn = get_db_connection()
    # Fetch all ID cards ordered by newest first
    cards = conn.execute("SELECT id, job_id, name, department, image_path, status FROM id_cards ORDER BY id DESC").fetchall()
    conn.close()
    
    return jsonify([dict(card) for card in cards]), 200

if __name__ == '__main__':
    app.run(debug=True, port=5000)
