import api from "./api";

// Get the information of the logged user thanks to the cookie containing the token
export const getUser = () => {
  return api.get("/users/me");
};