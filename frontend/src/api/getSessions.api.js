import api from "./api";

// Get the historic off one user (the one who is connected)
export const getSessions = () => {
  return api.get("/focus_sessions/");
}