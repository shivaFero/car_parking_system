<template>
  <div>
    <v-app class="app-background">
      <v-dialog v-model="dialog" persistent max-width="600px" min-width="360px">
        <div>
          <v-tabs
            v-model="tab"
            show-arrows
            background-color="deep-purple accent-4"
            icons-and-text
            dark
            grow
          >
            <v-tabs-slider color="purple darken-4"></v-tabs-slider>
            <v-tab v-for="(item, index) in tabs" :key="index">
              <v-icon large>{{ item.icon }}</v-icon>
              <div class="caption py-1">{{ item.name }}</div>
            </v-tab>
            <v-tab-item>
              <UserSignInForm />
            </v-tab-item>
            <v-tab-item>
              <UserSignupForm />
            </v-tab-item>
          </v-tabs>
        </div>
      </v-dialog>
    </v-app>
  </div>
</template>

<script>
import UserSignInForm from "@/components/users/UserSignInForm.vue";
import UserSignupForm from "@/components/users/UserSignupForm.vue";
export default {
  name: "The-Landing-Comp",
  components: {
    UserSignInForm,
    UserSignupForm,
  },
  data() {
    return {
      dialog: true,
      tab: 0,
      tabs: [
        { name: "Login", icon: "mdi-account" },
        { name: "Register", icon: "mdi-account-outline" },
      ],
    };
  },
};
</script>

<style>
.app-background {
  background-image: url("@/assets/car-parking-two.jpg") !important;
  background-repeat: no-repeat !important;
  background-size: 100% 100% !important;
}
</style>
