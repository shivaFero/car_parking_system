import axiosInstance from "./axios";
import users from "@/services/users";

export default {
  users: users(axiosInstance),
};
