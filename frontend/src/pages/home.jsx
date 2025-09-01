import React, { useEffect } from 'react';
import { Navbar } from '../components/navBar';
import { useState } from 'react';
import Login from '../components/Login';


const Home = () => {
    const [status, setStatus] = useState("");
{/*}
    useEffect(() => {
        fetchStatus();
    }, []);

    const fetchStatus = async () => {
        const response = await fetch('http://localhost:5000');
        data = await response.json()
        setStatus(data.status);
    };


    if (status == 200) {
        return (
            <div>
                <Navbar/>
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
*/}
return (
    <div>
        <Navbar/>
        <h1>Welcome to Letterboxd Project</h1>
        <p>Discover and share your favorite movies!</p>
    </div>
);

};

export default Home;