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
    const interval = setInterval(loadStatuses, 2000); // Poll every 2 seconds
    return () => clearInterval(interval);
  }, []);

  const handleUpload = async () => {
    try {
      let data = JSON.parse(batchInput);
      if (!Array.isArray(data)) {
        data = [data];
      }
      setIsUploading(true);
      await submitBatch(data);
      setBatchInput('');
      await loadStatuses();
    } catch (error) {
      alert("Invalid JSON format or submission failed.\nExample: [{\"name\":\"Alice\",\"department\":\"HR\"}]");
    } finally {
      setIsUploading(false);
    }
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
          <p>Microservices Architecture &middot; Gateway &middot; Redis &middot; Workers</p>
        </div>
      </header>

      <main className="dashboard-main">
        {/* Top metrics row */}
        <div className="metrics-row">
          <div className="metric-card">
            <div className="metric-icon"><Users /></div>
            <div className="metric-info">
              <h3>Total Jobs</h3>
              <p>{stats.total}</p>
            </div>
          </div>
          <div className="metric-card warning">
            <div className="metric-icon"><Server /></div>
            <div className="metric-info">
              <h3>Queued</h3>
              <p>{stats.queued}</p>
            </div>
          </div>
          <div className="metric-card primary">
            <div className="metric-icon"><Activity /></div>
            <div className="metric-info">
              <h3>Processing</h3>
              <p>{stats.processing}</p>
            </div>
          </div>
          <div className="metric-card success">
            <div className="metric-icon"><CheckCircle /></div>
            <div className="metric-info">
              <h3>Printed</h3>
              <p>{stats.printed}</p>
            </div>
          </div>
        </div>

        <div className="content-grid">
          {/* Left panel: Batch Upload */}
          <div className="panel upload-panel">
            <h2>Batch Upload</h2>
            <p>Paste JSON array of users to simulate batch loading.</p>
            <textarea
              value={batchInput}
              onChange={(e) => setBatchInput(e.target.value)}
              placeholder={'[\n  { "name": "Stark", "department": "IOT" },\n  { "name": "Shreya", "department": "CSE" }\n]'}
              rows={8}
            />
            <button onClick={handleUpload} disabled={isUploading || !batchInput}>
              <Upload size={18} /> {isUploading ? 'Pushing to Queue...' : 'Submit Batch'}
            </button>
          </div>

          {/* Right panel: Live Queue */}
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
                jobs.map(job => (
                  <div key={job.job_id} className="job-item">
                    <span className="job-id">{job.job_id.substring(0,8)}</span>
                    <span className="job-name" title={job.name}>{job.name}</span>
                    <span className="job-dept">{job.department}</span>
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
