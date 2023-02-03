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
        <h3>Pricing Details</h3>
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

      <v-card
        outlined
        class="mr-2 pa-0"
        v-for="(value, name, index) in paymentInfoList"
        :key="index"
      >
        <div class="d-flex" outlined>
          <v-card-title class="light_grey py-1 pl-6 pr-1" style="width: 100%">
            <span class="text-caption text-capitalize">
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
export default {
  name: "Payment-Info-Dialog",
  data() {
    return {
      paymentInfoList: {},
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
    getPaymentInfoList(params = {}) {
      params = {
        ...params,
      };
      this.$api.slotBooking
        .getPaymentInfo(params)
        .then((res) => {
          this.paymentInfoList = res.data;
        })
        .catch((err) => {
          console.error(err);
        });
    },
  },
  mounted() {
    this.getPaymentInfoList();
  },
};
</script>

<style></style>
