import { HashRouter, Routes, Route } from 'react-router-dom'
import './App.css'
import Home from './pages/home';
import Movies from './pages/movies';
import Friends from './pages/friends';
import Profile from './pages/profile';

const axios = axiosAPI.create({
  baseURL: baseURL
});

// Check if user is logged in.
(function() { 
let authToken = localStorage.getItem("JWT");
if (authToken === null) {
    // This means that there ISN'T JWT and no user is logged in.
    axios.defaults.headers.common.Authorization = null;
} else {
    // This means that there IS a JWT so someone must be logged in.
    axios.defaults.headers.common.Authorization = `Bearer ${authToken}`;
}
})();

function App() {
  return (
    <div>      
      <HashRouter>
        <Routes>
          <Route path="/" element={<Home/>} />
          <Route path="/movies" element={<Movies/>} />
          <Route path="/friends" element={<Friends/>} />
          <Route path="/profile" element={<Profile/>} />
        </Routes>
      </HashRouter>
    </div>
  );
}

export default App;
