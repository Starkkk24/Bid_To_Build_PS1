import os
import time
import json
import sqlite3
import redis

REDIS_URL = os.getenv('REDIS_URL', 'redis://localhost:6379/0')
DB_PATH = os.getenv('DB_PATH', '../shared/database.db')

# Use a connection pool to avoid creating a new redis client per job
pool = redis.ConnectionPool.from_url(REDIS_URL)
queue = redis.Redis(connection_pool=pool)

def get_db_connection():
    # Large timeout to avoid locking when multiple workers are running
    conn = sqlite3.connect(DB_PATH, timeout=20) 
    return conn

def update_job_status(job_id, status):
    conn = get_db_connection()
    c = conn.cursor()
    c.execute("UPDATE jobs SET status = ? WHERE job_id = ?", (status, job_id))
    conn.commit()
    conn.close()

def process_job(job_data):
    job_id = job_data['job_id']
    name = job_data['name']
    
    print(f"[{job_id}] Picked up job for {name}", flush=True)
    
    # Update status to Processing
    update_job_status(job_id, 'Processing')
    
    # Simulate work
    time.sleep(1)
    
    # Update status to Printed
    update_job_status(job_id, 'Printed')
    print(f"[{job_id}] Finished job for {name}", flush=True)

def worker_loop():
    print("Worker started. Waiting for jobs...", flush=True)
    while True:
        try:
            # BLPOP blocks until an item is available in the list
            # It returns a tuple (queue_name, item)
            _, raw_data = queue.blpop('id_card_jobs')
            job_data = json.loads(raw_data.decode('utf-8'))
            
            process_job(job_data)
        except Exception as e:
            print(f"Error processing job: {e}", flush=True)
            time.sleep(1)

if __name__ == "__main__":
    # Ensure database file exists/wait for gateway to init if needed
    time.sleep(2) 
    worker_loop()
