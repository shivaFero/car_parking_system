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
  getUserDetails(id) {
    return new Promise((resolve, reject) => {
      axios
        .get(`${user.base}retrieve_or_update/${id}/`)
        .then((res) => {
          resolve(responseHandler(res));
        })
        .catch((err) => {
          reject(errorHandler(err));
        });
    });
  },
  updateUserDetails(payload) {
    return new Promise((resolve, reject) => {
      axios
        .patch(`${user.base}retrieve_or_update/${payload.id}/`, payload.data)
        .then((res) => {
          resolve(responseHandler(res));
        })
        .catch((err) => {
          reject(errorHandler(err));
        });
    });
  },
  userLogout(payload) {
    return new Promise((resolve, reject) => {
      axios
        .post(`${user.base}logout/`, payload)
        .then((res) => {
          resolve(responseHandler(res));
        })
        .catch((err) => {
          reject(errorHandler(err));
        });
    });
  },
});
