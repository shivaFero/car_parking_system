import Vue from "vue";
import VueRouter from "vue-router";
import LandingPage from "@/views/index.vue";
import Dashboard from "@/views/dashboard/index.vue";

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
    meta: {
      auth: true,
    },
  },
];

const router = new VueRouter({
  mode: "history",
  base: process.env.BASE_URL,
  routes,
});

// For Check Route Auth
router.beforeEach((to, from, next) => {
  // // Check Urls Match or not
  // if (to.path == from.path) {
  //   next();
  // } else {
  //   next({ name: "home" });
  // }

  // Check Users are login or not
  if (to.matched.some((record) => record.meta.auth)) {
    if (!localStorage.getItem("token")) {
      next({ name: "home" });
    } else {
      next();
    }
  } else {
    next();
  }
});

export default router;
