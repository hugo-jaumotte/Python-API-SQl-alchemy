import { useCallback, useEffect, useRef, useState } from "react";
import { postSession } from "../api/postSessions.api";

const PRE_BEEP_SECONDS = [3, 2, 1];
const WORK_CYCLES_LIMIT = 2;

const STORAGE_KEY = "focus_timer";

const Timer = ({ onStop }) => {
    const [isReady, setIsReady] = useState(false);
    const [error, setError] = useState(false);

    // Caracteristics of the new session
    const [session, setSession] = useState({
        title: "",
        work: 25,
        rest: 5,
    });

    const workTotal = (Number(session.work) || 25) * 60;
    const restTotal = (Number(session.rest) || 5) * 60;

    // State (working phase/break phase)
    const [phase, setPhase] = useState("work");
    const [timeLeft, setTimeLeft] = useState(workTotal);

    const startRef = useRef(null);
    const beepedRef = useRef(new Set());
    const audioCtxRef = useRef(null);

    const cycleLengthRef = useRef(workTotal + restTotal);

    useEffect(() => {
        cycleLengthRef.current = workTotal + restTotal;
    }, [workTotal, restTotal]);

    const CIRCUMFERENCE = 2 * Math.PI * 85;

    // Restore the timer state when the page is opened
    useEffect(() => {
    const saved = JSON.parse(localStorage.getItem(STORAGE_KEY));

        if (saved?.startTime) {
            setSession({
                title: saved.title ?? "",
                work: Number(saved.work) || 25,
                rest: Number(saved.rest) || 5,
            });

            startRef.current = saved.startTime;
            setPhase(saved.phase || "work");
            beepedRef.current = new Set(saved.beeped || []);
        } else {
            const startTime = Date.now();
            startRef.current = startTime;

            localStorage.setItem(
                STORAGE_KEY,
                JSON.stringify({
                    title: "",
                    work: 25,
                    rest: 5,
                    startTime,
                    phase: "work",
                    beeped: [],
                })
            );
        }

        setIsReady(true);
    }, []);

    // Beep when the stage is finished
    const beep = useCallback(() => {
        if (!audioCtxRef.current) {
            audioCtxRef.current = new (window.AudioContext ||
                window.webkitAudioContext)();
        }

        const ctx = audioCtxRef.current;

        const osc = ctx.createOscillator();
        const gain = ctx.createGain();

        osc.connect(gain);
        gain.connect(ctx.destination);

        osc.frequency.value = 880;
        osc.type = "sine";

        gain.gain.setValueAtTime(0.3, ctx.currentTime);
        gain.gain.exponentialRampToValueAtTime(
            0.001,
            ctx.currentTime + 0.2
        );

        osc.start();
        osc.stop(ctx.currentTime + 0.2);
    }, []);

    // Stop a session when the user click on the Stop Button
    const stopSession = useCallback(async () => {
        try {
            await postSession({
                title: session.title,
                work_time: session.work,
                break_time: session.rest,
                start_time: new Date(startRef.current).toISOString(),
            });

            localStorage.removeItem(STORAGE_KEY);

            onStop?.();
        } catch (err) {
            console.error(err);
            setError(true);
        }
    }, [onStop, session]);

    // Timer
    useEffect(() => {
        if (!isReady) return;

        const interval = setInterval(() => {
            const saved = JSON.parse(localStorage.getItem(STORAGE_KEY));
            const startTime = saved?.startTime ?? startRef.current;

            const elapsed = Math.floor((Date.now() - startTime) / 1000);

            const cycleLength = cycleLengthRef.current;
            const fullCycles = Math.floor(elapsed / cycleLength);

            if (fullCycles >= WORK_CYCLES_LIMIT) {
                stopSession();
                localStorage.removeItem(STORAGE_KEY);
                return;
            }

            const cycleTime = elapsed % cycleLength;
            const isWork = cycleTime < workTotal;

            const currentPhase = isWork ? "work" : "rest";

            const phaseElapsed = isWork
                ? cycleTime
                : cycleTime - workTotal;

            const duration = isWork ? workTotal : restTotal;
            const remaining = duration - phaseElapsed;

            setPhase(currentPhase);
            setTimeLeft(remaining);

            localStorage.setItem(
                STORAGE_KEY,
                JSON.stringify({
                    startTime,
                    phase: currentPhase,
                    beeped: Array.from(beepedRef.current),
                })
            );

            // Bell
            if (
                PRE_BEEP_SECONDS.includes(remaining) &&
                !beepedRef.current.has(
                    `${currentPhase}-${remaining}`
                )
            ) {
                beep();
                beepedRef.current.add(
                    `${currentPhase}-${remaining}`
                );
            }

            if (remaining <= 0) {
                beep();
                beepedRef.current.clear();
            }
        }, 250);

        return () => clearInterval(interval);
    }, [isReady, workTotal, restTotal, stopSession, beep]);

    //UI design
    const color = phase === "work" ? "#7F77DD" : "#1D9E75";

    const total = phase === "work" ? workTotal : restTotal;

    const pct = total ? timeLeft / total : 0;

    const offset = CIRCUMFERENCE * (1 - pct);

    const minutes = String(Math.floor(timeLeft / 60)).padStart(2, "0");
    const seconds = String(timeLeft % 60).padStart(2, "0");

    return (
        <div
            style={{
                display: "flex",
                flexDirection: "column",
                alignItems: "center",
                padding: "2rem",
                gap: "1.5rem",
            }}
        >
            <span
                style={{
                    fontSize: "13px",
                    fontWeight: "500",
                    padding: "4px 14px",
                    borderRadius: "99px",
                    textTransform: "uppercase",
                    background: phase === "work" ? "#EEEDFE" : "#E1F5EE",
                    color: phase === "work" ? "#3C3489" : "#085041",
                }}
            >
                {phase}
            </span>

            <svg width="200" height="200" viewBox="0 0 200 200">
                <circle
                    cx="100"
                    cy="100"
                    r="85"
                    fill="none"
                    stroke="#e5e5e5"
                    strokeWidth="8"
                />

                <circle
                    cx="100"
                    cy="100"
                    r="85"
                    fill="none"
                    stroke={color}
                    strokeWidth="8"
                    strokeDasharray={CIRCUMFERENCE}
                    strokeDashoffset={offset}
                    style={{
                        transform: "rotate(-90deg)",
                        transformOrigin: "center",
                    }}
                />

                <text
                    x="100"
                    y="105"
                    textAnchor="middle"
                    fontSize="36"
                    fill="#333"
                >
                    {`${minutes}:${seconds}`}
                </text>
            </svg>

            <div style={{ display: "flex", gap: "2rem" }}>
                <span>
                    Work <b>{session.work}</b> min
                </span>
                <span>
                    Rest <b>{session.rest}</b> min
                </span>
            </div>

            <button
                onClick={stopSession}
                style={{
                    background: "#e74c3c",
                    color: "white",
                }}
            >
                Stop
            </button>

            {error && (
                <p style={{ color: "red" }}>
                    Failed to save session.
                </p>
            )}
        </div>
    );
};

export default Timer;