<template>
  <v-col cols="12" md="3">
    <div class="pa-4 indigo darken-2 text-no-wrap rounded-pill">
      rounded-pill
    </div>
  </v-col>
</template>

<script>
export default {
  props: {
    listOfData: {
      type: Array,
      required: true,
    },
  },
};
</script>

<style></style>
