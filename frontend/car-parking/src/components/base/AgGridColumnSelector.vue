<template>
  <v-autocomplete
    outlined
    :items="allHeaders"
    v-model="headersSelected"
    v-bind="$attrs"
    return-object
    label="Choose columns to show"
    multiple
    dense
    chips
    :item-text="itemText"
    :item-value="itemValue"
    :allow-overflow="false"
    hide-details
  >
    <template v-slot:selection="{ index }">
      <span class="text-body-2 text-capitalize" v-if="index === 0">
        {{ headersSelected.length }} columns selected
      </span>
    </template>
    <template v-slot:item="{ item }">
      <v-list-item
        :disabled="isItemSelected(item) && selectedHeaderKeys.length < 3"
        :class="{ 'v-list-item--active': isItemSelected(item) }"
        ripple
        @mousedown.prevent
        @click="toggle(item)"
      >
        <v-list-item-action>
          <v-icon :color="selectedHeaders.length > 0 ? 'indigo darken-4' : ''">
            {{
              isItemSelected(item)
                ? "mdi-checkbox-marked"
                : "mdi-checkbox-blank-outline"
            }}
          </v-icon>
        </v-list-item-action>
        <v-list-item-content>
          <v-list-item-title class="text-capitalize">
            {{ item.headerName }}
          </v-list-item-title>
        </v-list-item-content>
      </v-list-item>
    </template>
  </v-autocomplete>
</template>

<script>
export default {
  props: {
    allHeaders: {
      type: Array,
      default: () => [],
    },
    selectedHeaders: {
      type: Array,
      default: () => [],
    },
    localStorageKey: {
      type: String,
    },
    itemText: {
      type: String,
      default: "headerName",
    },
    itemValue: {
      type: String,
      default: "field",
    },
  },
  computed: {
    headersSelected: {
      get() {
        return this.selectedHeaders;
      },
      set(value) {
        this.$emit("headers-changed", value);
      },
    },
    selectedHeaderKeys() {
      return this.selectedHeaders.map((key) => key.field);
    },
  },
  methods: {
    toggle(item) {
      if (this.isItemSelected(item)) {
        this.headersSelected.splice(
          this.selectedHeaderKeys.indexOf(item.field),
          1
        );
      } else {
        this.headersSelected.push(item);
      }
      this.headersSelected = [...this.headersSelected];
    },
    isItemSelected(item) {
      return this.selectedHeaderKeys.indexOf(item.field) > -1;
    },
    async updateLanguage() {
      if (this.selectedHeaderKeys.length) {
        const selectedHeaders = this.allHeaders.filter(
          (head) =>
            head.field != "actions" &&
            this.selectedHeaderKeys.indexOf(head.field) > -1
        );
        if (selectedHeaders) {
          localStorage.setItem(
            `${this.localStorageKey}`,
            JSON.stringify(selectedHeaders)
          );
        }
      }
    },
    populateHeaders() {
      this.updateLanguage();
      let headers;
      if (this.localStorageKey && this.localStorageKey.length) {
        if (localStorage.getItem(`${this.localStorageKey}`)) {
          headers = JSON.parse(localStorage.getItem(`${this.localStorageKey}`));
        }
      }
      localStorage;
      if (!headers) {
        this.headersSelected = this.allHeaders.filter(
          (v) => v.value != "actions"
        );
      } else {
        this.headersSelected = headers;
      }
    },
  },
  mounted() {
    this.populateHeaders();
  },
};
</script>
