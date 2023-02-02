<template>
  <div>
    <AgGridTable
      title="Slot Booking"
      :tableData="slotBookingList"
      :tableHeader="tableHeaders"
      :total="totalItems"
      :context="context"
      @getList="getSlotBookingList"
      :tableScrollable="true"
      localStorageKey="slot_booking_columns"
      :isColumnShowVisibility="true"
    >
      <template #afterTitle>
        <v-col class="d-flex justify-start">
          <v-btn
            depressed
            color="primary"
            class="rounded"
            @click="slotAvailabilityDialog = true"
          >
            <v-icon small class="mr-1">mdi-calendar-month</v-icon>
            Check Slot Availability
          </v-btn>
          <v-btn
            depressed
            color="primary mx-3"
            class="rounded"
            @click="paymentInfoDialog = true"
          >
            <v-icon small class="mr-1">mdi-cash-multiple</v-icon>
            View Pricing
          </v-btn>
        </v-col>
      </template>
      <template #leftFilterSlot>
        <v-col class="d-flex justify-end">
          <v-btn
            depressed
            color="primary"
            class="rounded"
            @click="openFilterDialog = true"
          >
            <v-icon small class="mr-1">mdi-filter</v-icon>
            Filter
          </v-btn>
        </v-col>
      </template>
      <template #listAction>
        <v-btn small depressed class="primary" @click="addSlots()">
          <v-icon small class="mr-1">mdi-plus</v-icon>
          <span class="mr-2">Book Slot</span>
        </v-btn>
      </template>
      <template #dialogs>
        <v-col v-if="showFormDialog">
          <SlotBookingForm
            v-model="showFormDialog"
            :vehicle-type-list="vehicleTypeList"
            @refresh-list-page="refreshListPage"
          />
        </v-col>
        <v-col v-if="paymentFormDialog">
          <SlotBookingPaymentForm
            v-model="paymentFormDialog"
            :slotBookingObject="currentBookingDetails"
            @payment-collected="getSlotBookingList()"
          />
        </v-col>
        <v-col v-if="showBookingDetails">
          <SlotBookingDetails
            v-model="showBookingDetails"
            :showDetails="bookingDetails"
          />
        </v-col>
        <v-col v-if="openFilterDialog">
          <SlotBookingFilter
            v-model="openFilterDialog"
            :filterObject="filter"
            @applyFilters="applyFilters"
            @resetFilters="resetFilters"
          />
        </v-col>
        <v-col v-if="openBookingCancellationDialog">
          <SlotBookingCancellationDialog
            v-model="openBookingCancellationDialog"
            :slot-id="slotId"
            @refresh-list="getSlotBookingList()"
          />
        </v-col>
        <v-col v-if="slotAvailabilityDialog">
          <SlotBookingAvailabilityDialog v-model="slotAvailabilityDialog" />
        </v-col>
        <v-col v-if="paymentInfoDialog">
          <SlotPaymentInfoDialog v-model="paymentInfoDialog" />
        </v-col>
      </template>
    </AgGridTable>
  </div>
</template>

<script>
/* eslint-disable */
import AgGridTable from "@/components/base/AgGridTable.vue";
import SlotBookingForm from "@/components/slot_booking/SlotBookingForm.vue";
import SlotBookingPaymentForm from "@/components/slot_booking/SlotBookingPaymentForm.vue";
import SlotBookingActionButton from "@/components/slot_booking/SlotBookingActionButton.vue";
import SlotBookingDetails from "@/components/slot_booking/SlotBookingDetails.vue";
import SlotBookingFilter from "@/components/slot_booking/SlotBookingFilter.vue";
import SlotBookingCancellationDialog from "@/components/slot_booking/SlotBookingCancellationDialog.vue";
import SlotBookingAvailabilityDialog from "@/components/slot_booking/SlotBookingAvailabilityDialog.vue";
import SlotPaymentInfoDialog from "@/components/slot_booking/SlotPaymentInfoDialog.vue";
export default {
  name: "SlotBooking-Page",
  components: {
    AgGridTable,
    SlotBookingForm,
    SlotBookingPaymentForm,
    SlotBookingActionButton,
    SlotBookingDetails,
    SlotBookingFilter,
    SlotBookingCancellationDialog,
    SlotBookingAvailabilityDialog,
    SlotPaymentInfoDialog,
  },
  data() {
    return {
      showFormDialog: false,
      paymentFormDialog: false,
      showBookingDetails: false,
      openFilterDialog: false,
      openBookingCancellationDialog: false,
      slotAvailabilityDialog: false,
      paymentInfoDialog: false,
      filter: {},
      // Pagination Vars
      itemsPerPage: 10,
      totalItems: 0,
      pageNo: 1,
      // List Layout Com vars
      headerSelected: [
        {
          headerName: "Username",
          hide: false,
          pinned: "left",
          field: "username",
        },
        {
          headerName: "Vehicle Number",
          pinned: "left",
          hide: false,
          field: "vehicle_no",
        },
        {
          headerName: "First Name",
          hide: false,
          field: "first_name",
        },
        {
          headerName: "Last Name",
          hide: false,
          field: "last_name",
        },
        {
          headerName: "Pass ID",
          hide: false,
          field: "pass_id",
        },
        {
          headerName: "Booking Date",
          hide: false,
          field: "booking_date",
        },
        {
          headerName: "From Time",
          hide: false,
          field: "from_time",
        },
        {
          headerName: "To Time",
          hide: false,
          field: "to_time",
        },
        {
          headerName: "Exit date Time",
          hide: false,
          field: "exit_date_time",
        },
        {
          headerName: "Booking Status",
          hide: false,
          field: "booking_status",
        },
        {
          headerName: "Slot Assigned",
          hide: false,
          field: "slot_assigned",
        },
        {
          headerName: "Total Booking Duration",
          hide: false,
          field: "total_booking_hrs",
        },
      ],
      // Other vars
      slotId: null,
      slotBookingList: [],
      currentBookingDetails: {},
      bookingDetails: {},
      vehicleTypeList: [],
    };
  },
  computed: {
    totalPages() {
      return Math.ceil(this.totalItems / this.itemsPerPage);
    },
    offset() {
      return this.itemsPerPage * (this.pageNo - 1);
    },
    tableHeaders() {
      return [
        ...this.headerSelected,

        {
          headerName: "Actions",
          field: "actions",
          pinned: "right",
          minWidth: 150,
          sortable: false,
          width: 250,
          cellRenderer: "SlotBookingActionButton",
        },
      ];
    },
    context() {
      return { parentComponent: this };
    },
  },
  methods: {
    getSlotBookingList(params = {}) {
      params = {
        ...params,
        ...this.filter,
      };
      this.$api.slotBooking
        .getSlotBookingList(params)
        .then((res) => {
          this.totalItems = res.count;
          this.slotBookingList = res.data;
        })
        .catch((err) => {
          console.error(err);
        });
    },
    addSlots() {
      this.showFormDialog = true;
      this.getSlotBookingOptionList();
    },
    getSlotBookingDetails(id) {
      this.$api.slotBooking
        .getSlotBookingDetails(id)
        .then((res) => {
          this.bookingDetails = res.data;
          this.showBookingDetails = true;
        })
        .catch((err) => {
          console.error(err);
          this.$bus.emit("showToaster", {
            message: err.message || "something went wrong",
            color: "error",
          });
        });
    },
    cancelSlotBooking(id) {
      this.slotId = id;
      this.openBookingCancellationDialog = true;
    },
    onGridReady(params) {
      this.gridApi = params.api;
      this.gridColumnApi = params.columnApi;
    },
    headersChanged(value) {
      this.headerSelected = value;
    },
    refreshListPage(data) {
      this.paymentFormDialog = true;
      this.currentBookingDetails = data;
    },
    applyFilters() {
      if (!this.filter?.from_date) {
        delete this.filter.from_date;
      }
      if (!this.filter?.to_date) {
        delete this.filter.to_date;
      }
      if (!this.filter?.status) {
        delete this.filter.status;
      }
      if (!this.filter?.ordering) {
        delete this.filter.ordering;
      }
      localStorage.setItem("slotBookingFilter", JSON.stringify(this.filter));
      this.openFilterDialog = false;
      this.getSlotBookingList({ limit: 10, offset: 0 });
    },
    resetFilters() {
      localStorage.removeItem("slotBookingFilter");
      this.filter = {};
      this.getSlotBookingList({ limit: 10, offset: 0 });
    },
    getSlotBookingOptionList(params = {}) {
      this.$api.slotBooking
        .getSlotBookingOptions(params)
        .then((res) => {
          const data = res.data?.actions?.POST;
          this.vehicleTypeList = data?.vehicle_type?.choices || [];
        })
        .catch((err) => {
          console.error(err);
        });
    },
  },
};
</script>

<style></style>
