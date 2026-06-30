import { BrowserRouter, Routes, Route } from "react-router-dom";
import { useEffect, useState } from "react";

import Layout from "./Layout";

import { getUser } from "./api/getUser.api";

import Home from "./pages/Home";
import Login from "./pages/Login";
import Info from "./pages/Info";
import Register from "./pages/Register";
import PasswordReset from "./pages/PasswordReset";
import Historic from "./pages/Historic";
import EmailVerification from "./components/EmailVerification";
import PWDReset from "./components/PWDReset";

function App() {
    const [user, setUser] = useState(null);

    useEffect(() => {
        const initUser = async () => {
            try {
                const res = await getUser();
                setUser(res.data.username);
            } catch {
                setUser(null);
            }
        };

        initUser();
    }, []);

    return (
        <BrowserRouter>
            <Routes>
                <Route
                    path="/"
                    element={<Layout user={user} setUser={setUser} />}
                >
                    <Route index element={<Home />} />
                    <Route path="historic" element={<Historic />} />
                    <Route path="info" element={<Info />} />
                    <Route path="login" element={<Login user={user} setUser={setUser} />} />
                    <Route path="register" element={<Register />} />
                    <Route path="password-reset" element={<PasswordReset />} />
                    <Route path="password-reset/me" element={<PWDReset />} />
                    <Route path="verify-email" element={<EmailVerification />} />
                </Route>
            </Routes>
        </BrowserRouter>
    );
}

export default App;