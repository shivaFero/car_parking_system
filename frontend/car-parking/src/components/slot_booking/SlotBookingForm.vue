<template>
  <div>
    <v-dialog
      v-model="openFormDialog"
      persistent
      scrollable
      width="50%"
      @keydown.esc="closeDialog()"
    >
      <v-card class="pa-4">
        <v-card-title
          class="text-lg-subtitle-1 text-xl-h6 text-uppercase font-weight-black primary--text pb-4"
        >
          <v-spacer />
          <v-btn
            depressed
            text
            small
            icon
            class="primary-text"
            @click="closeDialog()"
          >
            <v-icon>mdi-close</v-icon>
          </v-btn>
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
            ref="slotBookingForm"
            id="slotBookingForm"
            v-model="isValid"
            autocomplete="off"
          >
            <v-row>
              <v-col cols="6">
                <v-text-field
                  outlined
                  hide-details="auto"
                  label="Vehicle Number*"
                  class="background-white"
                  name="vehicle_no"
                  :rules="[
                    (v) =>
                      (!!v && v.trim().length > 0) ||
                      'Vehicle Number is required',
                  ]"
                  :error-messages="formErrors.vehicle_no"
                  v-model="inputFormDetails.vehicle_no"
                  @input="delete formErrors.vehicle_no"
                ></v-text-field>
              </v-col>
              <v-col cols="6">
                <v-select
                  hide-details="auto"
                  label="Select Vehicle Type*"
                  outlined
                  :items="vehicleTypeList"
                  item-text="display_name"
                  item-value="value"
                  :rules="[(val) => !!val || 'Vehicle Type is required']"
                  v-model="inputFormDetails.vehicle_type"
                  :error-messages="formErrors.vehicle_type"
                  @change="delete formErrors.vehicle_type"
                ></v-select>
              </v-col>

              <v-col cols="12">
                <v-text-field
                  type="date"
                  name="booking_date"
                  label="Booking Date*"
                  :rules="[(val) => !!val || 'Booking date is required']"
                  outlined
                  hide-details="auto"
                  :min="today"
                  v-model="inputFormDetails.booking_date"
                  :error-messages="formErrors.booking_date"
                  @change="formErrors.booking_date = ''"
                  @input="formErrors.booking_date = ''"
                />
              </v-col>

              <!--  From Time and Time to Time section -->
              <v-col cols="6" class="mt-4">
                <v-text-field
                  v-model="inputFormDetails.from_time"
                  label="From Time*"
                  append-icon=""
                  type="time"
                  hide-details="auto"
                  outlined
                  :error-messages="formErrors.from_time"
                  :rules="[(v) => !!v || 'From time is required']"
                ></v-text-field>
              </v-col>
              <v-col cols="6" class="mt-4">
                <v-text-field
                  v-model="inputFormDetails.to_time"
                  label="To Time*"
                  append-icon=""
                  type="time"
                  hide-details="auto"
                  outlined
                  :error-messages="formErrors.to_time"
                  :rules="[(v) => !!v || 'To time  is required']"
                ></v-text-field>
              </v-col>
              <!-- From Time and Time to Time section -->
            </v-row>
          </v-form>
        </v-card-text>
        <v-card-actions class="pb-3 d-flex justify-center">
          <v-btn
            :disabled="!isValid"
            @click.prevent="submitForm()"
            class="primary text-uppercase mr-3"
          >
            <span class="text-capitalize">Proceed To Pay</span>
          </v-btn>
          <v-btn
            type="reset"
            class="primary text-uppercase"
            @click="resetForm()"
          >
            <span class="text-capitalize">Reset</span>
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </div>
</template>

<script>
import moment from "moment";
export default {
  name: "Slot-Booking-Form",
  props: {
    value: Boolean,
    vehicleTypeList: {
      type: Array,
      required: true,
    },
  },
  data() {
    return {
      isValid: true,
      nonFieldError: [],
      inputFormDetails: {
        vehicle_type: "Four Wheeler",
      },
      formErrors: {},
      today: moment().format("YYYY-MM-DD"),
      // vehicleTypeList: [],
      bookingDetails: {},
      paymentFormDialog: false,
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
    resetForm() {
      this.$refs.slotBookingForm.reset();
    },

    submitForm() {
      this.$api.slotBooking
        .addSlotBooking(this.inputFormDetails)
        .then((res) => {
          this.closeDialog();
          this.bookingDetails = res.data;
          this.$emit("refresh-list-page", res.data);
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

<style></style>
