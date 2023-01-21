import router from "../router";
import axios from "axios";

function authHeader() {
  let token = localStorage.getItem("token");
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
  console.log("env", process.env)
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
    }
    throw err;
  }
);

export default axiosInstance;
