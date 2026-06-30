import { getSessions } from "../api/getSessions.api";
import { useEffect, useState } from "react";

// This page contains the list of all the previous pomodoro sessions done by the user

// Define how the sessioncaracteristics will be expressed
const formatDuration = (ms) => {
    const totalSeconds = Math.floor(ms / 1000);

    const hours = Math.floor(totalSeconds / 3600);
    const minutes = Math.floor((totalSeconds % 3600) / 60);
    const seconds = totalSeconds % 60;

    return `${hours.toString().padStart(2, "0")}:${minutes
        .toString()
        .padStart(2, "0")}:${seconds.toString().padStart(2, "0")}`;
};

// Loading of the sessions caracteritics form the data base
const Historic = () => {
    const [sessions, setSessions] = useState([]);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        const fetchSessions = async () => {
            try {
                const res = await getSessions();
                setSessions(res.data);
            } catch (error) {
                console.error("Error fetching sessions:", error);
            } finally {
                setLoading(false);
            }
        };

        fetchSessions();
    }, []);

    return (
        <div>
            <h2>Historic</h2>
            <p>Here you can see your past sessions and their details.</p>

            {loading ? (
                <p>Loading sessions...</p>
            ) : sessions.length === 0 ? (
                <p>No sessions yet.</p>
            ) : (
                <table>
                    <thead>
                        <tr>
                            <th>Title</th>
                            <th>Work time</th>
                            <th>Rest time</th>
                            <th>Total duration</th>
                            <th>Start</th>
                        </tr>
                    </thead>

                    <tbody>
                        {sessions.map((session) => {
                            const start = new Date(session.start_time);
                            const end = new Date(session.end_time);

                            const durationMs = end - start;

                            return (
                                <tr key={session.id}>
                                    <td>{session.title}</td>
                                    <td>{session.work_time} min</td>
                                    <td>{session.break_time} min</td>
                                    <td>{formatDuration(durationMs)}</td>
                                    <td>{start.toLocaleString()}</td>
                                </tr>
                            );
                        })}
                    </tbody>
                </table>
            )}
        </div>
    );
};

export default Historic;