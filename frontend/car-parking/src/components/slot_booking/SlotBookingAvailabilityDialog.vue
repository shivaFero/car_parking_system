<template>
  <v-dialog
    max-width="500px"
    v-model="showDialog"
    persistent
    scrollable
    width="50%"
  >
    <v-card>
      <v-card-title
        class="text-lg-subtitle-1 text-xl-h6 text-uppercase font-weight-black primary white--text pb-4"
      >
        <h3>Today's Slot Availability</h3>
        <v-spacer />
        <v-btn
          depressed
          text
          small
          icon
          class="primary-text"
          @click="showDialog = false"
        >
          <v-icon>mdi-close</v-icon>
        </v-btn>
      </v-card-title>

      <v-card-text>
        <v-col cols="12">
          <v-text-field
            type="date"
            name="booking_date"
            label="Select Booking Date"
            outlined
            hide-details="auto"
            :min="today"
            v-model="booking_date"
            @input="getSlotAvailabilityList()"
          />
        </v-col>
      </v-card-text>

      <v-card
        outlined
        class="mr-2 pa-0"
        v-for="(value, name, index) in availabilityDetails"
        :key="index"
      >
        <div class="d-flex" outlined>
          <v-card-title class="light_grey py-1 pl-6 pr-1" style="width: 100%">
            <span
              :class="
                value >= 8
                  ? 'text-caption text-capitalize red--text'
                  : 'text-caption text-capitalize'
              "
            >
              {{ name.replaceAll("_", " ") }}
            </span>
          </v-card-title>
          <v-card-text class="py-2 text-center" style="width: 100%">
            <span class="cf-info-title font-weight-bold">
              {{ value }}
            </span>
          </v-card-text>
        </div>
      </v-card>
    </v-card>
  </v-dialog>
</template>

<script>
import moment from "moment";
export default {
  name: "Slot-Booking-Availability-Dialog",
  data() {
    return {
      today: moment().format("YYYY-MM-DD"),
      booking_date: null,
      availabilityDetails: {},
    };
  },
  props: {
    value: Boolean,
  },
  computed: {
    showDialog: {
      get() {
        return this.value;
      },
      set(value) {
        this.$emit("input", value);
      },
    },
  },
  methods: {
    getSlotAvailabilityList(params = {}) {
      params = {
        ...params,
        booking_date: this.booking_date,
      };
      this.$api.slotBooking
        .getSlotAvailability(params)
        .then((res) => {
          this.availabilityDetails = res.data;
        })
        .catch((err) => {
          console.error(err);
        });
    },
  },
  mounted() {
    this.getSlotAvailabilityList();
  },
};
</script>

<style></style>
