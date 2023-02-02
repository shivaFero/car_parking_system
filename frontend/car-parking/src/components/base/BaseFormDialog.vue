<template>
  <v-dialog :max-width="dialogWidth" v-model="showDialog">
    <v-card>
      <v-card-title class="blue text-white py-2">
        <span class="pr-2 text-capitalize">
          {{ title }}
        </span>

        <v-spacer></v-spacer>
        <v-btn icon class="text-white" @click="showDialog = false">
          <v-icon>mdi-close</v-icon>
        </v-btn>
      </v-card-title>

      <div v-if="isAlreadyCard">
        <v-card-text class="pa-5">
          <slot name="cardFormContent"></slot>
        </v-card-text>
        <v-card-actions>
          <slot name="cardFormActions"></slot>
        </v-card-actions>
      </div>
      <div v-else>
        <slot name="flatFormContent"></slot>
        <slot name="flatFormActions"></slot>
      </div>
    </v-card>
  </v-dialog>
</template>

<script>
export default {
  name: "Base-Form-Dialog",
  props: {
    value: {
      type: Boolean,
    },
    title: {
      type: String,
      default: "Form",
    },
    dialogWidth: {
      type: [Number, String],
      default: "750px",
    },
    isAlreadyCard: {
      type: Boolean,
      default: false,
    },
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
