import { Outlet } from "react-router-dom";
import { useEffect, useState } from "react";

import Navbar from "./components/Navbar";
import Timer from "./popup/Timer";

const STORAGE_KEY = "focus_timer";

const Layout = ({ user, setUser }) => {
    const [sessionKey, setSessionKey] = useState(null);
    const [showTimer, setShowTimer] = useState(false);

    /* ---------------- RESTORE TIMER ON NAVIGATION ---------------- */

    useEffect(() => {
        const saved = localStorage.getItem(STORAGE_KEY);

        if (saved) {
            const parsed = JSON.parse(saved);

            setSessionKey(parsed.startTime);
            setShowTimer(true);
        }
    }, []);

    return (
        <div>
            {/* NAVBAR GLOBAL */}
            <Navbar user={user} setUser={setUser} />

            {/* TIMER GLOBAL (persistant UI) */}
            {showTimer && sessionKey && (
                <Timer
                    key={sessionKey}
                    onStop={() => {
                        setShowTimer(false);
                        setSessionKey(null);
                    }}
                />
            )}

            {/* PAGES */}
            <div className="content">
                <Outlet
                    context={{
                        setShowTimer,
                        setSessionKey,
                    }}
                />
            </div>
        </div>
    );
};

export default Layout;