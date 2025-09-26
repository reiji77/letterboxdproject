import { Link } from 'react-router-dom';
import './Navbar.css'

export function Navbar() {
    return (
    <ul className="navbar">
        <Link to="/">
            <button>Home</button>
        </Link>
        <Link to="/movies">
            <button>Movies</button>
        </Link>
        <Link to="/friends">
            <button>Friends</button>
        </Link>
        <Link to="/profile">
            <button>Profile</button>
        </Link>
    </ul>)
}
