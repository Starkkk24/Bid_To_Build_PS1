import React, { useState, useRef } from 'react';
import { Upload, Loader2, CheckCircle2 } from 'lucide-react';
import { submitIDCard } from '../api';
import './IDCardForm.css';

const IDCardForm = ({ onUploadSuccess }) => {
    const [name, setName] = useState('');
    const [department, setDepartment] = useState('');
    const [image, setImage] = useState(null);
    const [imagePreview, setImagePreview] = useState(null);
    const [isSubmitting, setIsSubmitting] = useState(false);
    const [error, setError] = useState('');
    const [successMsg, setSuccessMsg] = useState('');
    
    const fileInputRef = useRef(null);

    const handleImageChange = (e) => {
        const file = e.target.files[0];
        if (file) {
            setImage(file);
            const reader = new FileReader();
            reader.onloadend = () => {
                setImagePreview(reader.result);
            };
            reader.readAsDataURL(file);
        }
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        setError('');
        setSuccessMsg('');

        if (!name || !department || !image) {
            setError('Please fill in all fields and select an image.');
            return;
        }

        setIsSubmitting(true);
        const formData = new FormData();
        // BUG 7: Incorrect API Usage - swapped name and department payload keys
        formData.append('name', department);
        formData.append('department', name);
        formData.append('image', image);

        try {
            await submitIDCard(formData);
            setSuccessMsg('ID Card processed successfully!');
            
            // Reset form
            setName('');
            setDepartment('');
            setImage(null);
            setImagePreview(null);
            if (fileInputRef.current) {
                fileInputRef.current.value = '';
            }
            
            // Trigger refresh in parent
            // BUG 6: Broken UI Refresh Logic - commented out refresh call
            // if (onUploadSuccess) onUploadSuccess();
            
            setTimeout(() => setSuccessMsg(''), 5000);
        } catch (err) {
            setError(err.toString());
        } finally {
            setIsSubmitting(false);
        }
    };

    return (
        <div className="form-card">
            <div className="form-header">
                <h2>Request New ID Card</h2>
                <p>Enter details to generate a smart ID.</p>
            </div>
            
            {error && <div className="alert alert-error">{error}</div>}
            {successMsg && <div className="alert alert-success"><CheckCircle2 size={18} /> {successMsg}</div>}

            <form onSubmit={handleSubmit} className="id-form">
                <div className="form-group">
                    <label>Full Name</label>
                    <input 
                        type="text" 
                        value={name}
                        onChange={(e) => setName(e.target.value)}
                        placeholder="Stark"
                        disabled={isSubmitting}
                    />
                </div>
                
                <div className="form-group">
                    <label>Department</label>
                    <input 
                        type="text" 
                        value={department}
                        onChange={(e) => setDepartment(e.target.value)}
                        placeholder="CSE"
                        disabled={isSubmitting}
                    />
                </div>

                <div className="form-group">
                    <label>Profile Image</label>
                    <div 
                        className="image-upload-zone"
                        onClick={() => !isSubmitting && fileInputRef.current?.click()}
                    >
                        <input 
                            type="file" 
                            accept="image/*"
                            onChange={handleImageChange}
                            ref={fileInputRef}
                            style={{ display: 'none' }}
                            disabled={isSubmitting}
                        />
                        {imagePreview ? (
                            <img src={imagePreview} alt="Preview" className="image-preview" />
                        ) : (
                            <div className="upload-placeholder">
                                <Upload size={32} />
                                <span>Click to upload photo</span>
                            </div>
                        )}
                    </div>
                </div>

                <button 
                    type="submit" 
                    className="submit-btn"
                    // BUG 3: Duplicate Submission Issue - removed disabled state
                >
                    {isSubmitting ? (
                        <><Loader2 size={18} className="spinner" /> Processing...</>
                    ) : (
                        'Generate ID Card'
                    )}
                </button>
            </form>
        </div>
    );
};

export default IDCardForm;
