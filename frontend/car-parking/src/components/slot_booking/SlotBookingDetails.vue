<template>
  <v-dialog max-width="750px" v-model="showDialog">
    <v-card v-if="showDetails && Object.keys(showDetails).length > 0">
      <div ref="downloadAsPdfContentRef">
        <v-card-title class="blue text-white py-2">
          <span v-if="showDetails.pass_id" class="pr-2">
            {{ `${showDetails.pass_id}'s` }}
          </span>

          {{ "Booking Detail's" }}
          <v-spacer></v-spacer>
          <v-btn icon class="text-white" @click="showDialog = false">
            <v-icon>mdi-close</v-icon>
          </v-btn>
        </v-card-title>
        <!-- -----------------------BARCODE ---------------------->
        <v-col cols="12" class="d-flex justify-center">
          <VueBarcode :value="showDetails.pass_id"> </VueBarcode>
        </v-col>

        <v-card-text class="pa-5">
          <v-row>
            <v-col
              cols="6"
              class="d-flex"
              v-for="(value, name, index) in showDetails"
              :key="index"
            >
              <v-row class="py-3" v-if="!(typeof value === 'object')">
                <span class="text-subtitle-1 text-capitalize">
                  {{ name.replaceAll("_", " ").toLowerCase() }} :</span
                >
                <span class="text-subtitle-2 font-weight-black pl-5">{{
                  value || "N/A"
                }}</span>
              </v-row>
              <v-row v-else>
                <v-col cols="12" v-if="value && value.length > 0">
                  <h3>
                    {{ name.replaceAll("_", " ").toUpperCase() }}
                  </h3>
                </v-col>
                <v-col v-if="value && value.length > 0">
                  <v-col
                    v-for="(paymentValue, paymentKey, paymentIndex) in value[0]"
                    :key="paymentIndex"
                  >
                    <span class="text-subtitle-1 text-capitalize">
                      {{ paymentKey }} :</span
                    >
                    <span class="text-subtitle-2 font-weight-black pl-5">{{
                      paymentValue || "N/A"
                    }}</span>
                  </v-col>
                </v-col>
              </v-row>
            </v-col>
          </v-row>
        </v-card-text>
      </div>
      <v-card-actions class="d-flex justify-end">
        <v-btn class="primary text-uppercase mr-3" @click="exportToPDF">
          Download In PDF Format
        </v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>

<script>
import html2pdf from "html2pdf.js";
import VueBarcode from "vue-barcode";
export default {
  name: "slot-Booking-details",
  components: {
    VueBarcode,
  },
  props: {
    value: {
      type: Boolean,
    },
    showDetails: {
      type: Object,
      required: true,
    },
  },
  data() {
    return {};
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
    exportToPDF() {
      html2pdf(this.$refs.downloadAsPdfContentRef, {
        margin: 1,
        filename: this.showDetails.pass_id,
        image: { type: "jpeg", quality: 0.98 },
        html2canvas: { dpi: 200 },
        jsPDF: { unit: "in", format: "letter" },
      });
    },
  },
};
</script>

<style></style>
