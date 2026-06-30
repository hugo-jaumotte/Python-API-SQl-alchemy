import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { Link } from 'react-router-dom';

import { login } from "../api/auth.api";
import { getUser } from "../api/getUser.api";

import ConnectionSuccesful from "../components/Connection.succesful";
import ConnectionFailed from "../components/Connection.failed";


const Login = ({ user, setUser }) => {
    const [username, setUsername] = useState("");
    const [password, setPassword] = useState("");
    const [status, setStatus] = useState(null);
    const navigate = useNavigate();

    const clickHandler = async () => {
        try {
            await login({ username, password });

            const userRes = await getUser();
            setUser(userRes.data.username);
            setStatus("success");
            navigate("/");
        } catch (err) {
            setUser(null);
            setStatus("failed");
            console.error(err);
        }
    };

    return (
        <div>
            <br />
            <input
                className="loginPage"
                placeholder="username"
                onChange={(e) => setUsername(e.target.value)}
            />
            <br />
            <input
                className="loginPage"
                type="password"
                placeholder="password"
                onChange={(e) => setPassword(e.target.value)}
            />
            <Link className="registerPage" to="/register">
                Register
            </Link>
            <Link className="registerPage" to="/password-reset">
                Forgot Password?
            </Link>
            <button className="loginPage" onClick={clickHandler}>
                Login
            </button>

            <p>
                This application uses HTTP-only cookies to manage authentication securely.
                These cookies are strictly necessary for user login, session management, and account verification.
            </p>
    
            {status === "success" && <ConnectionSuccesful />}
            {status === "failed" && <ConnectionFailed />}
        </div>
    );
};

export default Login;
