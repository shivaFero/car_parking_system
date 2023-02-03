<template>
  <v-dialog v-model="filterDialog" width="650">
    <v-card class="pa-6">
      <v-card-title class="mb-2">
        <span
          class="text-lg-subtitle-1 text-xl-h6 text-uppercase font-weight-bold primary--text"
        >
          {{ "filters" }}
        </span>
        <v-spacer />
        <v-btn class="mt-n3" icon @click="filterDialog = false">
          <v-icon>mdi-close</v-icon>
        </v-btn>
      </v-card-title>
      <v-card-text>
        <v-row no-gutters>
          <v-col cols="12" lg="12" xl="12" class="py-2">
            <span class="text-body-2 font-weight-bold text-capitalize">{{
              "Filter By Status"
            }}</span>
            <v-select
              dense
              clearable
              hide-details
              outlined
              label="Select Booking Status"
              :items="statusTypes"
              item-text="display_name"
              item-value="value"
              v-model="bindingObject.booking_status"
              :menu-props="{ offsetY: true }"
              class="pt-2"
            ></v-select>
          </v-col>
          <v-col cols="12" lg="12" xl="12" class="py-2">
            <span class="text-body-2 font-weight-bold text-capitalize">
              {{ "filter by date" }}
            </span>
            <v-row class="mt-1">
              <v-col cols="6">
                <v-text-field
                  type="date"
                  name="from_date"
                  label="Booking Date*"
                  outlined
                  hide-details="auto"
                  v-model="bindingObject.from_date"
                />
              </v-col>
              <v-col cols="6">
                <v-text-field
                  type="date"
                  name="to_date"
                  label="To Date*"
                  outlined
                  :min="bindingObject.from_date"
                  hide-details="auto"
                  v-model="bindingObject.to_date"
                />
              </v-col>
            </v-row>
          </v-col>
        </v-row>
        <v-row no-gutters>
          <v-col cols="12" lg="6" xl="6" class="pt-2">
            <span class="text-body-2 font-weight-bold text-capitalize pl-1">{{
              "order by"
            }}</span>
            <v-select
              dense
              hide-details
              outlined
              clearable
              label="select value"
              :items="orderBy"
              item-text="display_name"
              item-value="value"
              v-model="bindingObject.ordering"
              class="pt-2 pl-1"
              :menu-props="{ offsetY: true }"
            ></v-select>
          </v-col>
        </v-row>
      </v-card-text>
      <v-card-actions class="px-6 pb-4">
        <v-spacer></v-spacer>
        <v-btn
          depressed
          color="primary"
          class="text-capitalize"
          @click="$emit('applyFilters')"
        >
          {{ "apply" }}
        </v-btn>
        <v-btn depressed class="text-capitalize" @click="$emit('resetFilters')">
          {{ "reset" }}
        </v-btn>
        <v-btn depressed class="text-capitalize" @click="filterDialog = false">
          {{ "cancel" }}
        </v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>

<script>
export default {
  name: "Slot-Booking-Filter",
  props: {
    value: Boolean,
    filterObject: {
      type: Object,
      default: () => ({}),
    },
  },
  data() {
    return {
      orderBy: [
        { display_name: "Booking Date", value: "booking_date" },
        { display_name: "Booking Date (Descending)", value: "-booking_date" },
        { display_name: "Exit Date", value: "exit_date_time" },
        { display_name: "Exit Date (Descending)", value: "-exit_date_time" },
      ],
      statusTypes: [
        {
          display_name: "In",
          value: "In",
        },
        {
          display_name: "Out",
          value: "Out",
        },
        {
          display_name: "Cancel",
          value: "Cancel",
        },
      ],
    };
  },
  computed: {
    filterDialog: {
      get() {
        return this.value;
      },
      set(value) {
        this.$emit("input", value);
      },
    },
    bindingObject: {
      get() {
        return this.filterObject;
      },
      set(val) {
        this.$emit("input", val);
      },
    },
  },
  methods: {},
};
</script>
