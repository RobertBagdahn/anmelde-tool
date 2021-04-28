<template>
  <v-card class="mx-auto" :color="color" dark>
    <v-container fluid>
      <v-row align="center" justify="center" v-if="list.length">
        <v-list-item two-line>
          <v-list-item-content>
            <v-list-item-title class="headline">{{
              data.header
            }}</v-list-item-title>
            <v-list-item-subtitle>{{ data.subheader }}</v-list-item-subtitle>
          </v-list-item-content>
        </v-list-item>

        <v-list-item dense v-for="(item, index) in list" :key="index">
          <v-list-item-icon>
            <v-icon>mdi-account-group</v-icon>
          </v-list-item-icon>
          <v-list-item-content>
            <v-list-item-subtitle
              class="font-weight-bold"
              v-if="data.rankField === 'updatedAt'"
              v-text="formatData(item[data.rankField])"
            />
            <v-list-item-subtitle
              class="font-weight-bold"
              v-if="data.rankField !== 'updatedAt'"
              v-text="item[data.rankField]"
            />
            <v-list-item-subtitle
              >{{ `${item.scoutOrganisation} (${item.verbandName})` }}
            </v-list-item-subtitle>
          </v-list-item-content>
        </v-list-item>
      </v-row>
      <v-row class="ma-3" align="center" justify="center" v-else>
        <v-container fluid>
        <v-progress-circular
          :size="80"
          :width="10"
          class="ma-5"
          color="primary"
          indeterminate
        ></v-progress-circular>
        </v-container>
      </v-row>
    </v-container>

    <!-- <v-divider></v-divider>

    <v-card-actions>
      <v-btn text> Full Report </v-btn>
    </v-card-actions> -->
  </v-card>
</template>

<script>
import moment from 'moment';

export default {
  props: ['data', 'color'],
  computed: {
    list() {
      const xx = this._.orderBy(
        this.data.dataOne,
        [this.data.rankField],
        [this.data.rankOrder],
      ).slice(0, 5);
      return xx;
    },
  },
  methods: {
    formatData(item) {
      debugger;
      return moment(item).format(this.dateFormat);
    },
  },
  data() {
    return {
      dateFormat: 'DD.MM.YYYY',
    };
  },
};
</script>
