import { dashboard } from "@/utils/urls";
import { errorHandler, responseHandler } from "@/utils/functions";

export default (axios) => ({
  getDashboardData(params = {}) {
    return new Promise((resolve, reject) => {
      axios
        .get(dashboard.statics, {
          params: params,
        })
        .then((res) => {
          resolve(responseHandler(res));
        })
        .catch((err) => {
          reject(errorHandler(err));
        });
    });
  },
});
