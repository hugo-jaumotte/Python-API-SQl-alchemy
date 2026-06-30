import React, { useState } from 'react';
import { requestPasswordReset } from "../api/reset.password";

const PasswordReset = () => {
    const [email, setEmail] = useState("");
    const [status, setStatus] = useState(null);

    const ForgotPasswordHandler = () => {
        if(email) {
            try {
                requestPasswordReset({ email: email })
                setStatus(true);
            }catch (error) {
                console.error("Error requesting password reset:", error);
                setStatus(false);
            }
        }
    }

    return ( 
        <div>
            <h1>Password Reset</h1>
            <p>Enter your email to receive a password reset link.</p>
            <input 
                type="email" 
                placeholder="Email" 
                value={email}
                onChange={(e) => setEmail(e.target.value)}
            />
            <button onClick={ForgotPasswordHandler}>Request Password Reset</button>
            {status === true && <p>Password reset email sent!</p>}
            {status === false && <p>Failed to send password reset email. Please try again.</p>}
        </div>
     );
}
 
export default PasswordReset;