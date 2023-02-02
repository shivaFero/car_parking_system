import { slot } from "@/utils/urls";
import { errorHandler, responseHandler } from "@/utils/functions";

export default (axios) => ({
  getSlotBookingList(params = {}) {
    return new Promise((resolve, reject) => {
      axios
        .get(slot.slotBooking, {
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
  addSlotBooking(data) {
    return new Promise((resolve, reject) => {
      axios
        .post(slot.slotBooking, data)
        .then((res) => {
          resolve(responseHandler(res));
        })
        .catch((err) => {
          reject(errorHandler(err));
        });
    });
  },

  getSlotBookingOptions() {
    return new Promise((resolve, reject) => {
      axios
        .options(`${slot.slotBooking}`)
        .then((res) => {
          resolve(responseHandler(res));
        })
        .catch((err) => {
          reject(errorHandler(err));
        });
    });
  },
  collectPayment(data) {
    return new Promise((resolve, reject) => {
      axios
        .post(`${slot.slotBooking}collect_payment/`, data)
        .then((res) => {
          resolve(responseHandler(res));
        })
        .catch((err) => {
          reject(errorHandler(err));
        });
    });
  },
  getBookingDetails(id) {
    return new Promise((resolve, reject) => {
      axios
        .get(`${slot.slotBooking}${id}/view/`)
        .then((res) => {
          resolve(responseHandler(res));
        })
        .catch((err) => {
          reject(errorHandler(err));
        });
    });
  },
  cancelSlotBooking(payload) {
    return new Promise((resolve, reject) => {
      axios
        .patch(`${slot.slotBooking}${payload.id}/cancel_booking/`, payload.data)
        .then((res) => {
          resolve(responseHandler(res));
        })
        .catch((err) => {
          reject(errorHandler(err));
        });
    });
  },
  getSlotBookingDetails(id) {
    return new Promise((resolve, reject) => {
      axios
        .get(`${slot.slotBooking}${id}/view/`)
        .then((res) => {
          resolve(responseHandler(res));
        })
        .catch((err) => {
          reject(errorHandler(err));
        });
    });
  },
  getSlotAvailability(params = {}) {
    return new Promise((resolve, reject) => {
      axios
        .get(`${slot.base}slot_availability/`, {
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
  getPaymentInfo(params = {}) {
    return new Promise((resolve, reject) => {
      axios
        .get(`${slot.base}payment_info/`, {
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
