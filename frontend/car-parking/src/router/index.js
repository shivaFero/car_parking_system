import Vue from "vue";
import VueRouter from "vue-router";
import LandingPage from "../views/index.vue"
import Dashboard from "../views/dashboard/index.vue"

Vue.use(VueRouter);

const routes = [
  {
    path: "/",
    name: "home",
    component: LandingPage,
  },
  {
    path: "/dashboard",
    name: "dashboard",
    component: Dashboard,
  },
];

const router = new VueRouter({
  mode: "history",
  base: process.env.BASE_URL,
  routes,
});

export default router;
