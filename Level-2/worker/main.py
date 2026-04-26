import os
import time
import json
import sqlite3
import redis
import random

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
    # BUG 3: Stale Status Bug (DB Inconsistency)
    # Randomly skip the database update, leaving the old status cached in DB forever
    if random.random() < 0.3:
        return
        
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
    
    # BUG 4: Worker Crash Simulation (Partial Failure)
    # Crash AFTER marking as processing, effectively stranding the job
    if random.random() < 0.2:
        print(f"[{job_id}] CRITICAL WORKER CRASH! Execution halted.", flush=True)
        return
        
    # Simulate work
    time.sleep(1)
    
    # Update status to Printed
    update_job_status(job_id, 'Printed')
    print(f"[{job_id}] Finished job for {name}", flush=True)

def worker_loop():
    print("Worker started. Waiting for jobs...", flush=True)
    while True:
        try:
            # BUG 1: Duplicate Job Processing (Race Condition)
            # Read from top without popping. If multiple workers are running, they all read the SAME job
            raw_data = queue.lindex('id_card_jobs', 0)
            if not raw_data:
                time.sleep(1)
                continue
                
            job_data = json.loads(raw_data.decode('utf-8'))
            
            # BUG 2: Lost Jobs (Queue Drop)
            # Randomly pop the job and completely drop it without processing
            if random.random() < 0.2:
                print("Queue Drop: An item was lost from the queue.", flush=True)
                queue.lpop('id_card_jobs')
                continue
            
            process_job(job_data)
            
            # BUG 1 Continued: Pop the job AFTER processing. This creates the race condition window.
            queue.lpop('id_card_jobs')
        except Exception as e:
            print(f"Error processing job: {e}", flush=True)
            time.sleep(1)

if __name__ == "__main__":
    # Ensure database file exists/wait for gateway to init if needed
    time.sleep(2) 
    worker_loop()
