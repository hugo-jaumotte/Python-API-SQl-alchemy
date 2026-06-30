import {register} from '../api/registration.api';
import { useState } from 'react';

import RegistrationFailed from '../components/Registration.failed';
import RegistrationSuccessful from '../components/Registration.succesful';

const Register = () => {
    const [username, setUsername] = useState("");
    const [email, setEmail] = useState("");
    const [password, setPassword] = useState("");
    const [confirmPassword, setConfirmPassword] = useState("");

    const [error, setError] = useState(false);
    const [success, setSuccess] = useState(false);

    const handleClick = async () => {
        if(username && email && password.length >= 8 && password === confirmPassword){
            try {
                await register({ username, email, password });
                setSuccess(true);
                setError(false);
            } catch (err) {
                console.error(err);
                setError(true);
                setSuccess(false);
            }
        } else {
            setError(true);
            setSuccess(false);
        }
        
    };
    return ( 
        <div className="register">
            <h2>Register</h2>
            <input 
                placeholder="username" 
                value={username} 
                onChange={(e) => setUsername(e.target.value)} 
            />
            <br />
            <input 
                placeholder="email" 
                type="email" 
                value={email} 
                onChange={(e) => setEmail(e.target.value)} 
            />
            <br />
            <input 
                placeholder="password" 
                type="password" 
                value={password} 
                onChange={(e) => setPassword(e.target.value)} 
            />
            <br />
            <input 
                placeholder="confirm password" 
                type="password" 
                value={confirmPassword} 
                onChange={(e) => setConfirmPassword(e.target.value)} 
            />
            <button onClick={handleClick}>Register</button>
            {error && <RegistrationFailed />}
            {success && <RegistrationSuccessful />}
        </div>
     );
}
 
export default Register;