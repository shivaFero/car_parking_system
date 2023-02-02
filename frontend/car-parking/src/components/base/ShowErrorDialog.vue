<template>
  <v-row justify="center">
    <v-dialog v-model="dialog" persistent max-width="290">
      <v-card>
        <v-card-title class="text-h5"> Error From Server </v-card-title>
        <v-card-text> {{ errormessage }} </v-card-text>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn color="green darken-1" text @click="dialog = false">
            Close
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </v-row>
</template>

<script>
export default {
  data() {
    return {
      dialog: false,
    };
  },
  props: {
    value: Boolean,
    errors: {
      type: [Object, Array],
      required: false,
    },
    errormessage: {
      type: String,
      required: true,
    },
  },
};
</script>
