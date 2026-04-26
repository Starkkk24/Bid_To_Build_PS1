import os
import uuid
import json
import sqlite3
from flask import Flask, request, jsonify
from flask_cors import CORS
import redis

app = Flask(__name__)
CORS(app)

REDIS_URL = os.getenv('REDIS_URL', 'redis://localhost:6379/0')
DB_PATH = os.getenv('DB_PATH', '../shared/database.db')

queue = redis.Redis.from_url(REDIS_URL)

def init_db():
    conn = sqlite3.connect(DB_PATH, timeout=10)
    c = conn.cursor()
    c.execute("""
    CREATE TABLE IF NOT EXISTS jobs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        job_id TEXT UNIQUE,
        name TEXT,
        department TEXT,
        status TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)
    conn.commit()
    conn.close()

# Initialize DB on start
init_db()

def get_db_connection():
    conn = sqlite3.connect(DB_PATH, timeout=10)
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/api/batch', methods=['POST'])
def submit_batch():
    data = request.json
    if not data or not isinstance(data, list):
        return jsonify({"error": "Invalid batch payload. Must be a list of objects."}), 400

    conn = get_db_connection()
    c = conn.cursor()
    
    jobs = []
    # Insert all records synchronously first to ensure they exist before workers pick them up
    for item in data:
        job_id = str(uuid.uuid4())
        name = item.get('name', 'Unknown')
        department = item.get('department', 'Unknown')
        
        c.execute(
            "INSERT INTO jobs (job_id, name, department, status) VALUES (?, ?, ?, ?)",
            (job_id, name, department, 'Queued')
        )
        
        jobs.append({
            "job_id": job_id,
            "name": name,
            "department": department
        })
        
    conn.commit()
    conn.close()
    
    # Push all jobs to Redis queue
    for job in jobs:
        queue.rpush('id_card_jobs', json.dumps(job))
        
    return jsonify({
        "message": f"Successfully queued {len(jobs)} jobs.",
        "jobs": jobs
    }), 202

@app.route('/api/status', methods=['GET'])
def get_status():
    conn = get_db_connection()
    jobs = conn.execute("SELECT job_id, name, department, status, created_at FROM jobs ORDER BY id DESC").fetchall()
    conn.close()
    
    return jsonify([dict(job) for job in jobs]), 200

if __name__ == '__main__':
    # Listen on all interfaces so docker-compose port mapping works
    app.run(host='0.0.0.0', port=5001, debug=True)
