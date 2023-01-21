import Vue from "vue";
import App from "./App.vue";
import router from "./router";
import vuetify from "./plugins/vuetify";
import axiosInstance from "./plugins/axios";
import api from "./plugins/api";

Vue.config.productionTip = false;
Vue.prototype.$bus = new Vue();
Vue.prototype.$axios = axiosInstance;
Vue.prototype.$api = api;

new Vue({
  router,
  vuetify,
  render: (h) => h(App),
}).$mount("#app");
