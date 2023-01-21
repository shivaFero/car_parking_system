<template>
  <v-app>
    <router-view />
    <Vtoast
      v-model="showToaster"
      :message="vToasterMessage"
      :color="vToastColor"
    ></Vtoast>
  </v-app>
</template>

<script>
import Vtoast from "@/components/Vtoast.vue";
export default {
  components: {
    Vtoast,
  },
  data() {
    return {
      showToaster: false,
      vToasterMessage: "",
      vToastColor: "",
    };
  },
  mounted() {
    this.$bus.$on("showToaster", ({ color, message }) => {
      this.vToastColor = color;
      this.vToasterMessage = message;
      this.showToaster = true;
    });
  },
  beforeDestroy() {
    this.$bus.$off("showToaster");
  },
};
</script>

<style lang="scss"></style>
