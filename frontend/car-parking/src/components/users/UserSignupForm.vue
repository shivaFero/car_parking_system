<template>
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
          <v-col cols="6">
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
          <v-col cols="6">
            <v-text-field
              v-model="userSignupDetails.contact_number"
              :rules="[rules.required, rules.contactMin]"
              label="contact_number"
              maxlength="12"
              required
              :error-messages="fieldErrors.contact_number"
              @input="delete fieldErrors.contact_number"
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
              :append-icon="showPassword ? 'mdi-eye' : 'mdi-eye-off'"
              :rules="formType == 'add' ? [rules.required, rules.min] : []"
              :type="showPassword ? 'text' : 'password'"
              name="input-10-1"
              label="Password"
              hint="At least 8 characters"
              counter
              @click:append="showPassword = !showPassword"
              :error-messages="fieldErrors.password"
              @input="delete fieldErrors.password"
            ></v-text-field>
          </v-col>
          <v-col cols="12">
            <v-text-field
              block
              v-model="userSignupDetails.confirm_password"
              :append-icon="showCnfPassword ? 'mdi-eye' : 'mdi-eye-off'"
              :rules="formType == 'add' ? [rules.required, passwordMatch] : []"
              :type="showCnfPassword ? 'text' : 'password'"
              name="input-10-1"
              label="Confirm Password"
              counter
              @click:append="showCnfPassword = !showCnfPassword"
              :error-messages="fieldErrors.confirm_password"
              @input="delete fieldErrors.confirm_password"
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
</template>

<script>
import { setDataInLocalStorage, getLoginUserDetails } from "@/utils/functions";
export default {
  props: {
    formType: {
      type: String,
      default: "add",
    },
  },
  data() {
    return {
      signupFormValid: true,
      userId: null,

      userSignupDetails: {},

      fieldErrors: {},

      emailRules: [
        (v) => !!v || "Required",
        (v) => /.+@.+\..+/.test(v) || "E-mail must be valid",
      ],
      showPassword: false,
      showCnfPassword: false,
      rules: {
        required: (value) => !!value || "Required.",
        min: (v) => (v && v.length >= 8) || "Min 8 characters",
        contactMin: (v) => (v && v.length >= 10) || "Min 10 characters",
      },
    };
  },
  computed: {
    passwordMatch() {
      return () =>
        this.userSignupDetails?.password === this.userSignupDetails?.confirm_password ||
        "Password must match";
    },
  },
  methods: {
    submit(payload = {}) {
      if (this.formType === "add") {
        this.$api.users
          .createUsers(this.userSignupDetails)
          .then((res) => {
            setDataInLocalStorage(res.data, "user_credentials");
            setDataInLocalStorage(res.data.token, "token");
            this.$router.push({
              path: "/auth/dashboard/",
            });
          })
          .catch((error) => {
            this.fieldErrors = error.data;
            console.error(error);
          });
      } else {
        payload = {
          ...payload,
          data: this.userSignupDetails,
          id: this.userId,
        };
        this.$api.users
          .updateUserDetails(payload)
          .then(() => {
            this.$emit("refresh-list");
            this.fieldErrors = {};
          })
          .catch((error) => {
            this.fieldErrors = error.data;
            console.error(error);
          });
      }
    },

    populateForm(id) {
      this.$api.users
        .getUserDetails(id)
        .then((res) => {
          this.userSignupDetails = res.data;
        })
        .catch((error) => {
          console.error(error);
        });
    },
  },
  mounted() {
    if (this.formType === "edit") {
      this.userId = getLoginUserDetails().id;
      this.populateForm(this.userId);
    }
  },
};
</script>

<style></style>
