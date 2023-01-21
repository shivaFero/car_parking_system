import { user } from "@/utils/urls";
import { errorHandler, responseHandler } from "@/utils/functions.js";

export default (axios) => ({
  createUsers(payload) {
    return new Promise((resolve, reject) => {
      axios
        .post(`${user.base}register/`, payload)
        .then((res) => {
          resolve(responseHandler(res));
        })
        .catch((err) => {
          reject(errorHandler(err));
        });
    });
  },
  userLogin(payload) {
    return new Promise((resolve, reject) => {
      axios
        .post(`${user.base}login/`, payload)
        .then((res) => {
          resolve(responseHandler(res));
        })
        .catch((err) => {
          reject(errorHandler(err));
        });
    });
  },
});
