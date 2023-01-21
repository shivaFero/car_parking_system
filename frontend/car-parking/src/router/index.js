import Vue from "vue";
import VueRouter from "vue-router";
import LandingPage from "@/views/index.vue";
import PageNotFound from "@/components/PageNotFound.vue";

import slotRouter from "./slot";

import DefaultLayout from "@/layouts/default.vue";

Vue.use(VueRouter);

const routes = [
  {
    path: "/",
    name: "home",
    component: LandingPage,
  },
  {
    path: "/auth",
    name: "auth",
    component: DefaultLayout,
    children: [...slotRouter],
    meta: {
      auth: true,
    },
  },
  {
    path: "*",
    name: "not-found",
    component: PageNotFound,
  },
];

const router = new VueRouter({
  mode: "history",
  routes,
});

// For Check Route Auth
router.beforeEach((to, from, next) => {
  // Check Users are login or not
  if (to.matched.some((record) => record.meta.auth)) {
    if (!localStorage.getItem("user_credentials")) {
      next({ name: "home" });
    } else {
      next();
    }
  } else {
    next();
  }
});

export default router;
