import React, { useRef } from 'react';
import IDCardForm from './components/IDCardForm';
import StatusList from './components/StatusList';
import './App.css';

function App() {
  const statusListRef = useRef(null);

  const handleUploadSuccess = () => {
    if (statusListRef.current) {
      statusListRef.current.refresh();
    }
  };

  return (
    <div className="app-container">
      <header className="app-header">
        <h1>Smart ID Card System</h1>
      </header>

      <main className="app-main">
        <div className="left-panel">
            <IDCardForm onUploadSuccess={handleUploadSuccess} />
        </div>
        <div className="right-panel">
            <StatusList ref={statusListRef} />
        </div>
      </main>
    </div>
  );
}

export default App;
