import React, { useState } from 'react';
import { resetPassword } from "../api/reset.password";
import { useNavigate } from 'react-router-dom';

const PWDReset = () => {
    const [pwd, setPwd] = useState('');
    const [confirmPwd, setConfirmPwd] = useState('');
    const [status, setStatus] = useState(null);
    const Navigate = useNavigate();

    const handlePasswordReset = async () => {
        if (pwd === confirmPwd && pwd.length > 8) {
            const urlParams = new URLSearchParams(window.location.search);
            const token = urlParams.get('token');

            try {
                await resetPassword({
                    token,
                    new_password: pwd
                });

                setStatus(true);
                Navigate("/");
            } catch (error) {
                console.error("Error resetting password:", error);
                setStatus(false);
            }
        } else {
            setStatus(false);
        }
    };

    return ( 
        <div>
            <h1>Password Reset</h1>
            <p>Enter your email to receive a password reset link.</p>
            <input type="password" placeholder="New Password" value={pwd} onChange={(e) => setPwd(e.target.value)} />
            <br />
            <input type="password" placeholder="Confirm New Password" value={confirmPwd} onChange={(e) => setConfirmPwd(e.target.value)} />
            <button onClick={handlePasswordReset}>Request Password Reset</button>
            {status === true && <p>Password reset successful!</p>}
            {status === false && <p>Passwords do not match or reset failed. Please try again.</p>}
        </div>
     );
}
 
export default PWDReset
;