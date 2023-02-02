import router from "../router";
import axios from "axios";

function authHeader() {
  let token = JSON.parse(localStorage.getItem("token"));
  if (token) {
    return `token ${token}`;
  } else {
    return "";
  }
}

const axiosInstance = axios.create({
  baseURL: process.env.VUE_APP_BASE_URL,
});

axiosInstance.interceptors.request.use((config) => {
  let head = authHeader();
  if (head) {
    config.headers.Authorization = head;
  }
  return config;
});

axiosInstance.interceptors.response.use(
  (config) => {
    return config;
  },
  (err) => {
    if (
      err.response.status == 404 ||
      err.response.status == 403 ||
      err.response.status == 401
    ) {
      router.push({
        name: "not-found",
      });
      // #TODO: except 404 page show alert conformation dialog
    }
    throw err;
  }
);

export default axiosInstance;
