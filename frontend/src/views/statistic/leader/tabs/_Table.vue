<template>
  <Pivot
    :data="getItems"
    v-model="fields"
    :reducer="reducer"
    :showSettings="defaultShowSettings"
  />
</template>

<script>
import { mapGetters } from 'vuex';
import { Pivot } from 'vue-pivot-table-plus';
import axios from 'axios';

export default {
  name: 'RegistrationCalender',
  components: { Pivot },
  data: () => { // eslint-disable-line
    return {
      API_URL: process.env.VUE_APP_API,
      defaultShowSettings: true,
      data: [],
      fields: {
        availableFields: [],
        rowFields: [
          {
            getter: (item) => item.scoutOrganisation,
            label: 'Stamm',
          },
          {
            getter: (item) => item.isConfirmed,
            label: 'Bestätigt',
          },
          {
            getter: (item) => item.bundName,
            label: 'Bund',
            showHeader: false,
          },
        ],
        colFields: [
        ],
        fieldsOrder: {},
      },
      reducer: (sum, item) => sum + item.numberParticipant, // eslint-disable-line
      tableHeight: '400px',
    };
  },
  computed: {
    ...mapGetters(['currentEventParticipants']),
    getItems() {
      return this.data;
    },
  },
  methods: {
    getMessages() {
      const path = `${this.API_URL}basic/registration-stats/`;
      axios
        .get(path)
        .then((res) => {
          this.showSuccess = true;
          this.data = res.data;
        })
        .catch(() => {
          this.showError = true;
        });
    },
  },
  created() {
    this.getMessages();
  },
};
</script>
