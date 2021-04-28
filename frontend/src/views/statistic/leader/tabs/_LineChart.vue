<template>
  <GChart
    :settings="{
      packages: ['corechart', 'line'],
      mapsApiKey: 'AIzaSyA8b79CjjX-C9VgxMBF2aTs9fOI-UBT850'
    }"
    type="LineChart"
    :data="chartData"
    :options="chartOptions"
  />
</template>

<script>
import { mapGetters } from 'vuex';

export default {
  name: 'RegistrationLineChart',

  data() {
    return {
      API_URL: process.env.VUE_APP_API,
      chartData: [],
      chartOptions: {
        title: 'Anmedlungen',
        curveType: 'function',
        legend: { position: 'right' },
        vAxis: { minValue: 0 },
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
        // eslint-disable-next-line no-param-reassign
        regis.createdAt = new Date(regis.createdAt);
      });
      jsonData.sort((a, b) => a.createdAt.getTime() - b.createdAt.getTime());

      let count = 0;
      jsonData.forEach((regis) => {
        count += regis.numberOfPersons;
        returnData.push([
          regis.createdAt,
          count,
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
