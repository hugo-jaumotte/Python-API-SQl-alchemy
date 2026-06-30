import api from "./api";

// Register a new pomodoro session into the historic
export const postSession = (sessionData) => {
    return api.post("/focus_sessions/add", sessionData);
};