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
              <v-card class="px-4">
                <v-card-text>
                  <v-form ref="loginForm" v-model="loginFormValid">
                    <v-row>
                      <v-col cols="12">
                        <v-text-field
                          v-model="loginDetails.username"
                          :rules="[rules.required]"
                          label="Username"
                          required
                          :error-messages="fieldErrors.username"
                          @input="delete fieldErrors.username"
                        ></v-text-field>
                      </v-col>
                      <v-col cols="12">
                        <v-text-field
                          v-model="loginDetails.password"
                          :append-icon="show1 ? 'eye' : 'eye-off'"
                          :rules="[rules.required]"
                          :type="show1 ? 'text' : 'password'"
                          name="input-10-1"
                          label="Password"
                          hint="At least 8 characters"
                          counter
                          @click:append="show1 = !show1"
                        ></v-text-field>
                      </v-col>
                      <v-col class="d-flex" cols="12" sm="6" xsm="12"> </v-col>
                      <v-spacer></v-spacer>
                      <v-col class="d-flex" cols="12" sm="3" xsm="12" align-end>
                        <v-btn
                          x-large
                          block
                          :disabled="!loginFormValid"
                          color="success"
                          @click="submitLoginForm()"
                        >
                          Login
                        </v-btn>
                      </v-col>
                    </v-row>
                  </v-form>
                </v-card-text>
              </v-card>
            </v-tab-item>
            <v-tab-item>
              <v-card class="px-4">
                <v-card-text>
                  <v-form ref="registerForm" v-model="signupFormValid">
                    <v-row>
                      <v-col cols="12" sm="6" md="6">
                        <v-text-field
                          v-model="userSignupDetails.first_name"
                          :rules="[rules.required]"
                          label="First Name"
                          maxlength="20"
                          required
                          :error-messages="fieldErrors.first_name"
                          @input="delete fieldErrors.first_name"
                        ></v-text-field>
                      </v-col>
                      <v-col cols="12" sm="6" md="6">
                        <v-text-field
                          v-model="userSignupDetails.last_name"
                          :rules="[rules.required]"
                          label="Last Name"
                          maxlength="20"
                          required
                          :error-messages="fieldErrors.last_name"
                          @input="delete fieldErrors.last_name"
                        ></v-text-field>
                      </v-col>
                      <v-col cols="12">
                        <v-text-field
                          v-model="userSignupDetails.username"
                          :rules="[rules.required]"
                          label="Username"
                          maxlength="20"
                          required
                          :error-messages="fieldErrors.username"
                          @input="delete fieldErrors.username"
                        ></v-text-field>
                      </v-col>
                      <v-col cols="12">
                        <v-text-field
                          v-model="userSignupDetails.email"
                          :rules="emailRules"
                          label="E-mail"
                          required
                          :error-messages="fieldErrors.email"
                          @input="delete fieldErrors.email"
                        ></v-text-field>
                      </v-col>
                      <v-col cols="12">
                        <v-text-field
                          v-model="userSignupDetails.password"
                          :append-icon="show1 ? 'mdi-eye' : 'mdi-eye-off'"
                          :rules="[rules.required, rules.min]"
                          :type="show1 ? 'text' : 'password'"
                          name="input-10-1"
                          label="Password"
                          hint="At least 8 characters"
                          counter
                          @click:append="show1 = !show1"
                          :error-messages="fieldErrors.password"
                          @input="delete fieldErrors.password"
                        ></v-text-field>
                      </v-col>
                      <v-col cols="12">
                        <v-text-field
                          block
                          v-model="userSignupDetails.verify"
                          :append-icon="show1 ? 'mdi-eye' : 'mdi-eye-off'"
                          :rules="[rules.required, passwordMatch]"
                          :type="show1 ? 'text' : 'password'"
                          name="input-10-1"
                          label="Confirm Password"
                          counter
                          @click:append="show1 = !show1"
                        ></v-text-field>
                      </v-col>
                      <v-spacer></v-spacer>
                      <v-col class="d-flex ml-auto" cols="12" sm="3" xsm="12">
                        <v-btn
                          x-large
                          block
                          :disabled="!signupFormValid"
                          color="success"
                          @click="submit()"
                          >Register</v-btn
                        >
                      </v-col>
                    </v-row>
                  </v-form>
                </v-card-text>
              </v-card>
            </v-tab-item>
          </v-tabs>
        </div>
      </v-dialog>
    </v-app>
  </div>
</template>

<script>
import { setDataInLocalStorage } from "@/utils/functions";
export default {
  name: "The-Landing-Comp",
  data() {
    return {
      dialog: true,
      tab: 0,
      tabs: [
        { name: "Login", icon: "mdi-account" },
        { name: "Register", icon: "mdi-account-outline" },
      ],
      loginFormValid: true,
      signupFormValid: true,

      userSignupDetails: {},
      loginDetails: {},

      fieldErrors: {},

      emailRules: [
        (v) => !!v || "Required",
        (v) => /.+@.+\..+/.test(v) || "E-mail must be valid",
      ],

      show1: false,
      rules: {
        required: (value) => !!value || "Required.",
        min: (v) => (v && v.length >= 8) || "Min 8 characters",
      },
    };
  },
  computed: {
    passwordMatch() {
      return () =>
        this.userSignupDetails?.password === this.userSignupDetails?.verify ||
        "Password must match";
    },
  },
  methods: {
    submit() {
      this.$api.users
        .createUsers(this.userSignupDetails)
        .then((res) => {
          console.log(res.data);
          setDataInLocalStorage(res.data, "user_credentials");
          this.$router.push({
            path: "/auth/dashboard/",
          });
        })
        .catch((error) => {
          this.fieldErrors = error.data;
          console.error(error);
        });
    },
    submitLoginForm() {
      this.$api.users
        .userLogin(this.loginDetails)
        .then((res) => {
          setDataInLocalStorage(res.data, "user_credentials");
          this.$router.push({
            path: "/auth/dashboard/",
          });
        })
        .catch((err) => {
          console.error(err);
          this.fieldErrors = err.data;
          this.$bus.$emit("showToaster", {
            message:
              err.data?.message || "Unable to log in with provided credentials",
            color: "error",
          });
        });
    },
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
