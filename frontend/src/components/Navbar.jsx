import { Link } from 'react-router-dom';
import './Navbar.css'

export function Navbar() {
    return (
    <div className="navBar">
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
    </div> 
    )
}
