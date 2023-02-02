<template>
  <v-row class="ma-0">
    <v-col cols="12" class="d-flex justify-end align-center py-2">
      <v-select
        style="max-width: 60px !important"
        class="mr-2"
        dense
        hide-details
        :items="itemsPerPageValues"
        v-model="itemsPerPage"
        :menu-props="{ offsetY: true }"
      />
      <v-btn
        :disabled="pageNo == 1"
        x-small
        fab
        text
        class="rounded-lg elevation-0"
        @click="previousPage()"
      >
        <v-icon>mdi-arrow-left</v-icon>
      </v-btn>
      <span class="pa-2">
        <span>{{ pageNo }}</span>
        <span>/</span>
        <span>{{ totalPages == 0 ? 1 : totalPages }}</span>
      </span>
      <v-btn
        x-small
        fab
        text
        :disabled="pageNo == totalPages || totalPages == 0"
        class="rounded-lg elevation-0"
        @click="nextPage()"
      >
        <v-icon>mdi-arrow-right</v-icon>
      </v-btn>
    </v-col>
  </v-row>
</template>

<script>
export default {
  name: "basePagination",
  props: {
    pageNo: {
      require: true,
    },
    totalItems: {
      require: true,
    },
    pageSize: {
      require: true,
    },
  },
  data() {
    return {
      itemsPerPageValues: [10, 20, 50, 100],
    };
  },
  computed: {
    itemsPerPage: {
      get() {
        return this.pageSize;
      },
      set(value) {
        this.$emit("itemsPerPageChange", value);
      },
    },
    totalPages() {
      return Math.ceil(this.totalItems / this.pageSize);
    },
  },
  methods: {
    previousPage() {
      this.$emit("prevPage");
    },
    nextPage() {
      this.$emit("nextPage");
    },
  },
};
</script>

<style></style>
