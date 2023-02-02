<template>
  <v-dialog max-width="850px" v-model="showDialog">
    <v-card v-if="showDetails && Object.keys(showDetails).length > 0">
      <v-card-title class="blue text-white py-2">
        <span class="pr-2">
          {{ title }}
        </span>

        <v-spacer></v-spacer>
        <v-btn icon class="text-white" @click="showDialog = false">
          <v-icon>mdi-close</v-icon>
        </v-btn>
      </v-card-title>
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
          </v-col>
        </v-row>
      </v-card-text>
    </v-card>
  </v-dialog>
</template>

<script>
export default {
  name: "Base-Details",
  props: {
    value: {
      type: Boolean,
    },
    showDetails: {
      type: Object,
      required: true,
    },
    title: {
      type: String,
      default: "View Details",
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
};
</script>

<style></style>
