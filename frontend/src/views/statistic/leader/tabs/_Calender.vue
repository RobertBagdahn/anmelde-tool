<template>
  <GChart
    :settings="{
        packages: ['corechart', 'calendar'],
        mapsApiKey: 'AIzaSyA8b79CjjX-C9VgxMBF2aTs9fOI-UBT850'
      }"
    type="Calendar"
    :data="chartData"
    :options="chartOptions"
    :events="chartEvents"
  />
</template>

<script>
import { mapGetters } from 'vuex';

export default {
  name: 'RegistrationCalender',
  data() {
    return {
      chartOptions: {
        colorAxis: { colors: ['blue', 'red'] },
        title: 'Anmeldungen',
        chartData: [],

      },
      chartEvents: {
        select: () => {
          const table = this.$refs.gChart.chartObject;
          const selection = table.getSelection();
          const onSelectionMessage = selection.length !== 0 ? 'row was selected' : 'row was diselected';
        },
      },
    };
  },

  computed: {
    ...mapGetters(['currentEventParticipants']),

  },

  methods: {
    json_to_chart_data(jsonData) {
      const returnData = [];
      returnData.push(['date', 'number']);
      jsonData.forEach((regis) => {
        returnData.push([
          new Date(regis.createdAt),
          regis.numberOfPersons,
        ]);
      });
      return returnData;
    },
    getData() {
      this.chartData = this.json_to_chart_data(this.currentEventParticipants);
    },
  },
  created() {
    // this.getData();
  },
};
</script>
