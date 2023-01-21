import Dashboard from "@/views/dashboard/index.vue";
import SlotBooking from "@/views/slot_booking/index.vue";

const slots = [
  {
    path: "dashboard/",
    name: "dashboard",
    component: Dashboard,
  },
  {
    path: "slot_booking/",
    name: "slot_booking",
    component: SlotBooking,
  },
];

export default slots;
