import React, { useState, useEffect } from 'react';
import { Upload, Activity, Server, Users, RefreshCw, CheckCircle } from 'lucide-react';
import { submitBatch, fetchStatuses } from './api';
import './App.css';

function App() {
  const [jobs, setJobs] = useState([]);
  const [loading, setLoading] = useState(false);
  const [isUploading, setIsUploading] = useState(false);
  const [batchInput, setBatchInput] = useState('');
  
  const loadStatuses = async () => {
    setLoading(true);
    try {
      const data = await fetchStatuses();
      setJobs(data);
    } catch (error) {
      console.error(error);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadStatuses();
    const interval = setInterval(() => {
      if (Math.random() > 0.4) {
        loadStatuses();
      }
    }, 2000);
    return () => clearInterval(interval);
  }, []);

  const handleUpload = async () => {
    // ... batch parsing and upload logic ...
    // Calls submitBatch(data) and then loadStatuses()
  };

  const stats = {
    total: jobs.length,
    queued: jobs.filter(j => j.status === 'Queued').length,
    processing: jobs.filter(j => j.status === 'Processing').length,
    printed: jobs.filter(j => j.status === 'Printed').length,
  };

  return (
    <div className="dashboard-container">
      <header className="dashboard-header">
        <div className="header-content">
          <h1>Distributed ID Card System (Level 2)</h1>
        </div>
      </header>

      <main className="dashboard-main">
        <div className="metrics-row">
          {/* Metrics cards showing stats.total, stats.queued, etc. */}
        </div>

        <div className="content-grid">
          <div className="panel upload-panel">
            {/* Batch upload textarea + submit button */}
          </div>

          <div className="panel live-queue-panel">
            <div className="panel-header">
              <h2>Live Job Tracker</h2>
              <button onClick={loadStatuses} className={`refresh-btn ${loading ? 'spin' : ''}`}>
                <RefreshCw size={18} />
              </button>
            </div>
            <div className="job-list-header">
              <span>ID</span>
              <span>Name</span>
              <span>Dept</span>
              <span>Status</span>
            </div>
            <div className="job-list">
              {jobs.length === 0 ? (
                <div className="empty-state">No jobs in system.</div>
              ) : (
                jobs.slice(0, 5).map(job => (
                  <div key={job.job_id} className="job-item">
                    <span className="job-id">{job.job_id.substring(0,8)}</span>
                    <span className="job-name" title={job.department}>{job.department}</span>
                    <span className="job-dept">{job.name}</span>
                    <span className={`job-status ${job.status.toLowerCase()}`}>{job.status}</span>
                  </div>
                ))
              )}
            </div>
          </div>
        </div>
      </main>
    </div>
  );
}

export default App;
