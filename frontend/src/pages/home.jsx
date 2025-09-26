import React, { useEffect } from 'react';
import { Navbar } from '../components/Navbar';
import { useState } from 'react';
import Login from '../components/Login';


const Home = () => {
    const [value, setValue] = useState({});
    useEffect(() => {
        fetchStatus();
    }, []);

    const fetchStatus = async () => {
        const response = await axios.get('http://localhost:5000/status', { withCredentials: true });
        data = await response.json()
        setStatus(data.status);
    };
    
    const renderFileUploadButton = () => (
        <div>
            <input
                type="file"
                id="fileInput"
                style={{ display: 'none' }}
                onChange={handleFileUpload}
            />
            <button onClick={handleButtonClick}>Upload File</button>
        </div>
    );
    const handleFileUpload = async (event) => {
        const file = event.target.files[0];
        const formData = new FormData();
        formData.append('file', file);

        try {
            const response = await fetch('http://localhost:5000/upload', {
                method: 'POST',
                body: formData,
            });

            if (response.ok) {
                alert('File uploaded successfully!');
            } else {
                alert('Failed to upload file.');
            }
        } catch (error) {
            console.error('Error uploading file:', error);
            alert('An error occurred while uploading the file.');
        }
    };
    if (status == 200) {
        return (
            <div>
                <Navbar/>
                {renderFileUploadButton()}
                <h1>Welcome to Letterboxd Project</h1>
                <p>Discover and share your favorite movies!</p>
            </div>
        );
    } else {
        return (
            <div>
                <Login/>
            </div>
            
        )
        
    }

};

export default Home;