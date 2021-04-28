<template>
  <v-card class="mx-auto" :color="color" dark>
    <v-container fluid>
      <v-row align="center" justify="center" v-if="list.dataOne">
        <v-list-item two-line>
          <v-list-item-content>
            <v-list-item-title class="headline">{{
              list.header
            }}</v-list-item-title>
            <v-list-item-subtitle>{{ list.subheader }}</v-list-item-subtitle>
          </v-list-item-content>
        </v-list-item>

        <v-card-text>
          <v-row align="center">
            <v-col class="display-3" cols="6">{{ list.dataOne }}</v-col>
            <v-col class="display-3" cols="6">{{ list.dataTwo }}</v-col>
          </v-row>
          <v-row align="center">
            <v-col cols="6">{{ list.dataOneName }}</v-col>
            <v-col cols="6">{{ list.dataTwoName }}</v-col>
          </v-row>
        </v-card-text>
      </v-row>
      <v-row class="ma-3" align="center" justify="center" v-else>
        <v-progress-circular
          :size="80"
          :width="10"
          class="ma-5"
          color="primary"
          indeterminate
        ></v-progress-circular>
      </v-row>
    </v-container>
    <!-- <v-divider></v-divider>

    <v-card-actions>
      <v-btn text> Full Report </v-btn>
    </v-card-actions> -->
  </v-card>
</template>

<script>
export default {
  props: ['data', 'color'],
  computed: {
    list() {
      return this.data;
    },
  },
  data: () => ({}),
};
</script>
