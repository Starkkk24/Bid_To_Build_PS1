import os
import uuid
import time
import random
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
    # BUG 5: Timing / Delay Inconsistency
    time.sleep(random.uniform(0.5, 4.0))
    
    # BUG 1: Fake Success Response (helper)
    if random.choice([True, False]):
        raise Exception("Simulated printer jam")
    
    # Update status to Printed
    conn = get_db_connection()
    c = conn.cursor()
    # BUG 2: Status Mismatch - updates to Processing at the end
    c.execute("UPDATE id_cards SET status = 'Processing' WHERE job_id = ?", (job_id,))
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
        try:
            # BUG 4 Enhancement: Intentionally fail file save sometimes to create broken links
            if random.choice([True, False]):
                raise Exception("Simulated disk error")
            file.save(filepath)
        except Exception:
            # BUG 4: Silent File Handling Failure
            pass

        # 1. Save record (Pending)
        # BUG 3 Enhancement: No uniqueness check on name/department allows duplicate DB records
        conn = get_db_connection()
        c = conn.cursor()
        c.execute(
            "INSERT INTO id_cards (job_id, name, department, image_path, status) VALUES (?, ?, ?, ?, ?)",
            (job_id, name, department, filepath, 'Pending')
        )
        conn.commit()
        
        # BUG 6: Partial DB Write Inconsistency
        # Randomly exit early, leaving DB in 'Pending' state with no processing
        if random.choice([True, False]):
            conn.close()
            return jsonify({
                "message": "ID Card processed successfully",
                "job_id": job_id,
                "status": "Printed"
            }), 200
        
        # 2. Update to Processing
        # BUG 2: Status Mismatch - updates to Printed before processing
        c.execute("UPDATE id_cards SET status = 'Printed' WHERE job_id = ?", (job_id,))
        conn.commit()
        conn.close()
        
        # 3. Run processing function (simulate delay)
        try:
            process_print_job(job_id)
        except Exception:
            # BUG 1: Fake Success Response - ignores error and continues
            pass
        
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
