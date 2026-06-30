import api from "./api";

// Export of the roads linked to the user's login
export const login = (data) => {
  return api.post("/auth/login", data);
};

export const verifyEmail = (token) => {
  return api.get("/auth/verify-email", { params: { token } });
};

export const logout = () => {
  return api.post("/auth/logout");
}