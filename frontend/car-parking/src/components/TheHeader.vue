<template>
  <div>
    <v-app-bar
      :clipped-left="true"
      :clipped-right="true"
      fixed
      app
      color="#a372ed"
      dark
    >
      <v-toolbar-title class="d-flex">
        <img
          src="@/assets/download1.png"
          height="85px"
          width="150x"
          class="py-1 pa-1"
          light
        />
      </v-toolbar-title>

      <v-spacer></v-spacer>
      <h4>
        {{ loginUserDetails.first_name }} {{ loginUserDetails.last_name }}
      </h4>
      <v-menu bottom class="pr-10">
        <template v-slot:activator="{ on, attrs }">
          <v-btn icon v-bind="attrs" v-on="on">
            <v-avatar color="white" size="40">
              <span class="red--text text-h6"
                >{{ loginUserDetails?.first_name?.charAt(0) }}
                {{ loginUserDetails?.last_name?.charAt(0) }}</span
              >
            </v-avatar>
          </v-btn>
        </template>

        <v-list>
          <v-list-item @click="getUserDetails()">
            <v-icon>mdi-account-details</v-icon>
            <span class="pl-2 text-capitalize">{{ "View Profile" }}</span>
          </v-list-item>
          <v-list-item @click="editProfile = true">
            <v-icon>mdi-account-settings</v-icon>
            <span class="pl-2 text-capitalize">{{ "Edit Profile" }}</span>
          </v-list-item>
          <v-list-item @click="userLogout()">
            <v-icon>mdi-logout</v-icon>
            <span class="pl-2 text-capitalize">{{ "logout" }}</span>
          </v-list-item>
        </v-list>
      </v-menu>
    </v-app-bar>
    <v-col v-if="viewProfile">
      <BaseShowDetailsDialog
        v-model="viewProfile"
        title="User Profile Details"
        :show-details="userProfileDetails"
      />
    </v-col>
    <BaseFormDialog v-model="editProfile" title="edit user details">
      <template #flatFormContent>
        <UserSignupForm
          v-model="editProfile"
          form-type="edit"
          @refresh-list="editProfile = false"
        />
      </template>
    </BaseFormDialog>
  </div>
</template>

<script>
import BaseShowDetailsDialog from "@/components/base/BaseShowDetailsDialog.vue";
import UserSignupForm from "@/components/users/UserSignupForm.vue";
import { getLoginUserDetails } from "@/utils/functions";
import BaseFormDialog from "@/components/base/BaseFormDialog.vue";
export default {
  name: "The-Header",
  components: {
    BaseShowDetailsDialog,
    UserSignupForm,
    BaseFormDialog,
  },
  data() {
    return {
      viewProfile: false,
      editProfile: false,
      userProfileDetails: {},
      loginUserDetails: {},
    };
  },
  methods: {
    getUserDetails(id = null) {
      id = getLoginUserDetails().id;

      this.$api.users
        .getUserDetails(id)
        .then((res) => {
          this.viewProfile = true;
          this.userProfileDetails = res.data;
        })
        .catch((err) => {
          console.error(err);
          this.$bus.emit("showToaster", {
            message: err.message || "something went wrong",
            color: "error",
          });
        });
    },
    userLogout(payload = {}) {
      payload = {
        ...payload,
        id: getLoginUserDetails().id,
      };
      this.$api.users
        .userLogout(payload)
        .then((res) => {
          this.$bus.$emit("showToaster", {
            message: res.data || "You have successfully logged out",
            color: "success",
          });
          localStorage.clear();
          this.$router.push({
            path: "/",
          });
        })
        .catch((err) => {
          console.error(err);
          this.$bus.$emit("showToaster", {
            message: err.message || "Something went wrong",
            color: "error",
          });
        });
    },
  },
  mounted() {
    this.loginUserDetails = getLoginUserDetails();
  },
};
</script>
