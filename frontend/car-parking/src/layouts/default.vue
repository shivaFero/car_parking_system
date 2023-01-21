<template>
  <v-app>
    <TheNavBar />
    <!-- <Header /> -->
    <v-main style="position: relative">
      <v-container
        fluid
        class="pa-0"
        style="height: 100% !important; position: absolute"
      >
        <router-view />
      </v-container>
    </v-main>
  </v-app>
</template>

<script>
import TheNavBar from "../components/TheNavBar.vue";
export default {
  name: "Default-Comp",
  components: {
    TheNavBar,
  },
};
</script>

<style></style>
