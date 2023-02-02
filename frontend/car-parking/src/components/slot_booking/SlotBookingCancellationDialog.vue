<template>
  <v-dialog v-model="openDialog" scrollable width="700">
    <v-card>
      <v-card-title class="background primary text-white px-3 py-2">
        <span class="text-subtitle-1 text-uppercase"
          >{{ "Cancellation Remarks" }}
        </span>
        <v-spacer></v-spacer>
        <v-btn depressed color="white" icon small @click="openDialog = false">
          <v-icon>mdi-close</v-icon>
        </v-btn>
      </v-card-title>
      <v-card-text class="pa-0">
        <v-form
          ref="formRef"
          id="formRef"
          v-model="isValid"
          autocomplete="off"
          class="my-2 py-3"
        >
          <v-col cols="12">
            <v-text-field
              outlined
              hide-details="auto"
              label="Cancellation Remarks*"
              class="background-white"
              name="remarks"
              :rules="[
                (v) =>
                  (!!v && v.trim().length > 0) ||
                  'Cancellation Remarks is required',
              ]"
              :error-messages="formErrors.remarks"
              v-model="inputFormDetails.remarks"
              @input="delete formErrors.remarks"
            ></v-text-field>
          </v-col>
        </v-form>
      </v-card-text>

      <v-card-actions class="pb-3 d-flex justify-center">
        <v-btn
          :disabled="!isValid"
          @click.prevent="submitForm()"
          class="primary text-uppercase mr-3"
        >
          <span class="text-capitalize">Submit</span>
        </v-btn>
        <v-btn type="reset" class="primary text-uppercase" @click="resetForm()">
          <span class="text-capitalize">Reset</span>
        </v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>

<script>
export default {
  name: "Slot-Booking-Cancellation-Dialog",
  data() {
    return {
      isValid: false,
      inputFormDetails: {},
      formErrors: {},
      nonFieldError: [],
    };
  },
  props: {
    value: Boolean,
    slotId: {
      type: [Number, String],
      required: true,
    },
  },
  computed: {
    openDialog: {
      get() {
        return this.value;
      },
      set(value) {
        this.$emit("input", value);
      },
    },
  },
  methods: {
    resetForm() {
      this.$refs.formRef.reset();
    },
    closeDialog() {
      this.openDialog = false;
      this.inputFormDetails = {};
      this.formErrors = {};
      this.nonFieldError = [];
    },
    submitForm(params = {}) {
      params = {
        ...params,
        id: this.slotId,
        data: { ...this.inputFormDetails },
      };
      this.$api.slotBooking
        .cancelSlotBooking(params)
        .then(() => {
          this.$bus.$emit("showToaster", {
            message: "Booking Cancelled successfully",
            color: "success",
          });
          this.closeDialog();
          this.$emit("refresh-list")
        })
        .catch((err) => {
          console.error(err);
          if ("non_field_errors" in err.data) {
            this.nonFieldError = err.data.non_field_errors;
          }
          this.formErrors = err.data;
          this.$bus.$emit("showToaster", {
            message: err.message || "Something went wrong",
            color: "error",
          });
        });
    },
  },
};
</script>
