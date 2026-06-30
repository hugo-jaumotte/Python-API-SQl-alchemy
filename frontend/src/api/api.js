import axios from "axios";
// Connection between frontend and backend
const api = axios.create({
  baseURL: "https://focus-api-xcks.onrender.com",
  withCredentials: true
});

export default api;