<template>
  <GChart
    :settings="{
      packages: ['corechart'],
      mapsApiKey: 'AIzaSyA8b79CjjX-C9VgxMBF2aTs9fOI-UBT850',
    }"
    type="SteppedAreaChart"
    :data="chartData"
    :options="chartOptions"
  />
</template>

<script>
import { mapGetters } from 'vuex';

export default {
  name: 'RegistrationStackedChart',

  data() {
    return {
      API_URL: process.env.VUE_APP_API,
      chartData: [],
      chartOptions: {
        title: 'Anmedlungen',
        isStacked: true,
        legend: { position: 'right', maxLines: 3 },
        vAxis: { minValue: 0 },
      },
    };
  },
  computed: {
    ...mapGetters(['currentEventParticipants']),
  },
  created() {
    // this.debouncedGetAnswer = this._.debounce(this.json_to_chart_data, 500);
  },
  watch: {
    currentEventParticipants() {
      this.debouncedGetAnswer();
    },
  },
  methods: {
    json_to_chart_data() {
      const jsonData = this.currentEventParticipants;
      const chartData = [];
      const buende = [];
      jsonData.forEach((regis) => {
        if (buende.indexOf(regis.bund) === -1) buende.push(regis.bund);
      });
      chartData.push(['date'].concat(buende));
      jsonData.forEach((regis) => {
        // eslint-disable-next-line no-param-reassign
        regis.createdAt = new Date(regis.createdAt);
      });
      jsonData.sort((a, b) => a.createdAt.getTime() - b.createdAt.getTime());

      const buendeCount = new Array(buende.length).fill(0);
      jsonData.forEach((regis) => {
        buendeCount[buende.indexOf(regis.bund)] += regis.numberOfPersons;
        chartData.push([regis.createdAt].concat(buendeCount));
      });
      this.chartData = chartData;
    },
  },
};
</script>
