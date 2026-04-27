import React, { useEffect, useState, forwardRef, useImperativeHandle } from 'react';
import { fetchStatuses } from '../api';
import { Loader2, RefreshCw } from 'lucide-react';
import './StatusList.css';

const StatusList = forwardRef((props, ref) => {
    const [statuses, setStatuses] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState('');

    const loadStatuses = async () => {
        setLoading(true);
        setError('');
        try {
            const data = await fetchStatuses();
            setStatuses(data);
        } catch (err) {
            setError('Failed to load statuses.');
        } finally {
            setLoading(false);
        }
    };

    useEffect(() => {
        loadStatuses();
    }, []);

    useImperativeHandle(ref, () => ({
        refresh: loadStatuses
    }));

    return (
        <div className="status-card">
            <div className="status-header">
                <h2>Print Queue Status</h2>
                {/* Refresh button */}
            </div>

            {error && <div className="alert alert-error">{error}</div>}

            <div className="status-list">
                {statuses.length === 0 && !loading && (
                    <div className="empty-state">No ID cards in the system yet.</div>
                )}
                
                {statuses.map(item => (
                    <div key={item.id} className="status-item">
                        <div className="status-info">
                            <div className="status-name">{item.name}</div>
                            <div className="status-dept">{item.department}</div>
                        </div>
                        <div className="status-badge-container">
                            <span className={`status-badge ${item.status.toLowerCase()}`}>
                                {item.status}
                            </span>
                        </div>
                    </div>
                ))}
            </div>
        </div>
    );
});

export default StatusList;
