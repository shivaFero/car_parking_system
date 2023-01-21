<template>
  <v-navigation-drawer
    permanent
    clipped
    app
    mini-variant
    expand-on-hover
    width="250"
    dark
  >
    <v-list dense>
      <v-list-item
        class="border-bottom-light_blue"
        v-for="(item, i) in navBar"
        :key="i"
        :to="item.to"
        router
        exact
      >
        <v-list-item-action>
          <v-icon class="text-h6 font-weight-light">{{ item.icon }}</v-icon>
        </v-list-item-action>
        <v-list-item-content>
          <v-list-item-title v-text="item.title" />
        </v-list-item-content>
      </v-list-item>
    </v-list>
  </v-navigation-drawer>
</template>

<script>
export default {
  data() {
    return {
      navBar: [
        {
          title: "dashboard",
          icon: "mdi-monitor-dashboard",
          to: "/auth/dashboard",
        },
        {
          title: "Parking Booking",
          icon: "mdi-calendar-clock",
          to: "/auth/slot_booking",
        },
      ],
    };
  },
};
</script>

<style lang="scss"></style>
