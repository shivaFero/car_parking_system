<template>
  <v-dialog v-model="openFormDialog" persistent scrollable width="50%">
    <v-card class="pa-4">
      <v-card-title
        class="text-lg-subtitle-1 text-xl-h6 text-uppercase font-weight-black primary--text pb-4"
      >
        <v-spacer />
      </v-card-title>
      <v-card-text v-if="openFormDialog" class="pa-5 pt-2">
        <v-alert v-if="nonFieldError.length" dense type="error">
          <v-list
            class="pa-0"
            dense
            style="background: inherit !important"
            v-for="(error, i) in nonFieldError"
            :key="i"
          >
            <v-list-item dense style="min-height: 20px !important">
              <span>{{ i }} .</span><span>{{ error }}</span>
            </v-list-item>
          </v-list>
        </v-alert>
        <v-form
          ref="paymentForm"
          id="paymentForm"
          v-model="isValid"
          autocomplete="off"
        >
          <v-row>
            <v-col cols="6">
              <v-text-field
                outlined
                hide-details="auto"
                label="Total Amount*"
                class="background-white"
                name="due_amount"
                disabled
                :value="slotBookingObject.total_amount"
                :error-messages="formErrors.due_amount"
                @input="delete formErrors.due_amount"
              ></v-text-field>
            </v-col>
            <v-col cols="6">
              <v-select
                hide-details="auto"
                label="select Payment Type"
                outlined
                :items="paymentTypes"
                item-text="display_name"
                item-value="value"
                v-model="inputFormDetails.payment_type"
                :error-messages="formErrors.payment_type"
                @change="delete formErrors.payment_type"
              ></v-select>
            </v-col>

            <v-col cols="6" class="pb-8">
              <v-text-field
                type="number"
                name="amount_collected"
                label="Enter Amount*"
                :rules="[
                  (val) => !!val || 'Amount is required',
                  (val) => val > 0 || 'Amount should be greater than 0',
                  (val) =>
                    (val && val >= slotBookingObject.total_amount) ||
                    `Amount can not be less than ${slotBookingObject.total_amount}`,
                ]"
                outlined
                hide-details="auto"
                v-model="inputFormDetails.amount_collected"
                :error-messages="formErrors.amount_collected"
                @input="delete formErrors.amount_collected"
              />
            </v-col>
            <v-col>
              <v-text-field
                outlined
                hide-details="auto"
                label="Transaction/Card Ref Number*"
                class="background-white"
                name="transaction_ref_no"
                v-model="inputFormDetails.transaction_ref_no"
                :rules="[
                  (v) =>
                    (!!v && v.trim().length > 0) ||
                    'Transaction/Card Ref Number is required',
                ]"
                :error-messages="formErrors.transaction_ref_no"
                @input="delete formErrors.transaction_ref_no"
              ></v-text-field>
            </v-col>
          </v-row>
        </v-form>
      </v-card-text>
      <v-card-actions class="pb-3 d-flex justify-center">
        <v-btn
          :disabled="!isValid"
          @click.prevent="submitForm()"
          class="primary text-uppercase mr-3"
        >
          <span class="text-capitalize"> Submit</span>
        </v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>

<script>
import moment from "moment";
import { paymentTypes } from "@/utils/choices";
export default {
  name: "Slot-Booking-Payment-Form",
  props: {
    value: Boolean,
    slotBookingObject: {
      type: Object,
      required: true,
    },
  },
  data() {
    return {
      paymentTypes,
      isValid: true,
      nonFieldError: [],
      inputFormDetails: {
        payment_type: "Cash",
      },
      formErrors: {},
      today: moment().format("YYYY-MM-DD"),
    };
  },
  computed: {
    openFormDialog: {
      get() {
        return this.value;
      },
      set(value) {
        this.$emit("input", value);
      },
    },
  },

  methods: {
    closeDialog() {
      this.openFormDialog = false;
      this.inputFormDetails = {};
      this.formErrors = {};
      this.nonFieldError = [];
    },

    submitForm() {
      let payload = {
        ...this.inputFormDetails,
        slot: this.slotBookingObject.id,
        due_amount: this.slotBookingObject.total_amount,
      };
      this.$api.slotBooking
        .collectPayment(payload)
        .then(() => {
          this.closeDialog();

          this.$bus.$emit("showToaster", {
            message: "Slot Booked Successfully",
            color: "success",
          });
          this.$emit("payment-collected");
        })
        .catch((err) => {
          console.error(err);
          if ("non_field_errors" in err.data) {
            this.nonFieldError = err.data.non_field_errors;
          }
          this.formErrors = err.data;
          this.$bus.$emit("showToaster", {
            message: err.message || "something went wrong",
            color: "error",
          });
        });
    },
  },
};
</script>

<style></style>
