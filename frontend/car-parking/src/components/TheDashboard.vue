<template>
  <div class="d-flex ml-8 mt-12">
    <v-row class="pb-6">
      <v-row class="pl-5">
        <v-col cols="3">
          <v-text-field
            type="date"
            name="from_date"
            label="From Date"
            outlined
            hide-details="auto"
            v-model="filters.from_date"
            @input="getDashboardData()"
          />
        </v-col>
        <v-col cols="3">
          <v-text-field
            type="date"
            name="to_date"
            label="To Date"
            outlined
            hide-details="auto"
            :min="filters.from_date"
            v-model="filters.to_date"
            @input="getDashboardData()"
          />
        </v-col>
      </v-row>
      <v-col cols="12">
        <h3 class="text-capitalize">7 day's Data</h3>
      </v-col>
      <v-col
        cols="12"
        style="display: grid; grid-template-columns: repeat(4, 1fr); gap: 24px"
      >
        <v-card
          v-for="(item, i) in dashboardStatics"
          :key="i"
          style="border: 1px solid #8080807a !important; width: 100%"
          class="pa-5"
          outlined
          :color="item.color"
        >
          <v-row no-gutters>
            <v-col cols="12" class="pb-3">
              <v-icon
                style="font-size: 50px !important"
                class="card-icon-my"
                :class="'white--text'"
                >{{ item.icon }}</v-icon
              >
            </v-col>
            <v-col cols="12" class="pl-2">
              <h1 class="white--text">{{ dashboardData[item.key] || 0 }}</h1>
            </v-col>
            <v-col cols="12" class="d-flex justify-start">
              <h3 class="text-capitalize font-weight-bolder white--text">
                {{ item.title }}
              </h3>
            </v-col>
          </v-row>
        </v-card>
      </v-col>

      <!-- -------------------------------------Payment Overview ----------------------- -->
      <v-col cols="12" v-if="dashboardData?.payment_overview?.payment_count">
        <v-col cols="12">
          <v-divider></v-divider>
        </v-col>
        <h3>Payment Overview</h3>
      </v-col>
      <!-- --------------------------------------Payment Count ------------------------- -->
      <v-col cols="3" v-if="dashboardData?.payment_overview?.payment_count">
        <v-card
          style="border: 1px solid #8080807a !important; width: 100%"
          class="pa-5"
          outlined
          color="#444747"
        >
          <v-card-title> Payment In Count </v-card-title>
          <v-card-text>
            <v-row no-gutters>
              <v-col cols="12">
                <v-row
                  no-gutters
                  v-for="(value, name, index) in dashboardData.payment_overview
                    .payment_count"
                  :key="index"
                >
                  <v-col cols="6" class="py-1">
                    <span
                      class="cf-info-title font-weight-bold text-capitalize white--text"
                    >
                      {{ name }}
                    </span>
                  </v-col>
                  <v-col cols="6" class="d-flex justify-end py-1">
                    <span class="black--text font-weight-bold white--text">
                      {{ value }}
                    </span>
                  </v-col>
                </v-row>
              </v-col>
            </v-row>
          </v-card-text>
        </v-card>
      </v-col>
      <!-- --------------------------------------Payment Percentage ------------------------- -->
      <v-col
        cols="3"
        v-if="dashboardData?.payment_overview?.payment_in_percentage"
      >
        <v-card
          style="border: 1px solid #8080807a !important; width: 100%"
          class="pa-5"
          outlined
          color="#7f798f"
        >
          <v-card-title> Payment In Percentage(%) </v-card-title>
          <v-card-text>
            <v-row no-gutters>
              <v-col cols="12">
                <v-row
                  no-gutters
                  v-for="(value, name, index) in dashboardData.payment_overview
                    .payment_in_percentage"
                  :key="index"
                >
                  <v-col cols="6" class="py-1">
                    <span
                      class="cf-info-title font-weight-bold text-capitalize white--text"
                    >
                      {{ name }}
                    </span>
                  </v-col>
                  <v-col cols="6" class="d-flex justify-end py-1">
                    <span class="black--text font-weight-bold white--text">
                      {{ value }}
                    </span>
                  </v-col>
                </v-row>
              </v-col>
            </v-row>
          </v-card-text>
          <!-- --------------------------------------Payment Percentage ------------------------- -->
        </v-card>
      </v-col>
    </v-row>
  </div>
</template>

<script>
import moment from "moment";
export default {
  name: "TheDashboard-Comp",
  data() {
    return {
      today: moment().format("YYYY-MM-DD"),
      filters: {},
      dashboardData: {},
      dashboardStatics: [
        {
          title: "Total Booking",
          value: 0,
          icon: "mdi-truck",
          color: "#30328D",
          key: "total_booking",
        },
        {
          title: "Per Day Booking",
          value: 0,
          icon: "mdi-truck-cargo-container",
          color: "#2196F3",
          key: "per_day_booking",
        },
        {
          title: "Total Booking Hours",
          value: 0,
          icon: "mdi-truck-cargo-container",
          color: "#308D3C",
          key: "total_booking_hours",
        },

        {
          title: "Total Booking Hours Per Day",
          value: 0,
          icon: "mdi-truck-cargo-container",
          color: "#5d5c63",
          key: "total_booking_hours_per_day",
        },
        {
          title: "Total Amount",
          value: 0,
          icon: "mdi-truck-cargo-container",
          color: "#0ad14d",
          key: "total_amount",
        },
        {
          title: "Total Users",
          value: 0,
          icon: "mdi-truck-cargo-container",
          color: "#024020",
          key: "total_users",
        },
        {
          title: "Unique Users",
          value: 0,
          icon: "mdi-truck-cargo-container",
          color: "#515e03",
          key: "unique_user",
        },
      ],
    };
  },
  methods: {
    getDashboardData(params = {}) {
      if (this.filters?.from_date >= this.filters.to_date) {
        alert("From Date can't be greater than or equal to To date");
        return;
      }
      params = {
        ...params,
        ...this.filters,
      };
      this.$api.dashboard
        .getDashboardData(params)
        .then((res) => {
          this.dashboardData = res.data;
        })
        .catch((err) => {
          console.error(err);
        });
    },
  },
  mounted() {
    this.getDashboardData();
  },
};
</script>

<style></style>
