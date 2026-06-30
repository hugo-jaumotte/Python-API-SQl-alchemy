import { Link } from 'react-router-dom';
import { logout } from '../api/auth.api';

const Navbar = ({ user, setUser }) => {
    const handleLogout = () => {
        logout();
        setUser(null);
        
    };
    return ( 
        <nav className="navbar">
            <h1>Focus App</h1>
            <div className="links">
                <Link to="/">Home</Link>
                <Link to="/historic">Historic</Link>
                <Link to="/info">Info</Link>
                {!user && <Link to="/login" className="login">Login</Link>}
                {user && <Link to="/login" className="logout" onClick={handleLogout}>Logout</Link>}
                {user && <Link to="/profile" className="login">{user}</Link>}
            </div>
        </nav>
     );
}
 
export default Navbar;