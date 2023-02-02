<template>
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
              :append-icon="showPassword ? 'mdi-eye' : 'mdi-eye-off'"
              :rules="[rules.required]"
              :type="showPassword ? 'text' : 'password'"
              name="input-10-1"
              label="Password"
              hint="At least 8 characters"
              counter
              @click:append="showPassword = !showPassword"
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
</template>

<script>
import { setDataInLocalStorage } from "@/utils/functions";
export default {
  data() {
    return {
      loginFormValid: true,
      loginDetails: {},
      fieldErrors: {},
      showPassword: false,

      // Form Rules
      rules: {
        required: (value) => !!value || "Required.",
        min: (v) => (v && v.length >= 8) || "Min 8 characters",
      },
    };
  },
  methods: {
    submitLoginForm() {
      this.$api.users
        .userLogin(this.loginDetails)
        .then((res) => {
          setDataInLocalStorage(res.data, "user_credentials");
          setDataInLocalStorage(res.data.token, "token");
          this.$router.push({
            path: "/auth/dashboard/",
          });
        })
        .catch((err) => {
          console.error(err);
          this.fieldErrors = err.data;
          this.$bus.$emit("showToaster", {
            message:
              err.data?.message ||
              "Unable to log in with provided credentials or once clear your cookies",
            color: "error",
          });
        });
    },
  },
};
</script>

<style></style>
