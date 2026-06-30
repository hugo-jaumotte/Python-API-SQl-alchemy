import api from "./api";

// User's registration in case of a new account
export const register = (userData) => {
  return api.post("users/register", userData);
};