import { HashRouter, Routes, Route } from 'react-router-dom'
import './App.css'
import Home from './pages/home';
import Movies from './pages/movies';
import Friends from './pages/friends';
import Profile from './pages/profile';

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
