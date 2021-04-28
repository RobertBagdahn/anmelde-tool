<template>
  <v-container>
    <v-row>
      <v-btn
        class="ma-2"
        @click="clickDownload('event_locations_fee')"
        color="primary"
      >
        <v-icon left> mdi-microsoft-excel </v-icon>
        Zeltplatgebühren
      </v-btn>
    </v-row>
    <v-row>
      <v-btn
        class="ma-2"
        color="primary"
        @click="clickDownload('travel-preference')"
        download
      >
        <v-icon left> mdi-microsoft-excel </v-icon>
        Reise Preferenz
      </v-btn>
    </v-row>
    <v-row>
      <v-btn
        class="ma-2"
        @click="clickDownload('text-package-address')"
        download
        color="primary"
      >
        <v-icon left> mdi-microsoft-excel </v-icon>
        Packet Adressen
      </v-btn>
    </v-row>
  </v-container>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      API_URL: process.env.VUE_APP_API,
    };
  },
  computed: {
    eventId() {
      return this.$route.params.id;
    },
  },
  methods: {
    getLink(name) {
      return `${this.API_URL}basic/event/${this.eventId}/xlsx-generator/${name}/`;
    },

    clickDownload(name) {
      const config = { responseType: 'blob' };

      axios.get(this.getLink(name), config).then((response) => {
        const fileURL = window.URL.createObjectURL(new Blob([response.data]));
        const fileLink = document.createElement('a');

        fileLink.href = fileURL;
        fileLink.setAttribute('download', `${name}.xlsx`);
        document.body.appendChild(fileLink);

        fileLink.click();
      });
    },
  },
};
</script>
