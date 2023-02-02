import axiosInstance from "./axios";
import users from "@/services/users";
import slotBooking from "@/services/slot-booking";
import dashboard from "@/services/dashboard";

export default {
  users: users(axiosInstance),
  slotBooking: slotBooking(axiosInstance),
  dashboard: dashboard(axiosInstance),
};
