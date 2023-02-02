<template>
  <div>
    <v-tooltip top>
      <template v-slot:activator="{ on, attrs }">
        <v-icon
          class="mr-4"
          v-bind="attrs"
          v-on="on"
          @click="showSlotBookingDetails()"
          >mdi-eye</v-icon
        >
      </template>
      <span class="text-capitalize">Show Booking Details</span>
    </v-tooltip>

    <v-tooltip top v-if="params.data.booking_status == 'In'">
      <template v-slot:activator="{ on, attrs }">
        <v-icon
          class="mr-4 red--text"
          v-bind="attrs"
          v-on="on"
          @click="cancelSlotBooking()"
          >mdi-calendar-remove</v-icon
        >
      </template>
      <span class="text-capitalize">Cancel Booking</span>
    </v-tooltip>
  </div>
</template>

<script>
export default {
  methods: {
    cancelSlotBooking() {
      this.params.context.parentComponent.cancelSlotBooking(
        this.params.data.id
      );
    },
    showSlotBookingDetails() {
      this.params.context.parentComponent.getSlotBookingDetails(
        this.params.data.id
      );
    },
  },
};
</script>
