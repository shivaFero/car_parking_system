<template>
  <v-app>
    <TheNavBar />
    <TheHeader />
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
import TheNavBar from "@/components/TheNavBar.vue";
import TheHeader from "@/components/TheHeader.vue";
export default {
  name: "Default-Comp",
  components: {
    TheNavBar,
    TheHeader,
  },
};
</script>

<style></style>
