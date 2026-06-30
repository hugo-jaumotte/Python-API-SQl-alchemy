import { useState } from "react";
import { useOutletContext } from "react-router-dom";

const STORAGE_KEY = "focus_timer";

const Session = () => {
    const { setShowTimer, setSessionKey } = useOutletContext();

    const minWork = 20;
    const minRest = 0;

    const [work, setWorkTime] = useState(25);
    const [rest, setRestTime] = useState(5);
    const [title, setTitle] = useState("");

    // Function that starts a new pomodoro session
    const handleClick = () => {
        const startTime = Date.now();

        localStorage.setItem(
            STORAGE_KEY,
            JSON.stringify({
                title,
                work,
                rest,
                startTime,
                phase: "work",
                beeped: [],
            })
        );

        setSessionKey(startTime);
        setShowTimer(true);
    };

    return (
        <div className="session">
            <label>Session Title</label>
            <input
                type="text"
                value={title}
                onChange={(e) => setTitle(e.target.value)}
            />

            <br />

            <input
                type="number"
                min={minWork}
                value={work}
                onChange={(e) => setWorkTime(Number(e.target.value))}
            />
            <label> Minutes de travail</label>

            <br />

            <input
                type="number"
                min={minRest}
                value={rest}
                onChange={(e) => setRestTime(Number(e.target.value))}
            />
            <label> Minutes de repos</label>

            <br />

            <button onClick={handleClick}>
                Start Session
            </button>
        </div>
    );
};

export default Session;