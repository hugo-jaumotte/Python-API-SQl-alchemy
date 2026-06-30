import api from "./api";

export const requestPasswordReset = (data) => {
  return api.post("/password-reset/request", data);
};

export const resetPassword = (data) => {
  return api.post("/password-reset/confirm", data);
};